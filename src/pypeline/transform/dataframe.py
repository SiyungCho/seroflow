"""
Module: dataframe.py

This module implements a collection of transformation classes that perform various operations on DataFrames.
Each transformation class extends the base Transformation class and updates the DataFrame stored in the
pypeline context accordingly.

Classes:
    TransposeDataFrame: Transposes the DataFrame.
    PivotDataFrame: Creates a pivot table from a DataFrame.
    MeltDataFrame: Unpivots a DataFrame from wide to long format.
    GroupByAggregate: Groups a DataFrame by specified columns and aggregates using provided functions.
    FilterRows: Filters rows in a DataFrame based on a boolean function.
    SortDataFrame: Sorts a DataFrame by one or more columns.
    DropDuplicates: Removes duplicate rows from a DataFrame.
    SelectColumns: Selects a subset of columns from a DataFrame.
    FillNAValues: Fills missing values in a DataFrame with a specified fill value.
    ReplaceValues: Replaces occurrences of specified values in a DataFrame with a new value.
    MergeDataFrames: Merges two DataFrames based on specified keys and merge strategy.
    JoinDataFrames: Joins two DataFrames using the pandas join method.
    ApplyFunction: Applies a function to an entire DataFrame or a specified column.
    ApplyMap: Applies a function element-wise to a DataFrame.
    MapValues: Maps the values in a specified column based on a provided dictionary.
    OneHotEncode: Performs one-hot encoding on a categorical column.
"""

import pandas as pd
from .transformation import Transformation

class TransposeDataFrame(Transformation):
    """
    TransposeDataFrame

    Transposes the specified DataFrame using the pandas transpose method.
    The transposed DataFrame replaces the original in the pypeline context.
    """
    def __init__(self,
                 dataframe,
                 step_name="TransposeDataFrame",
                 on_error=None):
        """
        Initializes the TransposeDataFrame transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context to be transposed.
            step_name (str, optional): The name of this transformation step. Defaults to "TransposeDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the transposition of the DataFrame.

        Retrieves the DataFrame from the context, transposes it, updates the context, and returns the context.

        Arguments:
            context (Context): The pypeline context containing the DataFrame.

        Returns:
            Context: The updated context with the transposed DataFrame.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__transpose_df(df))
        return context

    def __transpose_df(self, df):
        """
        Transposes the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to transpose.

        Returns:
            DataFrame: The transposed DataFrame.
        """
        return pd.DataFrame.transpose(df)

class PivotDataFrame(Transformation):
    """
    PivotDataFrame

    Creates a pivot table from a DataFrame using specified index, columns, values, and aggregation function.
    The resulting pivot table is added to the context.
    """
    def __init__(self,
                 dataframe,
                 index,
                 columns,
                 values,
                 aggfunc='mean',
                 step_name="PivotDataFrame",
                 on_error=None):
        """
        Initializes the PivotDataFrame transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            index (str or list): Column(s) to set as the pivot table index.
            columns (str or list): Column(s) to pivot.
            values (str): Column to aggregate.
            aggfunc (str or function, optional): Aggregation function to apply. Defaults to 'mean'.
            step_name (str, optional): The name of this transformation step. Defaults to "PivotDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.index = index
        self.columns = columns
        self.values = values
        self.aggfunc = aggfunc
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)

    def func(self, context):
        """
        Executes the pivot transformation.

        Retrieves the DataFrame from the context, creates a pivot table based on the provided parameters,
        updates the context, and returns it.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the pivot table.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__pivot_df(df))
        return context

    def __pivot_df(self, df):
        """
        Creates a pivot table from the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to pivot.

        Returns:
            DataFrame: The resulting pivot table with reset index.
        """
        return pd.pivot_table(df, index=self.index, columns=self.columns,
                              values=self.values, aggfunc=self.aggfunc).reset_index()

class MeltDataFrame(Transformation):
    """
    MeltDataFrame

    Unpivots a DataFrame from wide to long format using the pandas melt function.
    The melted DataFrame is updated in the pypeline context.
    """
    def __init__(self,
                 dataframe,
                 id_vars,
                 value_vars,
                 var_name="variable",
                 value_name="value",
                 step_name="MeltDataFrame",
                 on_error=None):
        """
        Initializes the MeltDataFrame transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            id_vars (str or list): Column(s) to use as identifier variables.
            value_vars (str or list): Column(s) to unpivot.
            var_name (str, optional): Name for the variable column. Defaults to "variable".
            value_name (str, optional): Name for the value column. Defaults to "value".
            step_name (str, optional): The name of this transformation step. Defaults to "MeltDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.id_vars = id_vars
        self.value_vars = value_vars
        self.var_name = var_name
        self.value_name = value_name
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the melt transformation.

        Retrieves the DataFrame from the context, melts it from wide to long format,
        updates the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the melted DataFrame.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__melt_df(df))
        return context

    def __melt_df(self, df):
        """
        Unpivots the DataFrame from wide to long format.

        Arguments:
            df (DataFrame): The DataFrame to melt.

        Returns:
            DataFrame: The melted DataFrame.
        """
        return pd.melt(df, id_vars=self.id_vars, value_vars=self.value_vars,
                       var_name=self.var_name, value_name=self.value_name)

