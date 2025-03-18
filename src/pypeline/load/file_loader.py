"""
Module: file_loader

This module defines the FileLoader class, a concrete loader for writing DataFrames to files. The FileLoader class
extends the base Loader class and provides functionality to determine the target file path, handle file modes
according to the specified existence parameter, and define the file extension for the target file. It leverages
utility functions to verify target paths and directories.
"""
from abc import abstractmethod
from ..utils.utils import check_directory, check_str_is_file
from ..load.loader import Loader

class FileLoader(Loader):
    """
    FileLoader

    A concrete loader for writing a DataFrame to a file. This class extends Loader and provides methods
    to determine the target file path, handle file modes according to the specified existence parameter,
    and define the file extension for the target file.
    """

    def __init__(self,
                 target,
                 dataframe,
                 exists,
                 func,
                 file_extension,
                 on_error,
                 step_name="FileLoader",
                 **kwargs):
        """
        FileLoader Class Constructor
        Initializes the FileLoader object.

        Arguments:
            target (str): 
                The target directory where the file will be written
            dataframe (DataFrame): 
                The DataFrame to be written to the file
            exists (str): 
                The file mode to use when writing the file
            func (function): 
                The function to be executed by the loader
            file_extension (str): 
                The file extension to use when writing the file
            on_error (str): 
                The error handling strategy
            step_name (str): 
                The name of the step
            **kwargs: 
                Additional keyword arguments for the loader function
        """
        super().__init__(step_name=step_name,
                         dataframes=dataframe,
                         exists=exists,
                         func=func,
                         on_error=on_error)

        if check_str_is_file(target):
            self.target_file_path = target
        else:
            if not check_directory(target):
                raise FileNotFoundError("Error directory not found")
            self.file_extension = file_extension
            self.target_file_path = None
            self.target=target
        self.kwargs = kwargs

    @abstractmethod
    def func(self, context):
        """
        Abstract method: func()
        Reads the DataFrame from the context and writes it to a file
        """
