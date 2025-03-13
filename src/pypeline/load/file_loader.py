"""
"""
from abc import abstractmethod
import os
from ..utils.utils import check_directory, check_str_is_file
from ..load.loader import Loader

class FileLoader(Loader):
    """
    """

    def __init__(self, target, dataframe, exists, func, file_extension, step_name="FileLoader", **kwargs):
        """
        """
        super().__init__(step_name=step_name, dataframes=dataframe, exists=exists, func=func)

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
        """
        pass
