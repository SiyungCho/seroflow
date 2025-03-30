"""
Module: csv_loader

This module provides implementations for writing DataFrames to CSV files.
It defines two loader classes:
    - CSVLoader: Writes a single DataFrame to a CSV file.
    - MultiCSVLoader: Handles writing multiple DataFrames to CSV files.
These classes extend the FileLoader class and implement CSV-specific functionality.
"""
import os
from .file_loader import FileLoader

class CSVLoader(FileLoader):
    """
    CSVLoader

    A concrete loader for writing a DataFrame to a CSV file.
    This class extends FileLoader and provides methods to convert DataFrames into CSV format,
    determine the target file path, and handle file modes to the specified existence parameter.
    """

    def __init__(self,
                 target,
                 dataframe,
                 exists="append",
                 step_name="CSVLoader",
                 on_error=None,
                 **kwargs):
        """
        CSVLoader Class Constructor
        Initializes the CSVLoader object.

        Arguments:
            target (str): 
                The target directory where the CSV file will be written
            dataframe (DataFrame): 
                The DataFrame to be written to the CSV file
            exists (str): 
                The file mode to use when writing the CSV file
            step_name (str): 
                The name of the step
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the to_csv() method
        """
        super().__init__(target=target,
                         dataframe=dataframe,
                         exists=exists,
                         func=self.func,
                         file_extension=".csv",
                         step_name=step_name,
                         on_error=on_error,
                         **kwargs)

    def func(self, context):
        """
        Public method: func()
        Reads the DataFrame from the context and writes it to a CSV file

        Arguments:
            context (Context): 
                The context object containing the dataframes to be written to the CSV file
        """
        for key, df in context.dataframes.items():
            if self.target_file_path is None:
                file_path = key + self.file_extension
                target_file_path = os.path.join(self.target, file_path)
            else:
                target_file_path = self.target_file_path
            self.__to_csv(df, target_file_path, self.kwargs)

    def __to_csv(self, df, target_file_path, kwargs):
        """
        Private method: __to_csv()
        Writes the DataFrame to a CSV file

        Arguments:
            df (DataFrame): 
                The DataFrame to be written to the CSV file
            target_file_path (str): 
                The path to the target CSV file
            kwargs (dict): 
                Additional keyword arguments for the to_csv() method
        """
        df.to_csv(target_file_path, mode=self.map_exists_parameter(), **kwargs)

    def map_exists_parameter(self):
        """
        Public method: map_exists_parameter()
        Maps the exists parameter to the appropriate file mode

        Returns:
            str (['a', 'x', 'w'], None): 
                'a': append mode
                'x': fail if exists
                'w': replace mode
                None: if the exists parameter is not recognized
        """
        if self.exists == "append":
            return 'a'
        if self.exists == "fail":
            return 'x'
        if self.exists == "replace":
            return 'w'
        return None

class MultiCSVLoader(CSVLoader):
    """
    MultiCSVLoader

    A concrete loader for writing multiple DataFrames to CSV files.
    This class extends CSVLoader and provides methods to write multiple DataFrames
    to CSV files in the specified target directory.
    """
    def __init__(self,
                 target,
                 dataframes=None,
                 exists="append",
                 step_name="MultiCSVLoader",
                 on_error=None,
                 **kwargs):
        """
        MultiCSVLoader Class Constructor
        Initializes the MultiCSVLoader object.

        Arguments:
            target (str): 
                The target directory where the CSV files will be written
            dataframes (dict): 
                A dictionary mapping DataFrame keys to DataFrames
            exists (str): 
                The file mode to use when writing the CSV files
            step_name (str): 
                The name of the step
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the to_csv() method
        """
        super().__init__(target=target,
                         dataframe=dataframes,
                         exists=exists,
                         step_name=step_name,
                         on_error=on_error,
                         **kwargs)
