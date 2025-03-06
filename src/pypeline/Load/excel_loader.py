"""
Module for loading pandas DataFrames to Excel files.

This module defines the ExcelLoader class, which extends the Loader base class.
ExcelLoader writes DataFrames from a given context to Excel files in a specified target
directory. The file write mode is determined by the 'exists' parameter.
"""

import os
from ..utils.utils import check_directory
from ..load.loader import Loader


class ExcelLoader(Loader):
    """
    Loader for writing pandas DataFrames to Excel files.

    The ExcelLoader extracts DataFrames from a context and writes each DataFrame to an
    Excel file. The file name is derived from the DataFrame key with a specified file extension.
    The write mode (append, fail, or replace) is determined by the 'exists' parameter.
    """

    def __init__(self, target, file_extension=".xlsx", step_name="ExcelLoader",
                 dataframes=[], exists="append", **kwargs):
        """
        Initialize an ExcelLoader instance.

        This method checks that the target directory exists and sets up the necessary parameters
        for writing Excel files.

        Args:
            target (str): The target directory where Excel files will be saved.
            file_extension (str, optional): The file extension for the output files. Defaults to ".xlsx".
            step_name (str, optional): The name of this loader step. Defaults to "excel_loader".
            dataframes (list, optional): A list or dictionary of DataFrames to load. Defaults to an empty list.
            exists (str, optional): Behavior when file already exists; must be 'append', 'fail', or 'replace'. Defaults to "append".
            **kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_excel.

        Raises:
            Exception: If the target directory is not found.
        """
        super().__init__(step_name=step_name, dataframes=dataframes, exists=exists, func=self.func)
        if not check_directory(target):  # or check if it's a file
            raise Exception("Error directory not found")
        
        self.target_dir = target
        self.kwargs = kwargs
        self.file_extension = file_extension

    def func(self, context):
        """
        Execute the Excel loading process.

        Iterates over the DataFrames in the provided context and writes each to an Excel file
        in the target directory. The file name is created by appending the specified file extension
        to the key name of the DataFrame.

        Args:
            context: The context containing DataFrames to be loaded.

        Returns:
            None
        """
        for key, df in context.dataframes.items():
            target_file_path = os.path.join(self.target_dir, key + self.file_extension)
            self.__to_excel(df, target_file_path, self.kwargs)
        return

    def __to_excel(self, df, target_file_path, kwargs):
        """
        Write a pandas DataFrame to an Excel file.

        Uses the pandas to_excel method to write the DataFrame to the target file path.
        The file mode is determined by the mapped value from the 'exists' parameter.

        Args:
            df (pd.DataFrame): The DataFrame to write.
            target_file_path (str): The full file path for the output Excel file.
            kwargs (dict): Additional keyword arguments for pandas.DataFrame.to_excel.
        """
        df.to_excel(target_file_path, mode=self.map_exists_parameter(), **kwargs)

    def map_exists_parameter(self):
        """
        Map the 'exists' parameter to the appropriate Excel file mode.

        Returns:
            str: The file mode for pandas.DataFrame.to_excel:
                 'a' for append, 'x' for fail (if file exists), or 'w' for replace.
        """
        if self.exists == "append":
            return 'a'
        elif self.exists == "fail":
            return 'x'
        elif self.exists == "replace":
            return 'w'
