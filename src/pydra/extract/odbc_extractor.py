"""
Module: odbc_extractor.py

This module provides a concrete implementation for extracting data from any ODBC‑accessible
data source using raw SQL. It defines a single class:

    - ODBCExtractor: Extracts data from a table or view over a pyodbc.Connection,
      supporting both full-table reads and chunked reads via OFFSET/FETCH.

Each extraction returns a pandas DataFrame and integrates with the framework’s Extractor
interface for pipeline orchestration.
"""
import pandas as pd
from ..extract.extractor import Extractor

class ODBCExtractor(Extractor):
    """
    Extractor for ODBC‑accessible data sources. Uses a pyodbc.Connection to execute SQL queries
    and returns pandas DataFrames. Supports full-table extraction or chunked extraction via
    OFFSET/FETCH for batching large tables.

    Arguments:
        source (str): Name of the table or view to read.
        engine (pyodbc.Connection): An open ODBC connection.
        schema (str): Database schema (or owner) for qualifying the source.
        step_name (str, optional): Identifier for this extraction step (default: "ODBCExtractor").
        chunk_size (int, optional): Number of rows per chunk when using batch extraction.
        on_error (callable, optional): Callback invoked on extraction errors.
        **kwargs: Additional keyword arguments controlling extraction:
            - skiprows (int): Number of rows to skip (for chunked reads).
            - nrows (int): Number of rows to fetch (for chunked reads).
            - order_by (str): Column name to order by (defaults to first column if omitted).

    Raises:
        ValueError: If schema is not provided.

    """
    def __init__(
        self,
        source,
        engine,
        schema,
        step_name="ODBCExtractor",
        chunk_size=None,
        on_error=None,
        **kwargs
    ):
        if not schema:
            raise ValueError("Schema must be provided for ODBCExtractor")
        super().__init__(step_name=step_name,
                         func=self.func,
                         chunk_size=chunk_size,
                         on_error=on_error)
        self.source = source
        self.conn = engine
        self.schema = schema
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the extraction. Chooses between full or chunked reads based on presence
        of 'skiprows' and 'nrows' in kwargs, then adds the resulting DataFrame to context.

        Returns:
            context with the extracted DataFrame under self.source.
        """
        if "skiprows" in self.kwargs and "nrows" in self.kwargs:
            skip = self.kwargs.pop("skiprows")
            nrows = self.kwargs.pop("nrows")
            df = self._read_chunk(skip, nrows)
        else:
            df = self._read_full()
        context.add_dataframe(self.source, df)
        return context

    def _qualified_name(self):
        """Return the fully qualified object name including schema."""
        return f"{self.schema}.{self.source}"

    def _read_full(self):
        """
        Read the entire table or view into a DataFrame.

        Returns:
            pandas.DataFrame of all rows and columns.
        """
        query = f"SELECT * FROM {self._qualified_name()}"
        return pd.read_sql_query(query, con=self.conn)

    def _read_chunk(self, skip, nrows):
        """
        Read a subset of rows using OFFSET/FETCH for batching.

        Arguments:
            skip (int): Number of rows to skip (OFFSET).
            nrows (int): Number of rows to fetch.

        Returns:
            pandas.DataFrame containing the specified slice of data.
        """
        order_by = self.kwargs.pop("order_by", None) or self._default_order_by()
        query = (
            f"SELECT * FROM {self._qualified_name()} "
            f"ORDER BY {order_by} "
            f"OFFSET {skip} ROWS FETCH NEXT {nrows} ROWS ONLY"
        )
        return pd.read_sql_query(query, con=self.conn)

    def _default_order_by(self):
        """
        Infer a default ORDER BY column by selecting a single row and using first column name.

        Returns:
            str: Name of the first column in the result set.
        """
        query = f"SELECT TOP 1 * FROM {self._qualified_name()}"
        df = pd.read_sql_query(query, con=self.conn)
        return df.columns[0]

    def get_max_row_count(self):
        """
        Retrieve the total number of rows in the source without loading full data.

        Returns:
            int: Total row count.
        """
        query = f"SELECT COUNT(*) AS count FROM {self._qualified_name()}"
        df = pd.read_sql_query(query, con=self.conn)
        return int(df.at[0, "count"])
