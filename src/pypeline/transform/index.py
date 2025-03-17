"""
"""
from .transformation import Transformation

class SetIndex(Transformation):
    """
    Sets a specified column as the index of a dataframe.
    """
    def __init__(self,
                 dataframe,
                 index_column,
                 step_name="SetIndex",
                 on_error=None):
        """
        """
        self.dataframe = dataframe
        self.index_column = index_column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__set_index(df))
        return context

    def __set_index(self, df):
        """
        """
        return df.set_index(self.index_column, inplace=True)

class ResetIndex(Transformation):
    """
    Resets the index of a dataframe.
    """
    def __init__(self,
                 dataframe,
                 drop=False,
                 step_name="ResetIndex",
                 on_error=None):
        """
        """
        self.dataframe = dataframe
        self.drop = drop
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__reset_index(df))
        return context

    def __reset_index(self, df):
        """
        """
        return df.reset_index(drop=self.drop, inplace=True)
