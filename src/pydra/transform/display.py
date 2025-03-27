"""
Module: display.py

This module implements a variety of transformations for displaying information about DataFrames.
These transformations are primarily used for debugging and exploratory data analysis.
They print various aspects of a DataFrame, including its shape, column names, data types,
head, tail, and statistical summaries. Each transformation class extends the base Transformation 
class and is designed to operate on one or more DataFrames stored in the Pipeline context.
 
Classes:
    DisplayInfo: Prints basic information (shape, columns, and data types) for DataFrame.
    DisplayColumns: Prints the list of column names for DataFrame.
    DisplayHead: Prints the first N rows of DataFrame.
    DisplayTail: Prints the last N rows of DataFrame.
    DisplayColumnMean: Displays the mean of a specified column for DataFrame.
    DisplayColumnMedian: Displays the median of a specified column for DataFrame.
    DisplayColumnMode: Displays the mode(s) of a specified column for DataFrame.
    DisplayColumnVariance: Displays the variance of a specified column for DataFrame.
    DisplayColumnStdDev: Displays the standard deviation of a specified column for DataFrame.
    DisplayColumnSum: Displays the sum of a specified column for DataFrame.
    DisplayColumnMin: Displays the minimum value of a specified column for DataFrame.
    DisplayColumnMax: Displays the maximum value of a specified column for DataFrame.
    DisplayColumnCount: Displays the count of non-null values in a specified column for DataFrame.
    DisplayColumnUnique: Displays the unique values in a specified column for DataFrame.
    DisplayColumnNUnique: Displays the number of unique values in a specified column
                          for DataFrame.
    DisplayColumnDType: Displays the data type of a specified column for DataFrame.
    DisplayStringCount: Displays the value counts for a specified column in DataFrame.
    DisplayMostFrequentString: Displays the most frequent item(s) in a specified column
                               for DataFrame.
    DisplayAllCategories: Displays all unique categories in a specified column for DataFrame.
    DisplaySubstringOccurrence: Counts and displays occurrences of substring in a specified
                                column for DataFrame.
"""

#Need to configure to work with logger
#Need to have save_to_variable property

from .transformation import Transformation

class DisplayInfo(Transformation):
    """
    DisplayInfo

    Prints general information about each DataFrame in the context, including its shape,
    column names, and data types.
    """
    def __init__(self,
                 dataframes,
                 step_name="DisplayInfo"):
        """
        Initializes the DisplayInfo transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayInfo".
        """
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayInfo transformation.

        Iterates over each DataFrame in the context and prints its shape, columns,
        and data types.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"- Info for DataFrame '{dataframe_name}' -")
            print(f"Shape: {df.shape}")
            print("Columns and Data Types:")
            print(df.dtypes)
            print("-" * 50)

class DisplayColumns(Transformation):
    """
    DisplayColumns

    Prints the list of column names for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 step_name="DisplayColumns"):
        """
        Initializes the DisplayColumns transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumns".
        """
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumns transformation.

        Iterates over each DataFrame in the context and prints its column names.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"- DataFrame '{dataframe_name}' Columns: -")
            print(list(df.columns))
            print("-" * 50)

class DisplayHead(Transformation):
    """
    DisplayHead

    Prints the first N rows of each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 n=5,
                 step_name="DisplayHead"):
        """
        Initializes the DisplayHead transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            n (int, optional): Number of rows to display from the top. Defaults to 5.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayHead".
        """
        self.n = n
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayHead transformation.

        Iterates over each DataFrame in the context and prints the first n rows.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"------- DataFrame '{dataframe_name}' Head (first {self.n} rows): -------")
            print(df.head(self.n))
            print("-" * 50)

