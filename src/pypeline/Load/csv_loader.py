from ..Utils.utils import *
from ..Load.loader import loader
from ..Wrappers.wrappers import log_error
from ..Context.Context import context as base_context

class csv_loader(loader):
    def __init__(self, target, step_name = "csv_releasor", description = "Release to csv file", mode = "TEST", contexts = ['all'], exists = "append", **kwargs):
        super().__init__(step_name = step_name, description = description, mode = mode, contexts = contexts, exists = exists, func = self.func)
        if not check_directory(target):
            raise Exception(f"""Error directory not found""")
        
        self.target_dir = target
        self.kwargs = kwargs

    def func(self, context):
        for context_item in context.values():
            for key, df in context_item.dataframes.items():
                target_file_path = os.path.join(self.target_dir, key + ".csv")
                self.__to_csv(df, target_file_path, self.kwargs)
        return

    def __to_csv(self, df, target_file_path, kwargs):
        if self.mode == 'TEST':
            self.logger.logger.info(f"""current df...{key}: {df}""")
        else:
            df.to_csv(target_file_path, mode = self.map_exists_parameter(), **kwargs)
            print("context released to csv file: " + target_file_path)

    def map_exists_parameter(self):
        if self.exists == "append":
            return 'a'
        elif self.exists == "fail":
            return 'x'
        elif self.exists == "replace":
            return 'w'