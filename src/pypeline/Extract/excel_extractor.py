import pandas as pd
import openpyxl
from ..Utils.utils import *
from ..Extract.extractor import extractor
from ..Wrappers.wrappers import log_error

class excel_extractor(extractor): 
    def __init__(self, source, step_name = "excel_extractor", **kwargs):
        super().__init__(step_name = step_name, func = self.func)
        if not check_directory(source): #or check if its a file
            raise Exception(f"""Error directory not found""")
        
        self.source = source
        self.file_paths, self.file_names = gather_files(self.source, ["xlsx", "xls"])
        self.kwargs = kwargs

    def func(self, context):
        for name, file in zip(self.file_names, self.file_paths):
            context.add_dataframe(remove_extension(name), self.__read_excel(file, self.kwargs))
        return context

    def __read_excel(self, file, kwargs):
        if file.endswith('.xls'):
            return pd.read_excel(file, engine='xlrd', **kwargs)
        elif file.endswith('.xlsx'):
            return pd.read_excel(file, engine='openpyxl', **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file}")