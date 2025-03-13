"""
"""
from abc import abstractmethod
from ..utils.utils import check_directory, check_file
from ..load.loader import Loader, MultiLoader
from ..load.excel_loader import ExcelLoader
from ..load.csv_loader import CSVLoader

class FileLoader(Loader):
    """
    """

    def __init__(self, target, dataframes, exists, func, step_name="FileLoader", **kwargs):
        """
        """
        super().__init__(step_name=step_name, dataframes=dataframes, exists=exists, func=func)
        if not check_directory(target):
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
        """
        pass

class MultiFileLoader(MultiLoader):
    """
    """
    def __init__(self, target, dataframes, exists, type, step_name="MultiFileLoader", **kwargs):
        """
        """
        super().__init__(step_name=step_name, target=target, exists=exists, type=type)
        if not check_directory(self.target): 
            raise FileNotFoundError("Error directory not found")
        if not isinstance(dataframes, list):
            raise TypeError("Error dataframes must be a list")
        
        self.dataframes = dataframes
        self.add_loaders(self.dataframes, **kwargs)
