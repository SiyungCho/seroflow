"""
Module for loading pandas DataFrames into SQL Server tables.

This module defines the SQLServerLoader class, which extends the Loader base class.
SQLServerLoader writes DataFrames from a given context to SQL Server tables using a provided engine.
The behavior for existing tables is determined by the 'exists' parameter.
"""

from ..load.loader import Loader


class SQLServerLoader(Loader):
    """
    Loader for writing pandas DataFrames to SQL Server tables.

    SQLServerLoader extracts DataFrames from a context and writes each one to a SQL Server table.
    It supports specifying multiple target table names and uses a provided engine to connect to the database.
    The behavior when a table already exists is controlled by the 'exists' parameter.
    """

    def __init__(self, target, engine, step_name="SQLServerLoader", dataframes=[], exists="append", **kwargs):
        """
        Initialize a SQLServerLoader instance.

        Args:
            target (str or list): The target table name or list of table names where DataFrames will be loaded.
                                    If a single string is provided, it will be converted to a list.
            engine: The database engine instance used for connecting to SQL Server. It is assumed to have attributes
                    such as 'database', 'schema', and 'engine' (the underlying SQLAlchemy engine).
            step_name (str, optional): The name of this loader step. Defaults to "SQLServerLoader".
            dataframes (list or dict, optional): The DataFrames to load. Defaults to an empty list.
            exists (str, optional): Behavior when a table already exists; expected values are 'append', 'fail', or 'replace'.
                                    Defaults to "append".
            **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_sql.

        Note:
            No explicit type check is performed on the engine; it is assumed that a valid engine is provided.
        """
        super().__init__(step_name=step_name, dataframes=dataframes, exists=exists, func=self.func)
        self.target = [target] if not isinstance(target, list) else target
        self.engine = engine
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the SQL Server loading process.

        Iterates over the DataFrames in the provided context and writes each DataFrame to a SQL Server table.
        The target table names are taken from the self.target list, and the full schema is constructed using the engine's
        database and schema attributes.

        Args:
            context: The context object containing DataFrames to be loaded.

        Returns:
            None
        """
        for target, (key, df) in zip(self.target, context.dataframes.items()):
            full_schema = f"{self.engine.database}.{self.engine.schema}"
            self.__to_sql(df, target, full_schema, self.engine.engine, self.kwargs)
        return

    def __to_sql(self, df, target, schema, engine, kwargs):
        """
        Write a pandas DataFrame to a SQL Server table.

        Uses pandas.DataFrame.to_sql to write the DataFrame to the specified table in the given schema.
        The 'if_exists' parameter is set according to the mapped value from the 'exists' parameter.

        Args:
            df (pd.DataFrame): The DataFrame to write.
            target (str): The target table name.
            schema (str): The full schema (combination of database and schema) where the table resides.
            engine: The SQLAlchemy engine used for the database connection.
            kwargs (dict): Additional keyword arguments for pandas.DataFrame.to_sql.
        """
        df.to_sql(target, con=engine, if_exists=self.map_exists_parameter(), schema=schema, **kwargs)

    def map_exists_parameter(self):
        """
        Map the 'exists' parameter to the appropriate behavior for pandas.DataFrame.to_sql.

        Returns:
            str: The behavior for the 'if_exists' parameter in pandas.DataFrame.to_sql,
                 which is expected to be one of 'append', 'fail', or 'replace'.
        """
        return self.exists
