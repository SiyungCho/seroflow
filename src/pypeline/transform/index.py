from .transformation import Transformation

class SetIndex(Transformation):
    """
    Sets a specified column as the index of a dataframe.
    """
    def __init__(self, dataframe_name, index_column, step_name="SetIndex"):
        self.dataframe_name = dataframe_name
        self.index_column = index_column
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df.set_index(self.index_column, inplace=True)
        context.set_dataframe(self.dataframe_name, df)
        return context

class ResetIndex(Transformation):
    """
    Resets the index of a dataframe.
    """
    def __init__(self, dataframe_name, drop=False, step_name="ResetIndex"):
        self.dataframe_name = dataframe_name
        self.drop = drop
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df.reset_index(drop=self.drop, inplace=True)
        context.set_dataframe(self.dataframe_name, df)
        return context