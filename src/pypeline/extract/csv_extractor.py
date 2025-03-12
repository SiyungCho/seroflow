"""
Module for extracting CSV files and loading them into a context as pandas DataFrames.

This module defines the CSVExtractor class, which extends the Extractor base class.
It gathers CSV files from a specified source directory, reads them into DataFrames,
and adds them to a provided context.
"""

import pandas as pd
from ..utils.utils import check_directory, gather_files, remove_extension
from ..extract.extractor import Extractor


class CSVExtractor(Extractor):
    """
    A specialized extractor for CSV files.

    The CSVExtractor class scans a specified source directory for CSV files,
    reads each file into a pandas DataFrame, and adds the DataFrame to a context
    using a key derived from the file name.
    """

    def __init__(self, source, step_name="CSVExtractor", chunk_size=None, **kwargs):
        """
        Initialize a CSVExtractor instance.

        This method validates the source directory, gathers CSV file paths and names,
        and stores additional keyword arguments for reading CSV files.

        Args:
            source (str): The directory path where CSV files are located.
            step_name (str, optional): The name of the extraction step. Defaults to "CSVExtractor".
            **kwargs: Additional keyword arguments to pass to the pandas read_csv function.

        Raises:
            Exception: If the source directory is not found.
        """
        super().__init__(step_name=step_name, func = self.func if chunk_size is None else self.chunk_func, chunk_size=chunk_size)
        if not check_directory(source):  # or check if it's a file
            raise FileNotFoundError("Error directory not found")

        self.source = source
        self.file_paths, self.file_names = gather_files(self.source, ["csv"])
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the CSV extraction process.

        Iterates over the gathered CSV files, reads each file into a DataFrame,
        and adds the DataFrame to the provided context with a key based on the file name.

        Args:
            context: The context object where DataFrames are stored.

        Returns:
            The updated context object with added DataFrames.
        """
        for name, file in zip(self.file_names, self.file_paths):
            context.add_dataframe(remove_extension(name), self.__read_csv(file, self.kwargs))
        return context

    def chunk_func(self, context, chunk_coordinates):
        for name, file in zip(self.file_names, self.file_paths):
            context.add_dataframe(remove_extension(name), self.__read_csv_chunk(file, chunk_coordinates, self.kwargs))
        return context     

    def __read_csv(self, file, kwargs):
        """
        Read a CSV file into a pandas DataFrame.

        This private helper method uses pandas.read_csv to load the CSV file,
        applying any additional keyword arguments provided.

        Args:
            file (str): The file path to the CSV file.
            kwargs (dict): Additional keyword arguments for pandas.read_csv.

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.
        """
        return pd.read_csv(file, **kwargs)
    
    def __read_csv_chunk(self, file, chunk_coordinates, kwargs):
        start_idx, stop_idx = chunk_coordinates
        print("csv coords:")
        print(start_idx)
        print(stop_idx)
        if start_idx is None:
            return pd.DataFrame()
        
        # Calculate how many rows to read.
        nrows = stop_idx - start_idx
        return pd.read_csv(file, skiprows=start_idx, nrows=nrows, **kwargs)
        # # Make a copy of kwargs so we don't modify the caller's dictionary.
        # kwargs = kwargs.copy()
        
        # # Determine if a header is present. If header is not None, assume the first row is a header.
        # header = kwargs.get("header", "infer")
        
        # if header is not None:
        #     # First, read the header row only to capture column names.
        #     df_header = pd.read_csv(file, nrows=0, **kwargs)
        #     # When reading the data chunk, we want to preserve the header row,
        #     # so we skip rows from 1 up to (and including) start_idx.
        #     # This is because pd.read_csv treats the first row (row index 0) as the header.
        #     skiprows = list(range(1, start_idx + 1))
        #     # Read the chunk with header=None (since we already have column names).
        #     df_chunk = pd.read_csv(file, skiprows=skiprows, nrows=nrows, header=None, **kwargs)
        #     # Reassign the header.
        #     df_chunk.columns = df_header.columns
        #     return df_chunk
        # else:
        #     # If no header is present, simply skip the first `start_idx` rows.
        #     return pd.read_csv(file, skiprows=start_idx, nrows=nrows, **kwargs)
    
    def get_max_row_count(self):
        """
        Out of all the files to be extracted we gather the largest number of rows. without actually reading the files.

        Returns:
            int: The largest number of rows extracted.
        """
        
        max_rows = 0
        for file in self.file_paths:
            with open(file, 'r') as f:
                row_count = sum(1 for row in f)
                if row_count > max_rows:
                    max_rows = row_count
        return max_rows
