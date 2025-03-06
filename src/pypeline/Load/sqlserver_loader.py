from ..Utils.utils import *
from ..Load.loader import loader
from ..Wrappers.wrappers import log_error

class sqlserver_loader(loader):
    def __init__(self, target, engine, step_name = "sqlserver_loader", dataframes = [], exists = "append", **kwargs):
        super().__init__(step_name = step_name, dataframes=dataframes, exists = exists, func = self.func)
        #Need to check that engine is an engine
        
        self.target = [target] if not isinstance(target, list) else target
        self.engine = engine
        self.kwargs = kwargs

    def func(self, context):
        for target, (key, df) in zip(self.target, context.dataframes.items()):
            self.__to_sql(df, target, f"""{self.engine.database}.{self.engine.schema}""", self.engine.engine, self.kwargs)
        return

    def __to_sql(self, df, target, schema, engine, kwargs):
        df.to_sql(target, con=engine, if_exists= self.map_exists_parameter(), schema=schema, **kwargs)

    def map_exists_parameter(self):
        return self.exists