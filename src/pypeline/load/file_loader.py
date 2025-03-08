"""
Module for loading pandas DataFrames to base files.
"""
from abc import abstractmethod
from ..utils.utils import check_directory
from ..load.loader import Loader


class FileLoader(Loader):
    """
    file loader class
    """

    def __init__(self,
                 target,
                 step_name="FileLoader",
                 dataframes=None,
                 exists="append",
                 func=None,
                 kwargs=None):
        """
        init method
        """
        super().__init__(step_name=step_name,
                         dataframes = [] if dataframes is None else dataframes,
                         exists=exists,
                         func=func)
        if not check_directory(target):  # or check if it's a file
            raise FileNotFoundError("Error directory not found")
        self.target_dir = target
        self.kwargs = kwargs

    def map_exists_parameter(self):
        """
        Map the 'exists' parameter to the appropriate Excel file mode.

        Returns:
            str: The file mode for pandas.DataFrame.to_excel:
                 'a' for append, 'x' for fail (if file exists), or 'w' for replace.
        """
        if self.exists == "append":
            return 'a'
        if self.exists == "fail":
            return 'x'
        if self.exists == "replace":
            return 'w'
        return None

    @abstractmethod
    def func(self, context):
        """
        custom func
        """
