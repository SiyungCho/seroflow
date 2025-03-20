# Module: odbc_loader.py

import pandas as pd
from ..load.loader import Loader

class ODBCLoader(Loader):
    """
    """

    def __init__(
        self,
        target: str,
        connection,
        dataframe: pd.DataFrame,
        schema: str = None,
        step_name: str = "ODBCLoader",
        exists: str = "append",
        chunk_size: int = None,
        batch_size: int = 1000,
        on_error=None
    ):
        super().__init__(step_name=step_name, dataframes=dataframe, exists=exists, func=self.func, on_error=on_error)
        self.target = target
        self.conn = connection
        self.schema = schema
        self.chunk_size = chunk_size or len(dataframe)
        self.batch_size = batch_size

    def func(self, context):
        df = context.dataframes[self.target]
        full_name = f"[{self.schema}].[{self.target}]" if self.schema else f"[{self.target}]"

        if self.exists == "replace":
            self._drop_table_if_exists(full_name)
            self._create_table(full_name, df)
        elif self.exists == "error" and self._table_exists(full_name):
            raise ValueError(f"Target table {full_name} already exists")

        # Insert in chunks
        for start in range(0, len(df), self.chunk_size):
            chunk = df.iloc[start : start + self.chunk_size]
            self._insert_rows(full_name, chunk)

        return context

    def _table_exists(self, full_name: str) -> bool:
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
        cursor = self.conn.cursor()
        cursor.execute(f"IF OBJECT_ID('{full_name}', 'U') IS NOT NULL DROP TABLE {full_name}")
        self.conn.commit()
        cursor.close()

    def _create_table(self, full_name: str, df: pd.DataFrame):
        cols = []
        for col, dtype in df.dtypes.items():
            sql_type = self._map_dtype(dtype, df[col])
            cols.append(f"[{col}] {sql_type}")
        ddl = f"CREATE TABLE {full_name} ({', '.join(cols)})"
        cursor = self.conn.cursor()
        cursor.execute(ddl)
        self.conn.commit()
        cursor.close()

    def _map_dtype(self, dtype, series) -> str:
        if pd.api.types.is_integer_dtype(dtype):
            return "BIGINT"
        if pd.api.types.is_float_dtype(dtype):
            return "FLOAT"
        if pd.api.types.is_bool_dtype(dtype):
            return "BIT"
        if pd.api.types.is_datetime64_any_dtype(dtype):
            return "DATETIME2"
        # default to NVARCHAR(max), sizing to longest value if < 4000
        max_len = series.astype(str).str.len().max()
        if max_len and max_len < 4000:
            return f"NVARCHAR({int(max_len)})"
        return "NVARCHAR(MAX)"

    def _insert_rows(self, full_name: str, df: pd.DataFrame):
        cols = ", ".join(f"[{c}]" for c in df.columns)
        placeholders = ", ".join("?" for _ in df.columns)
        sql = f"INSERT INTO {full_name} ({cols}) VALUES ({placeholders})"
        data = df.values.tolist()

        cursor = self.conn.cursor()
        cursor.fast_executemany = True
        for i in range(0, len(data), self.batch_size):
            batch = data[i : i + self.batch_size]
            cursor.executemany(sql, batch)
            self.conn.commit()
        cursor.close()
