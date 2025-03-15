import pandas as pd
from .transformation import Transformation
    
class TransposeDataFrame(Transformation):
    def __init__(self, dataframe, step_name="TransposeDataFrame", on_error=None):
        self.dataframe = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__transpose_df(df))
        return context
    
    def __transpose_df(self, df):
        return pd.DataFrame.transpose(df)
    
class PivotDataFrame(Transformation):
    """
    Creates a pivot table from a dataframe.
    """
    def __init__(self, dataframe, index, columns, values, aggfunc='mean', step_name="PivotDataFrame", on_error=None):
        self.dataframe = dataframe
        self.index = index
        self.columns = columns
        self.values = values
        self.aggfunc = aggfunc
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__pivot_df(df))
        return context
    
    def __pivot_df(self, df):
        return pd.pivot_table(df, index=self.index, columns=self.columns,
                              values=self.values, aggfunc=self.aggfunc).reset_index()

class MeltDataFrame(Transformation):
    """
    Unpivots a dataframe from wide to long format.
    """
    def __init__(self, dataframe, id_vars, value_vars, var_name="variable", value_name="value", step_name="MeltDataFrame", on_error=None):
        self.dataframe = dataframe
        self.id_vars = id_vars
        self.value_vars = value_vars
        self.var_name = var_name
        self.value_name = value_name
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__melt_df(df))
        return context
    
    def __melt_df(self, df):
        return pd.melt(df, id_vars=self.id_vars, value_vars=self.value_vars,
                       var_name=self.var_name, value_name=self.value_name)

class GroupByAggregate(Transformation):
    """
    Groups a dataframe by specified columns and aggregates other columns based on a dictionary of functions.
    """
    def __init__(self, dataframe, groupby_columns, agg_dict, step_name="GroupByAggregate", on_error=None):
        self.dataframe = dataframe
        self.groupby_columns = groupby_columns
        self.agg_dict = agg_dict  # e.g., {'col1': 'sum', 'col2': 'mean'}
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__groupby_aggregate(df))
        return context
    
    def __groupby_aggregate(self, df):
        return df.groupby(self.groupby_columns).agg(self.agg_dict).reset_index()

class FilterRows(Transformation):
    """
    Filters rows of a dataframe based on a boolean function.
    The filter_func should accept the dataframe and return a boolean Series.
    """
    def __init__(self, dataframe, filter_func, step_name="FilterRows", on_error=None):
        self.dataframe = dataframe
        self.filter_func = filter_func
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__filter_func(df))
        return context
    
    def __filter_func(self, df):
        return self.filter_func(df)

class SortDataFrame(Transformation):
    """
    Sorts a dataframe by the given column(s).
    """
    def __init__(self, dataframe, by, ascending=True, step_name="SortDataFrame", on_error=None):
        self.dataframe = dataframe
        self.by = by
        self.ascending = ascending
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__sort_df(df))
        return context
    
    def __sort_df(self, df):
        return df.sort_values(by=self.by, ascending=self.ascending)

class DropDuplicates(Transformation):
    """
    Removes duplicate rows from a dataframe.
    """
    def __init__(self, dataframe, subset=None, keep='first', step_name="DropDuplicates", on_error=None):
        self.dataframe = dataframe
        self.subset = subset
        self.keep = keep
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__drop_duplicates(df))
        return context
    
    def __drop_duplicates(self, df):
        return df.drop_duplicates(subset=self.subset, keep=self.keep)

class SelectColumns(Transformation):
    """
    Selects a subset of columns from a dataframe.
    """
    def __init__(self, dataframe, columns, step_name="SelectColumns", on_error=None):
        self.dataframe = dataframe
        self.columns = columns
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__select_columns(df))
        return context
    
    def __select_columns(self, df):
        return df[self.columns]

class FillNAValues(Transformation):
    def __init__(self, dataframe, fill_value, step_name="FillNAValues", on_error=None):
        self.dataframe = dataframe
        self.fill_value = fill_value
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)

    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__fillna_df(df))
        return context

    def __fillna_df(self, df):
        return df.fillna(self.fill_value)

