"""
"""
import os
from ..load.file_loader import FileLoader

class CSVLoader(FileLoader):
    """
    """

    def __init__(self, target, dataframe, exists="append", step_name="CSVLoader", **kwargs):
        """
        """
        super().__init__(target=target, dataframe=dataframe, exists=exists, func=self.func, file_extension=".csv", step_name=step_name, **kwargs)

    def func(self, context):
        """
        """
        for key, df in context.dataframes.items():
            if self.target_file_path is None:
                target_file_path = os.path.join(self.target, key + self.file_extension)
            else:
                target_file_path = self.target_file_path
            self.__to_csv(df, target_file_path, self.kwargs)

    def __to_csv(self, df, target_file_path, kwargs):
        """
        """
        df.to_csv(target_file_path, mode=self.map_exists_parameter(), **kwargs)

    def map_exists_parameter(self):
        """
        """
        if self.exists == "append":
            return 'a'
        if self.exists == "fail":
            return 'x'
        if self.exists == "replace":
            return 'w'
        return None

class MultiCSVLoader(CSVLoader):
    def __init__(self, target, dataframes=None, exists="append", step_name="MultiCSVLoader", **kwargs):
        super().__init__(target=target, dataframe=dataframes, exists=exists, step_name=step_name, **kwargs)
