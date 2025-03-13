import pandas as pd
from .transformation import Transformation

class ConvertToDateTime(Transformation):
    """
    Converts a column to datetime format.
    """
    def __init__(self, dataframe_name, column, format=None, step_name="ConvertToDateTime"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.format = format
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        if self.format:
            df[self.column] = pd.to_datetime(df[self.column], format=self.format)
        else:
            df[self.column] = pd.to_datetime(df[self.column])
        context.set_dataframe(self.dataframe_name, df)
        return context