class GroupByAggregate(Transformation):
    """
    GroupByAggregate

    Groups a DataFrame by specified column(s) and aggregates other columns based on a dictionary of functions.
    The resulting aggregated DataFrame is updated in the context.
    """
    def __init__(self,
                 dataframe,
                 groupby_columns,
                 agg_dict,
                 step_name="GroupByAggregate",
                 on_error=None):
        """
        Initializes the GroupByAggregate transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            groupby_columns (str or list): Column(s) to group by.
            agg_dict (dict): A dictionary specifying aggregation functions for columns (e.g., {'col1': 'sum', 'col2': 'mean'}).
            step_name (str, optional): The name of this transformation step. Defaults to "GroupByAggregate".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.groupby_columns = groupby_columns
        self.agg_dict = agg_dict
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the group by and aggregate transformation.

        Retrieves the DataFrame from the context, groups it by the specified columns, applies the aggregation
        functions, updates the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the aggregated DataFrame.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__groupby_aggregate(df))
        return context

    def __groupby_aggregate(self, df):
        """
        Groups and aggregates the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to group and aggregate.

        Returns:
            DataFrame: The grouped and aggregated DataFrame with reset index.
        """
        return df.groupby(self.groupby_columns).agg(self.agg_dict).reset_index()

class FilterRows(Transformation):
    """
    FilterRows

    Filters rows of a DataFrame based on a provided boolean function.
    The function should accept the DataFrame and return a boolean Series used for filtering.
    """
    def __init__(self,
                 dataframe,
                 filter_func,
                 step_name="FilterRows",
                 on_error=None):
        """
        Initializes the FilterRows transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            filter_func (function): A function that takes a DataFrame and returns a boolean Series for filtering rows.
            step_name (str, optional): The name of this transformation step. Defaults to "FilterRows".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.filter_func = filter_func
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the row filtering transformation.

        Retrieves the DataFrame from the context, applies the filter function to retain only rows where
        the function returns True, updates the context, and returns it.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with filtered rows.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__filter_func(df))
        return context

    def __filter_func(self, df):
        """
        Applies the filter function to the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to filter.

        Returns:
            DataFrame: The filtered DataFrame.
        """
        return self.filter_func(df)

