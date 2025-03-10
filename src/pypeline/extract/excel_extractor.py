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
        super().__init__(step_name=step_name, func=self.func, chunk_size=chunk_size)
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
