"""
Module for extracting Excel files and loading them into a context as pandas DataFrames.

This module defines the ExcelExtractor class, which extends the Extractor base class.
It scans a specified source directory for Excel files (.xlsx and .xls), reads each file into
a pandas DataFrame using the appropriate engine, and adds the DataFrame to a provided context.
"""

import pandas as pd
from ..utils.utils import check_directory, gather_files, remove_extension
from ..extract.extractor import Extractor


class ExcelExtractor(Extractor):
    """
    A specialized extractor for Excel files.

    The ExcelExtractor class searches a given source directory for Excel files (.xlsx and .xls),
    reads each file into a pandas DataFrame using the appropriate engine, and adds the DataFrame
    to a context with a key based on the file name.
    """

    def __init__(self, source, step_name="ExcelExtractor", chunk_size = None, **kwargs):
        """
        Initialize an ExcelExtractor instance.

        This method verifies that the source directory exists, gathers the file paths and names
        for Excel files in the directory, stores any additional keyword arguments for Excel files.

        Args:
            source (str): The directory path where Excel files are located.
            step_name (str, optional): 
                The name of the extraction step. Defaults to "ExcelExtractor".
            **kwargs: Additional keyword arguments to pass to pandas.read_excel.

        Raises:
            Exception: If the specified source directory is not found.
        """
        super().__init__(step_name=step_name, func = self.func if chunk_size is None else self.chunk_func, chunk_size=chunk_size)
        if not check_directory(source):  # or check if it's a file
            raise FileNotFoundError("Error directory not found")

        self.source = source
        self.file_paths, self.file_names = gather_files(self.source, ["xlsx", "xls"])
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the Excel extraction process.

        Iterates over the gathered Excel files, reads each file into a pandas DataFrame,
        and adds the DataFrame to the provided context with a key derived from the file name
        (with the file extension removed).

        Args:
            context: The context object where DataFrames are stored.

        Returns:
            The updated context object with the added DataFrames.
        """
        for name, file in zip(self.file_names, self.file_paths):
            context.add_dataframe(remove_extension(name), self.__read_excel(file, self.kwargs))
        return context
    
    def chunk_func(self, context, chunk_coordinates):
        for name, file in zip(self.file_names, self.file_paths):
            context.add_dataframe(remove_extension(name), self.__read_excel_chunk(file, chunk_coordinates, self.kwargs))
        return context 

    def __read_excel(self, file, kwargs):
        """
        Read an Excel file into a pandas DataFrame.

        Uses the appropriate engine based on the file extension:
          - For '.xls' files, uses the 'xlrd' engine.
          - For '.xlsx' files, uses the 'openpyxl' engine.

        Args:
            file (str): The file path to the Excel file.
            kwargs (dict): Additional keyword arguments to pass to pandas.read_excel.

        Returns:
            pd.DataFrame: The DataFrame containing the data from the Excel file.

        Raises:
            ValueError: If the file format is unsupported.
        """
        if file.endswith('.xls'):
            return pd.read_excel(file, engine='xlrd', **kwargs)
        if file.endswith('.xlsx'):
            return pd.read_excel(file, engine='openpyxl', **kwargs)
        raise ValueError(f"Unsupported file format: {file}")
    
    def __read_excel_chunk(self, file, chunk_coordinates, kwargs):
        start_idx, stop_idx = chunk_coordinates
        print("excel coords:")
        print(start_idx)
        print(stop_idx)
        if start_idx is None:
            return pd.DataFrame()

        # Determine how many rows to read for this chunk.
        nrows = stop_idx - start_idx
        # Make a copy of kwargs so we don't modify the original dictionary.
        # kwargs = kwargs.copy()

        # Select the engine based on the file extension.
        if file.endswith('.xls'):
            engine = 'xlrd'
        elif file.endswith('.xlsx'):
            engine = 'openpyxl'
        else:
            raise ValueError(f"Unsupported file format: {file}")
        
        nrows = stop_idx - start_idx
        return pd.read_excel(file, skiprows=start_idx, nrows=nrows, engine=engine, **kwargs)

        # # Check if a header is present.
        # header = kwargs.get("header", 0)
        # if header is not None:
        #     # Read the header separately to capture column names.
        #     df_header = pd.read_excel(file, nrows=0, engine=engine, **kwargs)
        #     # When reading the chunk, skip rows from 1 to start_idx (since row 0 is the header).
        #     skiprows = list(range(1, start_idx + 1))
        #     # Read the chunk with header=None so that the header row is not re-read.
        #     df_chunk = pd.read_excel(file, skiprows=skiprows, nrows=nrows, header=None, engine=engine, **kwargs)
        #     df_chunk.columns = df_header.columns
        #     return df_chunk
        # else:
        #     # If no header is present, directly skip the first start_idx rows.
        #     return pd.read_excel(file, skiprows=start_idx, nrows=nrows, engine=engine, **kwargs)
    
    def get_max_row_count(self):
        """
        Determine the maximum number of rows across all Excel files in the source directory
        without reading the entire data.

        For '.xlsx' files, uses openpyxl in read-only mode to quickly access the worksheet's
        max_row property. For '.xls' files, uses xlrd to open the workbook on-demand and retrieves
        the row count from the first sheet.

        Returns:
            int: The maximum row count found among all Excel files.
        """
        max_rows = 0
        for file in self.file_paths:
            if file.endswith('.xlsx'):
                from openpyxl import load_workbook
                # Open the workbook in read-only mode to avoid loading the full file into memory.
                wb = load_workbook(filename=file, read_only=True)
                ws = wb.active  # use the first (active) sheet
                rows_count = ws.max_row
                wb.close()
            elif file.endswith('.xls'):
                import xlrd
                # Open the workbook with on_demand to avoid reading all data.
                wb = xlrd.open_workbook(file, on_demand=True)
                ws = wb.sheet_by_index(0)
                rows_count = ws.nrows
                wb.release_resources()
            else:
                raise ValueError(f"Unsupported file format: {file}")
            
            max_rows = max(max_rows, rows_count)
        
        return max_rows
