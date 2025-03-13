import pandasql as sqldf
from .transformation import Transformation

class SQLQuery(Transformation):
    """
    Executes a SQL query using pandasql on the dataframes in the context.
    The query can reference any dataframe in context by its key.
    """
    def __init__(self, query, output_dataframe_name, step_name="SQLQuery"):
        self.query = query
        self.output_dataframe_name = output_dataframe_name
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        # The query uses context.dataframes as the namespace
        result = sqldf.sqldf(self.query, context.dataframes)
        context.set_dataframe(self.output_dataframe_name, result)
        return context