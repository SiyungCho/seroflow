import pandas as pd
from .transformation import Transformation

class ConvertColumnType(Transformation):
    """
    Converts a specified column of a dataframe to a new data type.
    """
    def __init__(self, dataframe, column, new_type, step_name="ConvertColumnType"):
        self.dataframe = dataframe
        self.column = column
        self.new_type = new_type
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__convert_column_type(df, self.column, self.new_type)
        context.set_dataframe(self.dataframe, df)
        return context
    
    def __convert_column_type(self, df, column, new_type):
        return df[column].astype(new_type)

class RenameColumns(Transformation):
    """
    Renames one or more columns in a dataframe based on a mapping.
    """
    def __init__(self, dataframe, columns_mapping, step_name="RenameColumns"):
        self.dataframe = dataframe
        self.columns_mapping = columns_mapping
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__rename_columns(df))
        return context
    
    def __rename_columns(self, df):
        return df.rename(columns=self.columns_mapping, inplace=True)

class DropColumn(Transformation):
    """
    Drops a specified column from a dataframe.
    """
    def __init__(self, dataframe, column, step_name="DropColumn"):
        self.dataframe = dataframe
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__drop_column(df))
        return context
    
    def __drop_column(self, df):
        return df.drop(columns=[self.column])

class DropColumns(Transformation):
    def __init__(self, dataframe, columns, step_name="DropColumns"):
        self.dataframe = dataframe
        self.columns = columns
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__drop_columns(df))
        return context

    def __drop_columns(self, df):
        return df.drop(columns=self.columns, errors='ignore')
    
class AddColumn(Transformation):
    """
    Adds a new column to a dataframe computed from a function.
    """
    def __init__(self, dataframe, column, compute_func, step_name="AddColumn"):
        self.dataframe = dataframe
        self.column = column
        self.compute_func = compute_func  # function that receives a dataframe and returns a Series
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__compute_column(df)
        context.set_dataframe(self.dataframe, df)
        return context
    
    def __compute_column(self, df):
        return self.compute_func(df)

class MergeColumns(Transformation):
    """
    Merges multiple columns into a single column by concatenating their string representations.
    """
    def __init__(self, dataframe, columns, new_column, separator=" ", step_name="MergeColumns"):
        self.dataframe = dataframe
        self.columns = columns
        self.new_column = new_column
        self.separator = separator
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        df[self.new_column] = self.__merge_columns(df)
        context.set_dataframe(self.dataframe, df)
        return context
    
    def __merge_columns(self, df):
        return df[self.columns].astype(str).agg(self.separator.join, axis=1)

class SplitColumn(Transformation):
    """
    Splits a single column into multiple columns based on a delimiter.
    """
    def __init__(self, dataframe, column, new_columns, delimiter=" ", step_name="SplitColumn"):
        self.dataframe = dataframe
        self.column = column
        self.new_columns = new_columns
        self.delimiter = delimiter
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__split_column(df))
        return context
    
    def __split_column(self, df):
        splits = df[self.column].str.split(self.delimiter, expand=True)
        splits.columns = self.new_columns
        df = pd.concat([df, splits], axis=1)
        return df

class ExplodeColumn(Transformation):
    """
    Explodes a column of lists into multiple rows.
    """
    def __init__(self, dataframe, column, step_name="ExplodeColumn"):
        self.dataframe = dataframe
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__explode_column(df))
        return context
    
    def __explode_column(self, df):
        return df.explode(self.column)