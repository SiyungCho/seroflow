"""
"""

import os
from ..load.file_loader import FileLoader, MultiFileLoader

class ExcelLoader(FileLoader):
    """
    """

    def __init__(self, target, file_extension=".xlsx", dataframes=None, exists="append", step_name="CSVLoader", **kwargs):
        """
        """
        super().__init__(target=target, dataframes=dataframes, exists=exists, func=self.func, step_name=step_name, kwargs=kwargs)
        self.file_extension = file_extension

    def func(self, context):
        """
        """
        for key, df in context.dataframes.items():
            target_file_path = os.path.join(self.target_dir, key + self.file_extension)
            self.__to_excel(df, target_file_path, self.kwargs)

    def __to_excel(self, df, target_file_path, kwargs):
        """
        """
        df.to_excel(target_file_path, mode=self.map_exists_parameter(), **kwargs)

class MultiExcelLoader(MultiFileLoader):
    def __init__(self, target, dataframes, exists='append', **kwargs):
        super().__init__(target=target, dataframes=dataframes, exists=exists, type=ExcelLoader, step_name="MultiExcelLoader", kwargs=kwargs)