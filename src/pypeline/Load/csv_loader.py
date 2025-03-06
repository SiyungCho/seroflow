"""
Module for loading pandas DataFrames to CSV files.

This module defines the CSVLoader class, which extends the Loader base class.
CSVLoader writes DataFrames from a given context to CSV files in a specified target
directory. The file write mode is determined by the 'exists' parameter.
"""

import os
from ..utils.utils import check_directory
from ..load.loader import Loader


class CSVLoader(Loader):
    """
    Loader for writing pandas DataFrames to CSV files.

    The CSVLoader extracts DataFrames from a context and writes each DataFrame to a CSV file
    in the target directory. The file name is derived from the DataFrame key with a ".csv"
    extension. The file write mode (append, fail, or replace) is determined by the 'exists'
    parameter.
    """

    def __init__(self, target, step_name="CSVLoader", dataframes=[], exists="append", **kwargs):
        """
        Initialize a CSVLoader instance.

        This method verifies that the target directory exists and sets up the necessary parameters
        for writing CSV files.

        Args:
            target (str): The target directory where CSV files will be saved.
            step_name (str, optional): The name of this loader step. Defaults to "CSVLoader".
            dataframes (list or dict, optional): The DataFrames to load. Defaults to an empty list.
            exists (str, optional): Behavior when a file already exists; must be 'append', 'fail', or 'replace'.
                                    Defaults to "append".
            **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv.

        Raises:
            Exception: If the target directory is not found.
        """
        super().__init__(step_name=step_name, dataframes=dataframes, exists=exists, func=self.func)
        if not check_directory(target):  # or check if it's a file
            raise Exception("Error directory not found")

        self.target_dir = target
        self.kwargs = kwargs

    def func(self, context):
        """
        Execute the CSV loading process.

        Iterates over the DataFrames in the provided context and writes each to a CSV file in the target directory.
        The file name is created by appending ".csv" to the DataFrame's key.

        Args:
            context: The context object containing DataFrames to be loaded.

        Returns:
            None
        """
        for key, df in context.dataframes.items():
            target_file_path = os.path.join(self.target_dir, key + ".csv")
            self.__to_csv(df, target_file_path, self.kwargs)
        return

    def __to_csv(self, df, target_file_path, kwargs):
        """
        Write a pandas DataFrame to a CSV file.

        Uses pandas.DataFrame.to_csv to write the DataFrame to the specified file path.
        The file mode is determined by the mapped value from the 'exists' parameter.

        Args:
            df (pd.DataFrame): The DataFrame to write.
            target_file_path (str): The full file path for the output CSV file.
            kwargs (dict): Additional keyword arguments for pandas.DataFrame.to_csv.
        """
        df.to_csv(target_file_path, mode=self.map_exists_parameter(), **kwargs)

    def map_exists_parameter(self):
        """
        Map the 'exists' parameter to the appropriate CSV file mode.

        Returns:
            str: The file mode for pandas.DataFrame.to_csv:
                 'a' for append, 'x' for fail (if file exists), or 'w' for replace.
        """
        if self.exists == "append":
            return 'a'
        elif self.exists == "fail":
            return 'x'
        elif self.exists == "replace":
            return 'w'
