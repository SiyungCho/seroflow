"""
"""

import pandas as pd
from ..extract.file_extractor import FileExtractor, MultiFileExtractor

class CSVExtractor(FileExtractor):
    """
    """
    def __init__(self, source, step_name="CSVExtractor", chunk_size=None, **kwargs):
        """
        """
        super().__init__(source=source, step_name=step_name, func = self.func if chunk_size is None else self.chunk_func, chunk_size=chunk_size, **kwargs)

    def func(self, context):
        """
        """
        context.add_dataframe(self.file_name, self.__read_csv(self.file_path, self.kwargs))
        return context

    def chunk_func(self, context, chunk_coordinates):
        """
        """
        context.add_dataframe(self.file_name, self.__read_csv_chunk(self.file_path, chunk_coordinates, self.kwargs))
        return context     

    def __read_csv(self, file, kwargs):
        """
        """
        return pd.read_csv(file, **kwargs)

    def __read_csv_chunk(self, file, chunk_coordinates, kwargs):
        """
        """
        start_idx, stop_idx = chunk_coordinates
        if start_idx is None:
            return pd.DataFrame()
        
        nrows = stop_idx - start_idx
        return pd.read_csv(file, skiprows=start_idx, nrows=nrows, **kwargs)

    def get_max_row_count(self):
        """
        """
        max_rows = 0
        with open(self.file_path, 'r') as f:
            row_count = sum(1 for row in f)
            if row_count > max_rows:
                max_rows = row_count
        return max_rows

class MultiCSVExtractor(MultiFileExtractor):
    """
    """
    def __init__(self, source, chunk_size=None, **kwargs):
        """
        """
        super().__init__(source=source, step_name="MultiCSVExtractor", type=CSVExtractor, extension_type='csv', chunk_size=chunk_size, **kwargs)
