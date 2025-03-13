import pandas as pd
from .transformation import Transformation

class TransposeDataFrame(Transformation):
    def __init__(self, dataframes, step_name="TransposeDataFrame"):
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            context.set_dataframe(dataframe_name, self.__transpose_df(df))
        return context
    
    def __transpose_df(self, df):
        return pd.DataFrame.transpose(df)
    
class PivotDataFrame(Transformation):
    """
    Creates a pivot table from a dataframe.
    """
    def __init__(self, dataframe_name, index, columns, values, aggfunc='mean', step_name="PivotDataFrame"):
        self.dataframe_name = dataframe_name
        self.index = index
        self.columns = columns
        self.values = values
        self.aggfunc = aggfunc
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        pivot_df = pd.pivot_table(df, index=self.index, columns=self.columns,
                                  values=self.values, aggfunc=self.aggfunc)
        # Reset index so that the pivot becomes a normal dataframe
        context.set_dataframe(self.dataframe_name, pivot_df.reset_index())
        return context

class MeltDataFrame(Transformation):
    """
    Unpivots a dataframe from wide to long format.
    """
    def __init__(self, dataframe_name, id_vars, value_vars, var_name="variable", value_name="value", step_name="MeltDataFrame"):
        self.dataframe_name = dataframe_name
        self.id_vars = id_vars
        self.value_vars = value_vars
        self.var_name = var_name
        self.value_name = value_name
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        melted_df = pd.melt(df, id_vars=self.id_vars, value_vars=self.value_vars,
                            var_name=self.var_name, value_name=self.value_name)
        context.set_dataframe(self.dataframe_name, melted_df)
        return context

class GroupByAggregate(Transformation):
    """
    Groups a dataframe by specified columns and aggregates other columns based on a dictionary of functions.
    """
    def __init__(self, dataframe_name, groupby_columns, agg_dict, step_name="GroupByAggregate"):
        self.dataframe_name = dataframe_name
        self.groupby_columns = groupby_columns
        self.agg_dict = agg_dict  # e.g., {'col1': 'sum', 'col2': 'mean'}
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        grouped_df = df.groupby(self.groupby_columns).agg(self.agg_dict).reset_index()
        context.set_dataframe(self.dataframe_name, grouped_df)
        return context

class AggregateDataFrame(Transformation):
    def __init__(self, dataframes, group_by, agg_dict, step_name="AggregateDataFrame"):
        self.group_by = group_by
        self.agg_dict = agg_dict
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            # Group, aggregate, and reset the index.
            context.set_dataframe(dataframe_name, self.__aggregate_df(df))
        return context

    def __aggregate_df(self, df):
        return df.groupby(self.group_by).agg(self.agg_dict).reset_index()

class FilterRows(Transformation):
    """
    Filters rows of a dataframe based on a boolean function.
    The filter_func should accept the dataframe and return a boolean Series.
    """
    def __init__(self, dataframe_name, filter_func, step_name="FilterRows"):
        self.dataframe_name = dataframe_name
        self.filter_func = filter_func
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        filtered_df = df[self.filter_func(df)]
        context.set_dataframe(self.dataframe_name, filtered_df)
        return context

class SortDataFrame(Transformation):
    """
    Sorts a dataframe by the given column(s).
    """
    def __init__(self, dataframe_name, by, ascending=True, step_name="SortDataFrame"):
        self.dataframe_name = dataframe_name
        self.by = by
        self.ascending = ascending
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        sorted_df = df.sort_values(by=self.by, ascending=self.ascending)
        context.set_dataframe(self.dataframe_name, sorted_df)
        return context

class DropDuplicates(Transformation):
    """
    Removes duplicate rows from a dataframe.
    """
    def __init__(self, dataframe_name, subset=None, keep='first', step_name="DropDuplicates"):
        self.dataframe_name = dataframe_name
        self.subset = subset
        self.keep = keep
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        deduped_df = df.drop_duplicates(subset=self.subset, keep=self.keep)
        context.set_dataframe(self.dataframe_name, deduped_df)
        return context

class SelectColumns(Transformation):
    """
    Selects a subset of columns from a dataframe.
    """
    def __init__(self, dataframe_name, columns, step_name="SelectColumns"):
        self.dataframe_name = dataframe_name
        self.columns = columns
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        selected_df = df[self.columns]
        context.set_dataframe(self.dataframe_name, selected_df)
        return context