class SortDataFrame(Transformation):
    """
    SortDataFrame

    Sorts a DataFrame by one or more specified columns.
    """
    def __init__(self,
                 dataframe,
                 by,
                 ascending=True,
                 step_name="SortDataFrame",
                 on_error=None):
        """
        Initializes the SortDataFrame transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            by (str or list): The column or list of columns to sort by.
            ascending (bool, optional): Whether to sort in ascending order. Defaults to True.
            step_name (str, optional): The name of this transformation step. Defaults to "SortDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.by = by
        self.ascending = ascending
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the sorting transformation.

        Retrieves the DataFrame from the context, sorts it by the specified column(s) in the desired order,
        updates the context, and returns the updated context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the sorted DataFrame.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__sort_df(df))
        return context

    def __sort_df(self, df):
        """
        Sorts the DataFrame by the specified columns.

        Arguments:
            df (DataFrame): The DataFrame to sort.

        Returns:
            DataFrame: The sorted DataFrame.
        """
        return df.sort_values(by=self.by, ascending=self.ascending)

class DropDuplicates(Transformation):
    """
    DropDuplicates

    Removes duplicate rows from a DataFrame based on specified subset columns.
    """
    def __init__(self,
                 dataframe,
                 subset=None,
                 keep='first',
                 step_name="DropDuplicates",
                 on_error=None):
        """
        Initializes the DropDuplicates transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            subset (str or list, optional): Column(s) to consider for identifying duplicates.
            keep (str, optional): Which duplicate to keep ('first', 'last', or False). Defaults to 'first'.
            step_name (str, optional): The name of this transformation step. Defaults to "DropDuplicates".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.subset = subset
        self.keep = keep
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)

    def func(self, context):
        """
        Executes the duplicate removal transformation.

        Retrieves the DataFrame from the context, drops duplicate rows based on the provided parameters,
        updates the context, and returns it.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with duplicates removed.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__drop_duplicates(df))
        return context

    def __drop_duplicates(self, df):
        """
        Drops duplicate rows from the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame after duplicate rows are removed.
        """
        return df.drop_duplicates(subset=self.subset, keep=self.keep)

class SelectColumns(Transformation):
    """
    SelectColumns

    Selects a subset of columns from a DataFrame.
    """
    def __init__(self,
                 dataframe,
                 columns,
                 step_name="SelectColumns",
                 on_error=None):
        """
        Initializes the SelectColumns transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            columns (list): A list of column names to retain.
            step_name (str, optional): The name of this transformation step. Defaults to "SelectColumns".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.columns = columns
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the column selection transformation.

        Retrieves the DataFrame from the context, selects the specified columns,
        updates the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with only the selected columns.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__select_columns(df))
        return context

    def __select_columns(self, df):
        """
        Selects the specified columns from the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame containing only the selected columns.
        """
        return df[self.columns]

class FillNAValues(Transformation):
    """
    FillNAValues

    Fills missing (NA) values in a DataFrame with a specified fill value.
    """
    def __init__(self,
                 dataframe,
                 fill_value,
                 step_name="FillNAValues",
                 on_error=None):
        """
        Initializes the FillNAValues transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            fill_value: The value to use for filling missing values.
            step_name (str, optional): The name of this transformation step. Defaults to "FillNAValues".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.fill_value = fill_value
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the NA filling transformation.

        Retrieves the DataFrame from the context, fills missing values with the specified fill value,
        updates the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with missing values filled.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__fillna_df(df))
        return context

    def __fillna_df(self, df):
        """
        Fills NA values in the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame after missing values have been filled.
        """
        return df.fillna(self.fill_value)

class ReplaceValues(Transformation):
    """
    ReplaceValues

    Replaces occurrences of specified values in a DataFrame with a new value.
    """
    def __init__(self,
                 dataframe,
                 to_replace,
                 value,
                 step_name="ReplaceValues",
                 on_error=None):
        """
        Initializes the ReplaceValues transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            to_replace: The value or list of values to be replaced.
            value: The value to replace with.
            step_name (str, optional): The name of this transformation step. Defaults to "ReplaceValues".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.to_replace = to_replace
        self.value = value
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ReplaceValues transformation.

        Retrieves the DataFrame from the context, replaces the specified values,
        updates the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with values replaced.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__replace_values(df))
        return context

    def __replace_values(self, df):
        """
        Replaces specified values in the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame with the values replaced.
        """
        return df.replace(self.to_replace, self.value)

