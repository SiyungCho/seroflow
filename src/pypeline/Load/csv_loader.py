from ..Utils.utils import *
from ..Load.loader import loader
from ..Wrappers.wrappers import log_error

class csv_loader(loader):
    def __init__(self, target, step_name = "csv_loader", dataframes = [], exists = "append", **kwargs):
        super().__init__(step_name = step_name, dataframes=dataframes, exists = exists, func = self.func)
        if not check_directory(target): #or check if its a file
            raise Exception(f"""Error directory not found""")
        
        self.target_dir = target
        self.kwargs = kwargs

    def func(self, context):
        for key, df in context.dataframes.items():
            target_file_path = os.path.join(self.target_dir, key + ".csv")
            self.__to_csv(df, target_file_path, self.kwargs)
        return

    def __to_csv(self, df, target_file_path, kwargs):
        df.to_csv(target_file_path, mode = self.map_exists_parameter(), **kwargs)
            #print("context released to csv file: " + target_file_path)

    def map_exists_parameter(self):
        if self.exists == "append":
            return 'a'
        elif self.exists == "fail":
            return 'x'
        elif self.exists == "replace":
            return 'w'