class FillNAValues(Transformation):
    def __init__(self, dataframes, fill_value, step_name="FillNAValues"):
        self.fill_value = fill_value
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            context.set_dataframe(dataframe_name, self.__fillna_df(df))
        return context

    def __fillna_df(self, df):
        return df.fillna(self.fill_value)

class ReplaceValues(Transformation):
    def __init__(self, dataframes, to_replace, value, step_name="ReplaceValues"):
        self.to_replace = to_replace
        self.value = value
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            context.set_dataframe(dataframe_name, self.__replace_values(df))
        return context

    def __replace_values(self, df):
        return df.replace(self.to_replace, self.value)

class MergeDataFrames(Transformation):
    """
    Merges two dataframes from the context on a specified column(s).
    """
    def __init__(self, left_dataframe_name, right_dataframe_name, on, how='inner', output_name=None, step_name="MergeDataFrames"):
        self.left_dataframe_name = left_dataframe_name
        self.right_dataframe_name = right_dataframe_name
        self.on = on
        self.how = how
        self.output_name = output_name if output_name else left_dataframe_name
        super().__init__(step_name=step_name, func=self.func)
    
    def func(self, context):
        left_df = context.dataframes[self.left_dataframe_name]
        right_df = context.dataframes[self.right_dataframe_name]
        merged_df = pd.merge(left_df, right_df, on=self.on, how=self.how)
        context.set_dataframe(self.output_name, merged_df)
        return context

class JoinDataFrames(Transformation):
    def __init__(self, primary_dataframe, secondary_dataframe, on=None, how='left', lsuffix='', rsuffix='', step_name="JoinDataFrames"):
        self.primary_dataframe = primary_dataframe
        self.secondary_dataframe = secondary_dataframe
        self.on = on
        self.how = how
        self.lsuffix = lsuffix
        self.rsuffix = rsuffix
        # Note: the provided keys must exist in the context.
        super().__init__(step_name=step_name, func=self.func, dataframes={primary_dataframe: None, secondary_dataframe: None})

    def func(self, context):
        left = context.get_dataframe(self.primary_dataframe)
        right = context.get_dataframe(self.secondary_dataframe)
        joined_df = self.__join_df(left, right)
        context.set_dataframe(self.primary_dataframe, joined_df)
        return context

    def __join_df(self, left, right):
        return left.join(right, on=self.on, how=self.how, lsuffix=self.lsuffix, rsuffix=self.rsuffix)

class ApplyFunction(Transformation):
    def __init__(self, dataframes, function, column=None, axis=0, step_name="ApplyFunction"):
        self.function = function
        self.column = column
        self.axis = axis
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            updated_df = self.__apply_function(df)
            context.set_dataframe(dataframe_name, updated_df)
        return context

    def __apply_function(self, df):
        if self.column:
            df[self.column] = df[self.column].apply(self.function)
            return df
        else:
            return df.apply(self.function, axis=self.axis)
        
class ApplyMap(Transformation):
    def __init__(self, dataframes, function, step_name="ApplyMap"):
        self.function = function
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            mapped_df = self.__apply_map(df)
            context.set_dataframe(dataframe_name, mapped_df)
        return context

    def __apply_map(self, df):
        return df.applymap(self.function)
    
class MapValues(Transformation):
    """
    Maps the values in a column based on a provided dictionary.
    """
    def __init__(self, dataframe_name, column, mapping_dict, step_name="MapValues"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.mapping_dict = mapping_dict
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df[self.column] = df[self.column].map(self.mapping_dict)
        context.set_dataframe(self.dataframe_name, df)
        return context

class OneHotEncode(Transformation):
    """
    Performs one-hot encoding on a categorical column.
    """
    def __init__(self, dataframe_name, column, drop_original=False, step_name="OneHotEncode"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.drop_original = drop_original
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        dummies = pd.get_dummies(df[self.column], prefix=self.column)
        df = pd.concat([df, dummies], axis=1)
        if self.drop_original:
            df = df.drop(columns=[self.column])
        context.set_dataframe(self.dataframe_name, df)
        return context