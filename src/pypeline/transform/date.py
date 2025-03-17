"""
"""
import pandas as pd
from .transformation import Transformation

# class ExtractDateTime(Transformation):
class ConvertToDateTime(Transformation):
    """
    Converts a column to datetime format.
    """
    def __init__(self,
                 dataframe,
                 column,
                 format=None,
                 step_name="ConvertToDateTime",
                 on_error=None):
        """
        """
        self.dataframe = dataframe
        self.column = column
        self.format = format
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__convert_to_datetime(df))
        return context

    def __convert_to_datetime(self, df):
        """
        """
        if self.format:
            df[self.column] = pd.to_datetime(df[self.column], format=self.format)
        else:
            df[self.column] = pd.to_datetime(df[self.column])
        return df
