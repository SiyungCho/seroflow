import pandas as pd
from ..Utils.utils import *
from ..Extract.extractor import extractor
from ..Wrappers.wrappers import log_error

class sqlserver_extractor(extractor): 
    def __init__(self, source, engine, step_name = "sqlserver_extractor", **kwargs):
        super().__init__(step_name = step_name, func = self.func)
        #Need to check that engine is an engine
        
        self.source = [source] if not isinstance(source, list) else source
        self.engine = engine
        self.kwargs = kwargs

    def func(self, context):
        for table_name in self.source:
            if not self.engine.table_exists(table_name): #Error table doesnt exist
                continue
            context.add_dataframe(table_name, self.__read_sqlserver_table(table_name, self.engine.schema, self.engine.engine, self.kwargs))
        return context

    def __read_sqlserver_table(self, table_name, schema, engine, kwargs):
        return pd.read_sql_table(table_name, schema=schema, con = engine.connect(), **kwargs)