class MergeDataFrames(Transformation):
    """
    MergeDataFrames

    Merges two DataFrames from the context based on specified key column(s) and merge strategy.
    The resulting merged DataFrame is updated in the context.
    """
    def __init__(self,
                 left_dataframe,
                 right_dataframe,
                 on,
                 how='inner',
                 output_name=None,
                 step_name="MergeDataFrames",
                 on_error=None):
        """
        Initializes the MergeDataFrames transformation.

        Arguments:
            left_dataframe (str): The name of the left DataFrame.
            right_dataframe (str): The name of the right DataFrame.
            on (str or list): The column(s) on which to merge.
            how (str, optional): The merge strategy (e.g., 'inner', 'outer', 'left', 'right'). Defaults to 'inner'.
            output_name (str, optional): The name under which the merged DataFrame will be stored in the context.
                                         Defaults to the left DataFrame's name.
            step_name (str, optional): The name of this transformation step. Defaults to "MergeDataFrames".
            on_error (str, optional): The error handling strategy.
        """
        self.left_dataframe = left_dataframe
        self.right_dataframe = right_dataframe
        self.on = on
        self.how = how
        self.output_name = output_name if output_name else left_dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=[left_dataframe, right_dataframe], on_error=on_error)

    def func(self, context):
        """
        Executes the MergeDataFrames transformation.

        Retrieves the left and right DataFrames from the context, merges them based on the specified keys and strategy,
        updates the context with the merged DataFrame under the output name, and returns the context.

        Arguments:
            context (Context): The context containing the DataFrames.

        Returns:
            Context: The updated context with the merged DataFrame.
        """
        left_df = context.dataframes[self.left_dataframe]
        right_df = context.dataframes[self.right_dataframe]
        context.set_dataframe(self.output_name, self.__merge_df(left_df, right_df))
        return context

    def __merge_df(self, left_df, right_df):
        """
        Merges the two DataFrames using pandas merge.

        Arguments:
            left_df (DataFrame): The left DataFrame.
            right_df (DataFrame): The right DataFrame.

        Returns:
            DataFrame: The merged DataFrame.
        """
        return pd.merge(left_df, right_df, on=self.on, how=self.how)

class JoinDataFrames(Transformation):
    """
    JoinDataFrames

    Joins two DataFrames from the context based on a specified key using the pandas join method.
    The joined DataFrame replaces the primary DataFrame in the context.
    """
    def __init__(self,
                 primary_dataframe,
                 secondary_dataframe,
                 on=None,
                 how='left',
                 lsuffix='',
                 rsuffix='',
                 step_name="JoinDataFrames",
                 on_error=None):
        """
        Initializes the JoinDataFrames transformation.

        Arguments:
            primary_dataframe (str): The name of the primary DataFrame.
            secondary_dataframe (str): The name of the secondary DataFrame to join.
            on (str, optional): The key column on which to join. Defaults to None.
            how (str, optional): The join strategy (e.g., 'left', 'right', 'inner', 'outer'). Defaults to 'left'.
            lsuffix (str, optional): Suffix for overlapping columns in the primary DataFrame. Defaults to ''.
            rsuffix (str, optional): Suffix for overlapping columns in the secondary DataFrame. Defaults to ''.
            step_name (str, optional): The name of this transformation step. Defaults to "JoinDataFrames".
            on_error (str, optional): The error handling strategy.
        """
        self.primary_dataframe = primary_dataframe
        self.secondary_dataframe = secondary_dataframe
        self.on = on
        self.how = how
        self.lsuffix = lsuffix
        self.rsuffix = rsuffix
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=[primary_dataframe, secondary_dataframe],
                         on_error=on_error)

    def func(self, context):
        """
        Executes the JoinDataFrames transformation.

        Retrieves the primary and secondary DataFrames from the context, joins them using the specified parameters,
        updates the context with the joined DataFrame under the primary DataFrame's name, and returns the context.

        Arguments:
            context (Context): The context containing the DataFrames.

        Returns:
            Context: The updated context with the joined DataFrame.
        """
        left = context.get_dataframe(self.primary_dataframe)
        right = context.get_dataframe(self.secondary_dataframe)
        joined_df = self.__join_df(left, right)
        context.set_dataframe(self.primary_dataframe, joined_df)
        return context

    def __join_df(self, left, right):
        """
        Joins the two DataFrames using the pandas join method.

        Arguments:
            left (DataFrame): The primary DataFrame.
            right (DataFrame): The secondary DataFrame.

        Returns:
            DataFrame: The joined DataFrame.
        """
        return left.join(right, on=self.on, how=self.how, lsuffix=self.lsuffix, rsuffix=self.rsuffix)

