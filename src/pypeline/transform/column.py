import pandas as pd
from .transformation import Transformation

class ConvertColumnType(Transformation):
    """
    Converts a specified column of a dataframe to a new data type.
    """
    def __init__(self, dataframe_name, column, new_type, step_name="ConvertColumnType"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.new_type = new_type
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df[self.column] = df[self.column].astype(self.new_type)
        context.set_dataframe(self.dataframe_name, df)
        return context

class RenameColumns(Transformation):
    """
    Renames one or more columns in a dataframe based on a mapping.
    """
    def __init__(self, dataframe_name, columns_mapping, step_name="RenameColumns"):
        self.dataframe_name = dataframe_name
        self.columns_mapping = columns_mapping
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df.rename(columns=self.columns_mapping, inplace=True)
        context.set_dataframe(self.dataframe_name, df)
        return context

class DropColumn(Transformation):
    """
    Drops a specified column from a dataframe.
    """
    def __init__(self, dataframe_name, column, step_name="DropColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df = df.drop(columns=[self.column])
        context.set_dataframe(self.dataframe_name, df)
        return context

class DropColumns(Transformation):
    def __init__(self, dataframes, columns, step_name="DropColumns"):
        self.columns = columns
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            context.set_dataframe(dataframe_name, self.__drop_columns(df))
        return context

    def __drop_columns(self, df):
        # 'errors="ignore"' avoids errors if a column is not found.
        return df.drop(columns=self.columns, errors='ignore')
    
class AddColumn(Transformation):
    """
    Adds a new column to a dataframe computed from a function.
    """
    def __init__(self, dataframe_name, column, compute_func, step_name="AddColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.compute_func = compute_func  # function that receives a dataframe and returns a Series
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df[self.column] = self.compute_func(df)
        context.set_dataframe(self.dataframe_name, df)
        return context

class MergeColumns(Transformation):
    """
    Merges multiple columns into a single column by concatenating their string representations.
    """
    def __init__(self, dataframe_name, columns, new_column, separator=" ", step_name="MergeColumns"):
        self.dataframe_name = dataframe_name
        self.columns = columns
        self.new_column = new_column
        self.separator = separator
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df[self.new_column] = df[self.columns].astype(str).agg(self.separator.join, axis=1)
        context.set_dataframe(self.dataframe_name, df)
        return context

class SplitColumn(Transformation):
    """
    Splits a single column into multiple columns based on a delimiter.
    """
    def __init__(self, dataframe_name, column, new_columns, delimiter=" ", step_name="SplitColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.new_columns = new_columns
        self.delimiter = delimiter
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        splits = df[self.column].str.split(self.delimiter, expand=True)
        splits.columns = self.new_columns
        df = pd.concat([df, splits], axis=1)
        context.set_dataframe(self.dataframe_name, df)
        return context

class ExplodeColumn(Transformation):
    """
    Explodes a column of lists into multiple rows.
    """
    def __init__(self, dataframe_name, column, step_name="ExplodeColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        exploded_df = df.explode(self.column)
        context.set_dataframe(self.dataframe_name, exploded_df)
        return context