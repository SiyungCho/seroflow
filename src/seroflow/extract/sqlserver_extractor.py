"""
Module: sqlserver_extractor.py

This module provides concrete implementations for extracting data from SQL server tables.
It defines two classes:
    - SQLServerExtractor: Extracts a DataFrame from a single SQL server table, supporting
      both full table reads and chunked reads.
These classes extend from the base extractor classes and leverage pandas along sqlalchemy
engines to read data.
"""
import pandas as pd
from sqlalchemy import MetaData, Table
from .extractor import Extractor

class SQLServerExtractor(Extractor):
    """
    Extractor for SQL Server databases. Connects to a SQL Server engine,
    reads tables into pandas DataFrames, and retrieves metadata such as row counts.
    """

    def __init__(self,
                 source,
                 engine,
                 schema=None,
                 step_name="SQLServerExtractor",
                 chunk_size=None,
                 on_error=None,
                 **kwargs):
        """
        Initialize the SQLServerExtractor.

        Arguments:
            source (str): Table name to extract data from.
            engine: An object containing the database engine attributes.
            schema (str, optional): Database schema where the table resides.
            step_name (str): Name of the extraction step.
            chunk_size (int, optional): Number of rows per chunk for chunked extraction
            (not used when skiprows/nrows are provided).
            on_error (callable, optional): Error handling strategy.
            **kwargs: Additional keyword arguments for the SQL query. When using chunking,
                      'skiprows' and 'nrows' are used. Optionally, 'order_by' can be provided.
        """
        super().__init__(step_name=step_name,
                         func=self.func,
                         chunk_size=chunk_size,
                         on_error=on_error)
        self.source = source
        self.engine = engine
        self.kwargs = kwargs
        self.schema = schema if not hasattr(engine, "schema") else engine.schema
        if not self.schema:
            raise ValueError("Schema must be provided for SQLServerExtractor")

    def func(self, context):
        """
        Execute the extraction function.

        If both 'skiprows' and 'nrows' are provided in kwargs, only the specified chunk
        of rows is retrieved using an OFFSET/FETCH query. Otherwise, the full table is read.

        Arguments:
            context: An object that holds the data and state throughout the extraction process.

        Returns:
            Updated context with the added DataFrame.
        """
        if "skiprows" in self.kwargs and "nrows" in self.kwargs:
            skiprows = self.kwargs.pop("skiprows")
            nrows = self.kwargs.pop("nrows")
            df = self.__read_sqlserver_table_chunk(
                self.source,
                self.schema,
                self.engine.engine,
                skiprows,
                nrows,
                self.kwargs
            )
        else:
            df = self.__read_sqlserver_table(
                self.source,
                self.schema,
                self.engine.engine,
                self.kwargs
            )
        context.add_dataframe(self.source, df)
        return context

    def __read_sqlserver_table(self, table_name, schema, engine, kwargs):
        """
        Read an entire SQL Server table into a pandas DataFrame.

        Arguments:
            table_name (str): Name of the table to read.
            schema (str): Database schema where the table resides.
            engine: Database engine used to establish a connection.
            kwargs: Additional keyword arguments for pd.read_sql_table.

        Returns:
            DataFrame containing the table data.
        """
        return pd.read_sql_table(table_name, schema=schema, con=engine.connect(), **kwargs)

    def __read_sqlserver_table_chunk(self, table_name, schema, engine, skiprows, nrows, kwargs):
        """
        Read a chunk of a SQL Server table into a pandas DataFrame using OFFSET/FETCH.

        Constructs a SQL query to return only a subset of rows based on the provided
        skiprows and nrows parameters. 'order_by' clause attempts to default to the
        primary key or the first column of the table.

        Arguments:
            table_name (str): Name of the table to read.
            schema (str): Database schema where the table resides.
            engine: Database engine used to establish a connection.
            skiprows (int): Number of rows to skip (offset).
            nrows (int): Number of rows to fetch.
            kwargs: Additional keyword arguments;

        Returns:
            DataFrame containing the specified chunk of table data.
        """
        full_table_name = f"{schema}.{table_name}" if schema else table_name
        order_by = self.__get_default_order_by(table_name, schema, engine)
        query = (f"SELECT * FROM {full_table_name} "
                 f"ORDER BY {order_by} "
                 f"OFFSET {skiprows} ROWS FETCH NEXT {nrows} ROWS ONLY")
        return pd.read_sql_query(query, con=engine.connect())

    def __get_default_order_by(self, table_name, schema, engine):
        """
        Determine a default ORDER BY column using the table's primary key or first column.

        Reflects the table using SQLAlchemy. If the table has a primary key, returns the
        name of the first primary key column. Otherwise, returns the name of the first column.

        Arguments:
            table_name (str): Name of the table.
            schema (str): Schema of the table.
            engine: Database engine used to establish a connection.

        Returns:
            str: Column name to be used in the ORDER BY clause.
        """
        metadata = MetaData(schema=schema)
        table = Table(table_name, metadata, autoload_with=engine)
        pk = list(table.primary_key.columns)
        if pk:
            return pk[0].name
        return list(table.columns)[0].name

    def get_max_row_count(self):
        """
        Retrieve the maximum number of rows in the SQL Server table without loading entire table.

        Returns:
            int: Total row count in the table.
        """
        with self.engine.engine.connect() as conn:
            full_table_name = f"{self.schema}.{self.source}" if self.schema else self.source
            query = f"SELECT COUNT(*) as count FROM {full_table_name}"
            result = conn.execute(query)
            row_count = result.scalar()
        return row_count
