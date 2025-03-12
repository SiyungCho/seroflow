"""
Module for extracting SQL Server tables and loading them into a context as pandas DataFrames.

This module defines the SQLServerExtractor class, which extends the Extractor base class.
It retrieves tables from a SQL Server database using a provided engine and adds them to a context.
"""

import pandas as pd
from ..extract.extractor import Extractor


class SQLServerExtractor(Extractor):
    """
    An extractor for SQL Server tables.

    The SQLServerExtractor class retrieves data from SQL Server tables using a given
    database engine and loads the data as pandas DataFrames into a context.
    """

    def __init__(self, source, engine, step_name="SQLServerExtractor", chunk_size=None, **kwargs):
        """
        Initialize an SQLServerExtractor instance.

        Args:
            source (str or list): A table name or a list of table names to extract.
            engine: The database engine instance used for connection and table verification.
                    It is assumed to have methods like `table_exists` and attributes such as
                    `schema` and `engine` (the latter being an SQLAlchemy engine instance).
            step_name (str, optional): 
                The name of the extraction step. Defaults to "SQLServerExtractor".
            **kwargs: Additional keyword arguments to pass to pandas.read_sql_table.
        
        Note:
            This initializer does not enforce a type check on the engine; it is expected
            that the engine provided is valid.
        """
        super().__init__(step_name=step_name, func=self.func, chunk_size=chunk_size)
        # Optionally, validate that engine is a proper engine instance here.
        self.source = [source] if not isinstance(source, list) else source
        self.engine = engine
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the SQL Server extraction process.

        Iterates over the list of table names, checks if each table exists using the engine,
        reads the table into a pandas DataFrame, and adds it to the provided context.

        Args:
            context: The context object to which the DataFrames will be added.

        Returns:
            The updated context object containing the added DataFrames.
        """
        for table_name in self.source:
            if not self.engine.table_exists(table_name):
                # If the table does not exist, skip to the next table.
                continue
            context.add_dataframe(
                table_name,
                self.__read_sqlserver_table(
                    table_name, self.engine.schema, self.engine.engine, self.kwargs
                )
            )
        return context
    
    def chunk_func(self, context, chunk_coordinates):
        return

    def __read_sqlserver_table(self, table_name, schema, engine, kwargs):
        """
        Read a SQL Server table into a pandas DataFrame.

        This private helper method connects to the database using the provided engine,
        reads the specified table with the given schema using pandas.read_sql_table, and
        returns the resulting DataFrame.

        Args:
            table_name (str): The name of the table to read.
            schema (str): The schema in which the table resides.
            engine: The SQLAlchemy engine instance used for the database connection.
            kwargs (dict): Additional keyword arguments to pass to pandas.read_sql_table.

        Returns:
            pd.DataFrame: A DataFrame containing the data from the specified SQL Server table.
        """
        return pd.read_sql_table(table_name, schema=schema, con=engine.connect(), **kwargs)
