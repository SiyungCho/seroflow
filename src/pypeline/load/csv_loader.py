"""
"""

import os
from ..load.file_loader import FileLoader, MultiFileLoader

class CSVLoader(FileLoader):
    """
    """

    def __init__(self, target, dataframes=None, exists="append", step_name="CSVLoader", **kwargs):
        """
        """
        super().__init__(target=target, dataframes=dataframes, exists=exists, func=self.func, step_name=step_name, kwargs=kwargs)

    def func(self, context):
        """
        """
        for key, df in context.dataframes.items():
            target_file_path = os.path.join(self.target_dir, key + ".csv")
            self.__to_csv(df, target_file_path, self.kwargs)

    def __to_csv(self, df, target_file_path, kwargs):
        """
        """
        df.to_csv(target_file_path, mode=self.map_exists_parameter(), **kwargs)

class MultiCSVLoader(MultiFileLoader):
    def __init__(self, target, dataframes, exists='append', **kwargs):
        super().__init__(target=target, dataframes=dataframes, exists=exists, type=CSVLoader, step_name="MultiCSVLoader", kwargs=kwargs)