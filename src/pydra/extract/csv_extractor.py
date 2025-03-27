"""
Module: csv_extractor

This module provides concrete implementations for extracting data from CSV files.
It defines two classes:
    - CSVExtractor: Extracts a DataFrame from a single CSV file.
    It supports both standard reading and chunked reading when a chunk_size is specified.
    - MultiCSVExtractor: Extracts DataFrames from multiple CSV files located in a directory.
Both classes extend from their respective base extractor classes and leverage pandas'
read_csv() functionality to read data.
Additionally, CSVExtractor provides a method to determine the maximum number of rows
in a CSV file, which is useful for chunking operations.
"""

import pandas as pd
from ..extract.file_extractor import FileExtractor, MultiFileExtractor

class CSVExtractor(FileExtractor):
    """
    CSVExtractor

    A concrete extractor for reading data from CSV files.
    This class extends FileExtractor and provides methods to read an entire CSV file or
    to read it in chunks when a chunk_size is specified. The extracted DataFrame is added
    to the context under the file name.
    """
    def __init__(self,
                 source,
                 step_name="CSVExtractor",
                 chunk_size=None,
                 on_error=None,
                 **kwargs):
        """
        CSVExtractor Class Constructor
        Initializes the CSVExtractor object.

        Arguments:
            source (str): 
                The source directory where the CSV file is located
            step_name (str): 
                The name of the step
            chunk_size (int): 
                The number of rows to read at a time
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the read_csv() method
        """
        super().__init__(source=source,
                         step_name=step_name,
                         func = self.func,
                         chunk_size=chunk_size,
                         on_error=on_error,
                         **kwargs)

    def func(self, context):
        """
        Public method: func()
        Reads the CSV file and adds the DataFrame to the context

        Arguments:
            context (Context): 
                Blank context object where the DataFrame will be added

        Returns:
            Context: 
                The context object with the DataFrame added
        """
        context.add_dataframe(self.file_name, self.__read_csv(self.file_path, self.kwargs))
        return context

    def __read_csv(self, file, kwargs):
        """
        Private method: __read_csv()
        Reads the CSV file

        Arguments:
            file (str): 
                The path to the CSV file
            kwargs (dict): 
                Additional keyword arguments for the read_csv() method

        Returns:
            DataFrame: 
                The DataFrame read from the CSV file
        """
        return pd.read_csv(file, **kwargs)

    def get_max_row_count(self):
        """
        Public method: get_max_row_count()
        Returns the maximum number of rows in the CSV file

        Returns:
            int: 
                The maximum number of rows in the CSV file
        """
        max_rows = 0
        with open(self.file_path, 'r', encoding="UTF-8") as f:
            row_count = sum(1 for row in f)
            max_rows = max(max_rows, row_count)
        return max_rows

class MultiCSVExtractor(MultiFileExtractor):
    """
    MultiCSVExtractor

    A concrete extractor for reading multiple CSV files from a specified source directory.
    This class extends MultiFileExtractor and leverages CSVExtractor to extract DataFrames
    from each CSV file found in the directory.
    """
    def __init__(self, source, chunk_size=None, on_error=None, **kwargs):
        """
        MultiCSVExtractor Class Constructor
        Initializes the MultiCSVExtractor object.

        Arguments:
            source (str): 
                The source directory where the CSV files are located
            chunk_size (int): 
                The number of rows to read at a time
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the CSVExtractor constructor
        """
        super().__init__(source=source,
                         step_name="MultiCSVExtractor",
                         type=CSVExtractor,
                         extension_type='csv',
                         chunk_size=chunk_size,
                         on_error=on_error,
                         **kwargs)
