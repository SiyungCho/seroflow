from ..Utils.utils import *
from ..Load.loader import loader
from ..Wrappers.wrappers import log_error

class excel_loader(loader):
    def __init__(self, target, file_extension=".xlsx", step_name = "excel_loader", dataframes = [], exists = "append", **kwargs):
        super().__init__(step_name = step_name, dataframes=dataframes, exists = exists, func = self.func)
        if not check_directory(target): #or check if its a file
            raise Exception(f"""Error directory not found""")
        
        self.target_dir = target
        self.kwargs = kwargs
        self.file_extension = file_extension

    def func(self, context):
        for key, df in context.dataframes.items():
            target_file_path = os.path.join(self.target_dir, key + self.file_extension)
            self.__to_excel(df, target_file_path, self.kwargs)
        return

    def __to_excel(self, df, target_file_path, kwargs):
        df.to_excel(target_file_path, mode = self.map_exists_parameter(), **kwargs)

    def map_exists_parameter(self):
        if self.exists == "append":
            return 'a'
        elif self.exists == "fail":
            return 'x'
        elif self.exists == "replace":
            return 'w'