class ApplyFunction(Transformation):
    """
    ApplyFunction

    Applies a specified function to a DataFrame or a specific column of a DataFrame.
    """
    def __init__(self,
                 dataframe,
                 function,
                 column=None,
                 axis=0,
                 step_name="ApplyFunction",
                 on_error=None):
        """
        Initializes the ApplyFunction transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            function (function): The function to apply.
            column (str, optional): If provided, applies the function only to this column.
            axis (int, optional): The axis along which to apply the function (default is 0).
            step_name (str, optional): The name of this transformation step. Defaults to "ApplyFunction".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.function = function
        self.column = column
        self.axis = axis
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ApplyFunction transformation.

        Applies the specified function to the entire DataFrame or to the specified column,
        updates the DataFrame in the context, and returns the context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the function applied.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__apply_function(df))
        return context

    def __apply_function(self, df):
        """
        Applies the function to the DataFrame.

        If a column is specified, applies the function only to that column;
        otherwise, applies the function along the specified axis.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame after the function has been applied.
        """
        if self.column:
            df[self.column] = df[self.column].apply(self.function)
            return df
        else:
            return df.apply(self.function, axis=self.axis)

class ApplyMap(Transformation):
    """
    ApplyMap

    Applies a function element-wise to all elements in a DataFrame.
    """
    def __init__(self,
                 dataframe,
                 function,
                 step_name="ApplyMap",
                 on_error=None):
        """
        Initializes the ApplyMap transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            function (function): The function to apply element-wise.
            step_name (str, optional): The name of this transformation step. Defaults to "ApplyMap".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.function = function
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ApplyMap transformation.

        Applies the function element-wise to the DataFrame, updates the context,
        and returns the updated context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the function applied element-wise.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__apply_map(df))
        return context

    def __apply_map(self, df):
        """
        Applies the function to each element of the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame after the element-wise function is applied.
        """
        return df.applymap(self.function)

class MapValues(Transformation):
    """
    MapValues

    Maps the values in a specified column of a DataFrame using a provided dictionary.
    """
    def __init__(self,
                 dataframe,
                 column,
                 mapping_dict,
                 step_name="MapValues",
                 on_error=None):
        """
        Initializes the MapValues transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            column (str): The column whose values will be mapped.
            mapping_dict (dict): A dictionary defining the mapping from original values to new values.
            step_name (str, optional): The name of this transformation step. Defaults to "MapValues".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.mapping_dict = mapping_dict
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the MapValues transformation.

        Retrieves the DataFrame from the context, maps the values in the specified column using the mapping dictionary,
        updates the DataFrame in the context, and returns the context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with mapped column values.
        """
        df = context.dataframes[self.dataframe]
        df[self.column] = df[self.column].map(self.mapping_dict)
        context.set_dataframe(self.dataframe, df)
        return context

class OneHotEncode(Transformation):
    """
    OneHotEncode

    Performs one-hot encoding on a specified categorical column of a DataFrame.
    Optionally drops the original column after encoding.
    """
    def __init__(self,
                 dataframe,
                 column,
                 drop_original=False,
                 step_name="OneHotEncode",
                 on_error=None):
        """
        Initializes the OneHotEncode transformation.

        Arguments:
            dataframe (str): The name of the DataFrame in the context.
            column (str): The categorical column to one-hot encode.
            drop_original (bool, optional): Whether to drop the original column after encoding. Defaults to False.
            step_name (str, optional): The name of this transformation step. Defaults to "OneHotEncode".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.drop_original = drop_original
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the OneHotEncode transformation.

        Retrieves the DataFrame from the context, applies one-hot encoding to the specified column,
        concatenates the resulting dummy columns with the original DataFrame, optionally drops the original column,
        updates the context, and returns the context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with one-hot encoded columns.
        """
        df = context.dataframes[self.dataframe]
        dummies = pd.get_dummies(df[self.column], prefix=self.column)
        df = pd.concat([df, dummies], axis=1)
        if self.drop_original:
            df = df.drop(columns=[self.column])
        context.set_dataframe(self.dataframe, df)
        return context
