"""
Module: loader

This module defines the Loader class, an abstract base class for writing DataFrames to files. 
Loader extends the Step class and provides a common interface for handling file output operations, including
determining the target file path, managing file modes according to a specified 'exists' parameter, and defining the file
extension for the output file. Subclasses must implement the abstract methods func() and map_exists_parameter() to provide
file-format-specific functionality.
"""

from abc import abstractmethod
from ..step.step import Step

class Loader(Step):
    """
    Loader
    An Abstract class for writing a DataFrame to a file. This class extends the Step class and provides methods
    to determine the target file path, handle file modes according to the specified existence parameter,
    and define the file extension for the target file.
    """

    def __init__(self,
                 step_name,
                 dataframes,
                 exists,
                 func,
                 on_error):
        """
        Loader Class Constructor
        Initializes the Loader object.

        Arguments:
            step_name (str): 
                The name of the step
            dataframes (DataFrame): 
                The DataFrame to be written to the file
            exists (str): 
                The file mode to use when writing the file
            func (function): 
                The function to be executed by the loader
            on_error (str): 
                The error handling strategy
        """
        super().__init__(step_name=step_name,
                         dataframes=dataframes if isinstance(dataframes, list) else [dataframes],
                         func=func,
                         on_error=on_error)
        self.exists = self.__check_exists_parameter(exists)

    def __check_exists_parameter(self, exists):
        """
        Private method: __check_exists_parameter()
        Checks if the exists parameter is valid.

        Arguments:
            exists (str): 
                The file mode to use when writing the file

        Returns:
            str: 
                The file mode to use when writing the file
        """
        if exists not in ['append', 'fail', 'replace']:
            raise ValueError("exists param must be either 'append', 'fail' or 'replace'")
        return exists

    def start_step(self):
        """
        Public method: start_step()
        Validates that the inputted context is of the correct type
        """
        # Check that inputted context is of context type
        return

    def stop_step(self):
        """
        Public method: stop_step()
        Clears the parameters dictionary
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        Abstract method: func()
        Writes the DataFrame to a file
        """

    @abstractmethod
    def map_exists_parameter(self):
        """
        Abstract method: map_exists_parameter()
        Maps the exists parameter to the appropriate file mode
        """
