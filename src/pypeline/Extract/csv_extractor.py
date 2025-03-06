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

    def __init__(self, source, step_name="CSVExtractor", **kwargs):
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
        super().__init__(step_name=step_name, func=self.func)
        if not check_directory(source):  # or check if it's a file
            raise Exception("Error directory not found")
        
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