class DisplayTail(Transformation):
    """
    DisplayTail

    Prints the last N rows of each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 n=5,
                 step_name="DisplayTail"):
        """
        Initializes the DisplayTail transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            n (int, optional): Number of rows to display from the bottom.
                               Defaults to 5.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayTail".
        """
        self.n = n
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayTail transformation.

        Iterates over each DataFrame in the context and prints the last n rows.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"-------- DataFrame '{dataframe_name}' Tail (last {self.n} rows): --------")
            print(df.tail(self.n))
            print("-" * 50)

class DisplayColumnMean(Transformation):
    """
    DisplayColumnMean

    Displays the mean of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnMean"):
        """
        Initializes the DisplayColumnMean transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the mean is to be computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnMean".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnMean transformation.

        Iterates over each DataFrame in the context, computes the mean of the specified column,
        and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"---- [{dataframe_name}] Column '{self.column}' not found. ----")
            else:
                mean_value = df[col_name].mean()
                print(f"---- [{dataframe_name}] Mean of column '{col_name}': {mean_value} ----")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if the column is not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnMedian(Transformation):
    """
    DisplayColumnMedian

    Displays the median of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnMedian"):
        """
        Initializes the DisplayColumnMedian transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the median is to be computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnMedian".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnMedian transformation.

        Iterates over each DataFrame in the context, computes the median of the specified
        column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"--- [{dataframe_name}] Column '{self.column}' not found. ---")
            else:
                median_value = df[col_name].median()
                print(f"--- [{dataframe_name}] Median of column '{col_name}': {median_value} ---")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if the column is not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnMode(Transformation):
    """
    DisplayColumnMode

    Displays the mode(s) of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnMode"):
        """
        Initializes the DisplayColumnMode transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the mode is to be computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnMode".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnMode transformation.

        Iterates over each DataFrame in the context, computes the mode(s) of the specified
        column, and prints the results as a list.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"--- [{dataframe_name}] Column '{self.column}' not found. ---")
            else:
                mode_series = df[col_name].mode()
                print(f"--- [{dataframe_name}] Mode of column '{col_name}': {list(mode_series)} ---")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnVariance(Transformation):
    """
    DisplayColumnVariance

    Displays the variance of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnVariance"):
        """
        Initializes the DisplayColumnVariance transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which variance is computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnVariance".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnVariance transformation.

        Iterates over each DataFrame in the context, computes the variance of the specified
        column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                variance_value = df[col_name].var()
                print(f"- [{dataframe_name}] Variance of column '{col_name}': {variance_value} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnStdDev(Transformation):
    """
    DisplayColumnStdDev

    Displays the standard deviation of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnStdDev"):
        """
        Initializes the DisplayColumnStdDev transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column or index for which standard deviation is computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnStdDev".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnStdDev transformation.

        Iterates over each DataFrame in the context, computes the standard deviation of
        the specified column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                std_dev = df[col].std()
                print(f"- [{dataframe_name}] Standard Deviation of column '{col}': {std_dev} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnSum(Transformation):
    """
    DisplayColumnSum

    Displays the sum of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnSum"):
        """
        Initializes the DisplayColumnSum transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the sum is computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnSum".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnSum transformation.

        Iterates over each DataFrame in the context, computes the sum of the specified column,
        and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                col_sum = df[col].sum()
                print(f"- [{dataframe_name}] Sum of column '{col}': {col_sum} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnMin(Transformation):
    """
    DisplayColumnMin

    Displays the minimum value of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnMin"):
        """
        Initializes the DisplayColumnMin transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the minimum value is computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnMin".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnMin transformation.

        Iterates over each DataFrame in the context, computes the minimum of the specified
        column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                col_min = df[col].min()
                print(f"- [{dataframe_name}] Minimum of column '{col}': {col_min} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnMax(Transformation):
    """
    DisplayColumnMax

    Displays the maximum value of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnMax"):
        """
        Initializes the DisplayColumnMax transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column or index for which the maximum value is computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnMax".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnMax transformation.

        Iterates over each DataFrame in the context, computes the maximum of the specified
        column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                col_max = df[col].max()
                print(f"- [{dataframe_name}] Maximum of column '{col}': {col_max} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnCount(Transformation):
    """
    DisplayColumnCount

    Displays the count of non-null values in a specified column for each DataFrame in the
    context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnCount"):
        """
        Initializes the DisplayColumnCount transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the count is computed.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnCount".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnCount transformation.

        Iterates over each DataFrame in the context, computes the count of non-null values
        in the specified column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{df_name}] Column '{self.column}' not found. -")
            else:
                count_val = df[col].count()
                print(f"- [{df_name}] Count (non-null) for column '{col}': {count_val} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnUnique(Transformation):
    """
    DisplayColumnUnique

    Displays the unique values present in a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnUnique"):
        """
        Initializes the DisplayColumnUnique transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index to retrieve unique values from.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnUnique".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnUnique transformation.

        Iterates over each DataFrame in the context, retrieves the unique values from the
        specified column, and prints them as a list.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{df_name}] Column '{self.column}' not found. -")
            else:
                unique_vals = df[col].unique()
                print(f"- [{df_name}] Unique values in column '{col}': {list(unique_vals)} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnNUnique(Transformation):
    """
    DisplayColumnNUnique

    Displays the number of unique values in a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnNUnique"):
        """
        Initializes the DisplayColumnNUnique transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to count unique values.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnNUnique".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnNUnique transformation.

        Iterates over each DataFrame in the context, computes the number of unique values
        in the specified column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{df_name}] Column '{self.column}' not found. -")
            else:
                n_unique = df[col].nunique()
                print(f"- [{df_name}] Number of unique values in column '{col}': {n_unique} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnDType(Transformation):
    """
    DisplayColumnDType

    Displays the data type of a specified column for each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayColumnDType"):
        """
        Initializes the DisplayColumnDType transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to display the data type.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayColumnDType".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayColumnDType transformation.

        Iterates over each DataFrame in the context, retrieves the data type of the
        specified column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{df_name}] Column '{self.column}' not found. -")
            else:
                dtype_val = df[col].dtype
                print(f"- [{df_name}] Data type for column '{col}': {dtype_val} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayStringCount(Transformation):
    """
    DisplayStringCount

    Displays the frequency count of unique string values in a specified column for
    each DataFrame in the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayStringItemCount"):
        """
        Initializes the DisplayStringCount transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to display value counts.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayStringItemCount".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayStringCount transformation.

        Iterates over each DataFrame in the context, computes value counts for the
        specified column, and prints the counts.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                counts = df[col].value_counts()
                print(f"- [{dataframe_name}] Value counts for column '{col}': -")
                print(counts)

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayMostFrequentString(Transformation):
    """
    DisplayMostFrequentString

    Displays the most frequent string(s) in a specified column for each DataFrame in
    the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayMostFrequentString"):
        """
        Initializes the DisplayMostFrequentString transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to display the most
                                 frequent string(s).
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayMostFrequentString".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayMostFrequentString transformation.

        Iterates over each DataFrame in the context, computes the mode of the specified column,
        and prints the most frequent string(s).

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                mode_series = df[col].mode()
                if mode_series.empty:
                    print(f"- [{dataframe_name}] No mode found for column '{col}'. -")
                else:
                    print(f"- [{dataframe_name}] Most frequent in '{col}': {list(mode_series)} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayAllCategories(Transformation):
    """
    DisplayAllCategories

    Displays all unique categories present in a specified column for each DataFrame in
    the context.
    """
    def __init__(self,
                 dataframes,
                 column,
                 step_name="DisplayAllCategories"):
        """
        Initializes the DisplayAllCategories transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index from which to retrieve unique
                                 categories.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplayAllCategories".
        """
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplayAllCategories transformation.

        Iterates over each DataFrame in the context, retrieves unique values from the
        specified column, and prints them.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                categories = df[col].unique()
                print(f"- [{dataframe_name}] Unique categories in '{col}': {list(categories)} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplaySubstringOccurrence(Transformation):
    """
    DisplaySubstringOccurrence

    Counts and displays the total number of occurrences of a specified substring in a
    given column for each DataFrame.
    """
    def __init__(self,
                 dataframes,
                 column,
                 substring,
                 step_name="DisplaySubstringOccurrence"):
        """
        Initializes the DisplaySubstringOccurrence transformation.

        Arguments:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index in which to count substring occurrences.
            substring (str): The substring to count.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DisplaySubstringOccurrence".
        """
        self.column = column
        self.substring = substring
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframes)

    def func(self, context):
        """
        Executes the DisplaySubstringOccurrence transformation.

        Iterates over each DataFrame in the context, counts the total occurrences of the
        specified substring in the designated column, and prints the result.

        Arguments:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"- [{dataframe_name}] Column '{self.column}' not found. -")
            else:
                count = df[col].astype(str).apply(lambda x: x.count(self.substring)).sum()
                print(f"- [{dataframe_name}] Occurrences '{self.substring}' in '{col}': {count} -")

    def __resolve_column(self, df):
        """
        Resolves the column name from the provided column identifier.

        Arguments:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
