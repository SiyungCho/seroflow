"""Module: odbc_loader.py

This module provides a concrete implementation for loading pandas DataFrames into
an ODBC-accessible database (e.g., SQL Server) using raw SQL executed via a pyodbc.Connection.
It defines the ODBCLoader class which writes a DataFrame to a target table, supporting append,
replace, or error-if-exists modes, and automatic table creation with datatype inference.
"""

import pandas as pd
from ..load.loader import Loader

class ODBCLoader(Loader):
    """
    Loader for ODBC-accessible targets. Inserts a pandas DataFrame into a database table via ODBC.

    Supports three existence behaviors:
        - append (default): Add rows to an existing table.
        - replace: Drop and recreate the table before loading.
        - error: Raise if the target table already exists.
    """

    def __init__(
        self,
        target: str,
        engine,
        dataframe: str,
        schema: str,
        step_name: str = "ODBCLoader",
        exists: str = "append",
        on_error=None,
        **kwargs
    ):
        """
        Initialize an ODBCLoader.

        Args:
            target (str): Name of the destination table.
            engine (pyodbc.Connection): Active ODBC connection.
            dataframe (str): Name of DataFrame to load.
            schema (str): Database schema or owner for qualifying the target.
            step_name (str): Identifier for this load step.
            exists (str): Behavior if the target exists: 'append', 'replace', or 'error'.
            on_error (callable, optional): Error handler callback.
        """
        super().__init__(step_name=step_name, dataframes=dataframe, exists=exists, func=self.func, on_error=on_error)
        self.dataframe = dataframe
        self.target = target
        self.conn = engine
        self.schema = schema
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the load operation. Depending on 'exists', may drop and recreate the table,
        raise on conflict, or append. Inserts all rows of the DataFrame in a single batch.

        Args:
            context: Pypeline context containing dataframes.

        Returns:
            context: Updated pypeline context after loading.

        Raises:
            ValueError: If exists='error' and target table already exists.
        """
        df = context.get_dataframe(self.dataframe)
        full_name = f"[{self.schema}].[{self.target}]" if self.schema else f"[{self.target}]"

        if self.exists == "replace":
            self._drop_table_if_exists(full_name)
            self._create_table(full_name, df)
        elif self.exists == "error" and self._table_exists(full_name):
            raise ValueError(f"Target table {full_name} already exists")

        self._insert_rows(full_name, df)
        return context

    def _table_exists(self, full_name: str) -> bool:
        """
        Check if the target table exists in INFORMATION_SCHEMA.TABLES.

        Args:
            full_name (str): Qualified table name.

        Returns:
            bool: True if table exists, False otherwise.
        """
        schema, table = full_name.strip("[]").split("].[")
        sql = (
            "SELECT 1 FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?"
        )
        cursor = self.conn.cursor()
        cursor.execute(sql, schema, table)
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def _drop_table_if_exists(self, full_name: str):
        """
        Drop the target table if it exists.

        Args:
            full_name (str): Qualified table name.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"IF OBJECT_ID('{full_name}', 'U') IS NOT NULL DROP TABLE {full_name}")
        self.conn.commit()
        cursor.close()

    def _create_table(self, full_name: str, df: pd.DataFrame):
        """
        Create a new table with column definitions inferred from DataFrame dtypes.

        Args:
            full_name (str): Qualified table name.
            df (pd.DataFrame): DataFrame whose schema will be used.
        """
        cols = [f"[{col}] {self._map_dtype(dtype, df[col])}" for col, dtype in df.dtypes.items()]
        ddl = f"CREATE TABLE {full_name} ({', '.join(cols)})"
        cursor = self.conn.cursor()
        cursor.execute(ddl)
        self.conn.commit()
        cursor.close()

    def _map_dtype(self, dtype, series) -> str:
        """
        Map a pandas dtype to an appropriate SQL column type.

        Args:
            dtype: pandas dtype of the column.
            series (pd.Series): Column data for length inference.

        Returns:
            str: SQL datatype declaration.
        """
        if pd.api.types.is_integer_dtype(dtype):
            return "BIGINT"
        if pd.api.types.is_float_dtype(dtype):
            return "FLOAT"
        if pd.api.types.is_bool_dtype(dtype):
            return "BIT"
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return "DATETIME2"
        max_len = series.astype(str).str.len().max()
        return f"NVARCHAR({int(max_len)})" if max_len and max_len < 4000 else "NVARCHAR(MAX)"

    def _insert_rows(self, full_name: str, df: pd.DataFrame):
        """
        Insert DataFrame rows into the target table using executemany for performance.

        Args:
            full_name (str): Qualified table name.
            df (pd.DataFrame): DataFrame to insert.
        """
        cols = ", ".join(f"[{c}]" for c in df.columns)
        placeholders = ", ".join("?" for _ in df.columns)
        sql = f"INSERT INTO {full_name} ({cols}) VALUES ({placeholders})"
        data = df.values.tolist()

        cursor = self.conn.cursor()
        cursor.fast_executemany = True
        cursor.executemany(sql, data)
        self.conn.commit()
        cursor.close()