class ReplaceValues(Transformation):
    def __init__(self, dataframe, to_replace, value, step_name="ReplaceValues", on_error=None):
        self.dataframe = dataframe
        self.to_replace = to_replace
        self.value = value
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__replace_values(df))
        return context

    def __replace_values(self, df):
        return df.replace(self.to_replace, self.value)

class MergeDataFrames(Transformation):
    """
    Merges two dataframes from the context on a specified column(s).
    """
    def __init__(self, left_dataframe, right_dataframe, on, how='inner', output_name=None, step_name="MergeDataFrames", on_error=None):
        self.left_dataframe = left_dataframe
        self.right_dataframe = right_dataframe
        self.on = on
        self.how = how
        self.output_name = output_name if output_name else left_dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=[left_dataframe, right_dataframe], on_error=on_error)
    
    def func(self, context):
        left_df = context.dataframes[self.left_dataframe]
        right_df = context.dataframes[self.right_dataframe]
        context.set_dataframe(self.output_name, self.__merge_df(left_df, right_df))
        return context
    
    def __merge_df(self, left_df, right_df):
        return pd.merge(left_df, right_df, on=self.on, how=self.how)

class JoinDataFrames(Transformation):
    def __init__(self, primary_dataframe, secondary_dataframe, on=None, how='left', lsuffix='', rsuffix='', step_name="JoinDataFrames", on_error=None):
        self.primary_dataframe = primary_dataframe
        self.secondary_dataframe = secondary_dataframe
        self.on = on
        self.how = how
        self.lsuffix = lsuffix
        self.rsuffix = rsuffix
        super().__init__(step_name=step_name, func=self.func, dataframes=[primary_dataframe, secondary_dataframe], on_error=on_error)

    def func(self, context):
        left = context.get_dataframe(self.primary_dataframe)
        right = context.get_dataframe(self.secondary_dataframe)
        joined_df = self.__join_df(left, right)
        context.set_dataframe(self.primary_dataframe, joined_df)
        return context

    def __join_df(self, left, right):
        return left.join(right, on=self.on, how=self.how, lsuffix=self.lsuffix, rsuffix=self.rsuffix)

class ApplyFunction(Transformation):
    def __init__(self, dataframe, function, column=None, axis=0, step_name="ApplyFunction", on_error=None):
        self.dataframe = dataframe
        self.function = function
        self.column = column
        self.axis = axis
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__apply_function(df))
        return context

    def __apply_function(self, df):
        if self.column:
            df[self.column] = df[self.column].apply(self.function)
            return df
        else:
            return df.apply(self.function, axis=self.axis)
        
class ApplyMap(Transformation):
    def __init__(self, dataframe, function, step_name="ApplyMap", on_error=None):
        self.dataframe = dataframe
        self.function = function
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
    
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__apply_map(df))
        return context

    def __apply_map(self, df):
        return df.applymap(self.function)
    
class MapValues(Transformation):
    """
    Maps the values in a column based on a provided dictionary.
    """
    def __init__(self, dataframe, column, mapping_dict, step_name="MapValues", on_error=None):
        self.dataframe = dataframe
        self.column = column
        self.mapping_dict = mapping_dict
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        df[self.column] = df[self.column].map(self.mapping_dict)
        context.set_dataframe(self.dataframe, df)
        return context

class OneHotEncode(Transformation):
    """
    Performs one-hot encoding on a categorical column.
    """
    def __init__(self, dataframe, column, drop_original=False, step_name="OneHotEncode", on_error=None):
        self.dataframe = dataframe
        self.column = column
        self.drop_original = drop_original
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        dummies = pd.get_dummies(df[self.column], prefix=self.column)
        df = pd.concat([df, dummies], axis=1)
        if self.drop_original:
            df = df.drop(columns=[self.column])
        context.set_dataframe(self.dataframe, df)
        return context
