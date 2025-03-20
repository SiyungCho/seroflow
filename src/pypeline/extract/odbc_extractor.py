"""
Module: 
"""
import pandas as pd
from ..extract.extractor import Extractor

class ODBCExtractor(Extractor):
    """
    General ODBC extractor using a pyodbc.Connection and raw SQL.
    """

    def __init__(
        self,
        source,
        engine,
        schema,
        step_name: str = "ODBCExtractor",
        chunk_size: int = None,
        on_error=None,
        **kwargs
    ):
        super().__init__(step_name=step_name, func=self.func, chunk_size=chunk_size, on_error=on_error)
        self.source = source
        self.conn = engine
        self.schema = schema
        self.kwargs = kwargs

    def func(self, context):
        if "skiprows" in self.kwargs and "nrows" in self.kwargs:
            skip = self.kwargs.pop("skiprows")
            nrows = self.kwargs.pop("nrows")
            df = self._read_chunk(skip, nrows)
        else:
            df = self._read_full()
        context.add_dataframe(self.source, df)
        return context

    def _qualified_name(self) -> str:
        return f"{self.schema}.{self.source}" if self.schema else self.source

    def _read_full(self) -> pd.DataFrame:
        query = f"SELECT * FROM {self._qualified_name()}"
        return pd.read_sql_query(query, con=self.conn)

    def _read_chunk(self, skip: int, nrows: int) -> pd.DataFrame:
        order_by = self.kwargs.pop("order_by", None) or self._default_order_by()
        query = (
            f"SELECT * FROM {self._qualified_name()} "
            f"ORDER BY {order_by} "
            f"OFFSET {skip} ROWS FETCH NEXT {nrows} ROWS ONLY"
        )
        return pd.read_sql_query(query, con=self.conn)

    def _default_order_by(self) -> str:
        # pull back a single row to infer the first column name
        query = f"SELECT TOP 1 * FROM {self._qualified_name()}"
        df = pd.read_sql_query(query, con=self.conn)
        return df.columns[0]

    def get_max_row_count(self) -> int:
        query = f"SELECT COUNT(*) AS count FROM {self._qualified_name()}"
        df = pd.read_sql_query(query, con=self.conn)
        return int(df.at[0, "count"])
