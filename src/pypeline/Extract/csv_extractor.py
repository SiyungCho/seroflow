import pandas as pd
from ..Utils.utils import *
from ..Extract.extractor import extractor
from ..Wrappers.wrappers import log_error

class csv_extractor(extractor): 
    def __init__(self, source, step_name = "csv_extractor", **kwargs):
        super().__init__(step_name = step_name, func = self.func)
        if not check_directory(source):
            raise Exception(f"""Error directory not found""")
        
        self.source = source
        self.file_paths, self.file_names = gather_files(self.source, ["csv"])
        self.kwargs = kwargs

    def func(self, context):
        for name, file in zip(self.file_names, self.file_paths):
            context.add_dataframe(remove_extension(name), self.__read_csv(file, self.kwargs))
        return context

    def __read_csv(self, file, kwargs):
        return pd.read_csv(file, **kwargs)