"""
"""
import os
import pandas as pd
from ..load.file_loader import FileLoader

class ExcelLoader(FileLoader):
    """
    """

    def __init__(self,
                 target,
                 dataframe,
                 file_extension=".xlsx",
                 exists="append",
                 step_name="ExcelLoader",
                 on_error=None,
                 **kwargs):
        """
        """
        super().__init__(target=target,
                         dataframe=dataframe,
                         exists=exists,
                         func=self.func,
                         step_name=step_name,
                         file_extension=file_extension,
                         on_error=on_error,
                         **kwargs)

    def func(self, context):
        """
        """
        for key, df in context.dataframes.items():
            if self.target_file_path is None:
                file_path = key+self.file_extension
                target_file_path = os.path.join(self.target, file_path)
            else:
                target_file_path = self.target_file_path
            self.__to_excel(df, target_file_path, self.kwargs)

    def __to_excel(self, df, target_file_path, kwargs):
        directory = os.path.dirname(target_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if self.file_extension == '.xls':
            engine = 'xlrd'
        elif self.file_extension == '.xlsx':
            engine = 'openpyxl'

        if os.path.exists(target_file_path):
            with pd.ExcelWriter(target_file_path,
                                engine=engine,
                                mode='a',
                                if_sheet_exists=self.map_exists_parameter()
                                ) as f:
                df.to_excel(f, **kwargs)
        else:
            with pd.ExcelWriter(target_file_path,
                                engine=engine,
                                mode='w'
                                ) as f:
                df.to_excel(f, **kwargs)

    def map_exists_parameter(self):
        """
        """
        if self.exists == "append":
            return 'overlay'
        if self.exists == "fail":
            return 'error'
        if self.exists == "replace":
            return 'replace'
        return None

class MultiExcelLoader(ExcelLoader):
    """
    """
    def __init__(self,
                 target,
                 dataframes=None,
                 file_extension=".xlsx",
                 exists="append",
                 step_name="MultiExcelLoader",
                 on_error=None,
                 **kwargs):
        """
        """
        super().__init__(target=target,
                         dataframe=dataframes,
                         file_extension=file_extension,
                         exists=exists,
                         step_name=step_name,
                         on_error=on_error,
                         **kwargs)
