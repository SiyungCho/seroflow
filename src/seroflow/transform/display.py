"""
This module implements a suite of transformation classes that displays key information of a DataFrame.
Each transformation class extends the base ``Transformation`` class and is designed to operate on a specified DataFrame stored in the ``Pipeline`` context.
The available transformations include:

- **DisplayInfo**: Prints basic information (shape, columns, and data types) for each DataFrame.
- **DisplayColumns**: Prints the list of column names for each DataFrame.
- **DisplayHead**: Prints the first N rows of each DataFrame.
- **DisplayTail**: Prints the last N rows of each DataFrame.
- **DisplayColumnMean**: Displays the mean of a specified column for each DataFrame.
- **DisplayColumnMedian**: Displays the median of a specified column for each DataFrame.
- **DisplayColumnMode**: Displays the mode(s) of a specified column for each DataFrame.
- **DisplayColumnVariance**: Displays the variance of a specified column for each DataFrame.
- **DisplayColumnStdDev**: Displays the standard deviation of a specified column for each DataFrame.
- **DisplayColumnSum**: Displays the sum of a specified column for each DataFrame.
- **DisplayColumnMin**: Displays the minimum value of a specified column for each DataFrame.
- **DisplayColumnMax**: Displays the maximum value of a specified column for each DataFrame.
- **DisplayColumnCount**: Displays the count of non-null values in a specified column for each DataFrame.
- **DisplayColumnUnique**: Displays the unique values in a specified column for each DataFrame.
- **DisplayColumnNUnique**: Displays the number of unique values in a specified column for each DataFrame.
- **DisplayColumnDType**: Displays the data type of a specified column for each DataFrame.
- **DisplayStringCount**: Displays the value counts for a specified column in each DataFrame.
- **DisplayMostFrequentString**: Displays the most frequent item(s) in a specified column for each DataFrame.
- **DisplayAllCategories**: Displays all unique categories in a specified column for each DataFrame.
- **DisplaySubstringOccurrence**: Counts and displays the total occurrences of a substring in a specified column for each DataFrame.

It is important to note that these classes are purely visual and meant solely to view information.
Future versions will seek to store the display results into variables/log the display results via ``logging.logger``.
"""

#Need to configure to work with logger
#Need to have save_to_variable property
from .transformation import Transformation


class DisplayInfo(Transformation):
    """
    Prints general information about each DataFrame in the context, including its shape,
    column names, and data types.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayInfo``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayInfo

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers dataframes called 'states' and 'regions'

        display_info = DisplayInfo(dataframes=['states', 'regions']) # Initialize the DisplayInfo Step

        pipeline.add_steps([display_info])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
    """

    def __init__(self, dataframes, step_name="DisplayInfo"):
        """Initialize the ``DisplayInfo`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayInfo".
        """
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayInfo`` transformation.

        Iterates over each DataFrame in the context and prints its shape, columns,
        and data types.

        Args:
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
    Prints the list of column names for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumns``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumns

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'sales'

        display_columns = DisplayColumns(dataframes='sales')  # Initialize the DisplayColumns step

        pipeline.add_steps([display_columns])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
    """

    def __init__(self, dataframes, step_name="DisplayColumns"):
        """Initialize the ``DisplayColumns`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumns".
        """
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumns`` transformation.

        Iterates over each DataFrame in the context and prints its column names.

        Args:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"- DataFrame '{dataframe_name}' Columns: -")
            print(list(df.columns))
            print("-" * 50)


class DisplayHead(Transformation):
    """
    Prints the first N rows of each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayHead``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayHead

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'employees'

        display_head = DisplayHead(dataframes='employees', n=10)  # Initialize the DisplayHead step to show first 10 rows

        pipeline.add_steps([display_head])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        n (int): Number of rows to display from the top.
    """

    def __init__(self, dataframes, n=5, step_name="DisplayHead"):
        """Initialize the ``DisplayHead`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            n (int, optional): Number of rows to display from the top.
                Defaults to 5.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayHead".
        """
        self.n = n
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayHead`` transformation.

        Iterates over each DataFrame in the context and prints the first n rows.

        Args:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"------- DataFrame '{dataframe_name}' Head (first {self.n} rows): -------")
            print(df.head(self.n))
            print("-" * 50)

class DisplayTail(Transformation):
    """
    Prints the last N rows of each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayTail``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayTail

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'orders'

        display_tail = DisplayTail(dataframes='orders', n=5)  # Initialize the DisplayTail step

        pipeline.add_steps([display_tail])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        n (int): Number of rows to display from the bottom.
    """

    def __init__(self, dataframes, n=5, step_name="DisplayTail"):
        """Initialize the ``DisplayTail`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            n (int, optional): Number of rows to display from the bottom.
                Defaults to 5.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayTail".
        """
        self.n = n
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayTail`` transformation.

        Iterates over each DataFrame in the context and prints the last n rows.

        Args:
            context (Context): The context containing the DataFrames.
        """
        for dataframe_name, df in context.dataframes.items():
            print(f"-------- DataFrame '{dataframe_name}' Tail (last {self.n} rows): --------")
            print(df.tail(self.n))
            print("-" * 50)

class DisplayColumnMean(Transformation):
    """
    Displays the mean of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnMean``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnMean

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'metrics' with a 'score' column

        display_mean = DisplayColumnMean(dataframes='metrics', column='score')  # Initialize the DisplayColumnMean step

        pipeline.add_steps([display_mean])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the mean is to be computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnMean"):
        """Initialize the ``DisplayColumnMean`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the mean is to be computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnMean".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnMean`` transformation.

        Iterates over each DataFrame in the context, computes the mean of the specified column,
        and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if the column is not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnMedian(Transformation):
    """
    Displays the median of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnMedian``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnMedian

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'data' with a 'age' column

        display_median = DisplayColumnMedian(dataframes='data', column='age')  # Initialize the DisplayColumnMedian step

        pipeline.add_steps([display_median])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the median is to be computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnMedian"):
        """Initialize the ``DisplayColumnMedian`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the median is to be computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnMedian".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnMedian`` transformation.

        Iterates over each DataFrame in the context, computes the median of the specified column,
        and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if the column is not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnMode(Transformation):
    """
    Displays the mode(s) of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnMode``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnMode

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'survey' with a 'response' column

        display_mode = DisplayColumnMode(dataframes='survey', column='response')  # Initialize the DisplayColumnMode step

        pipeline.add_steps([display_mode])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the mode is to be computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnMode"):
        """Initialize the DisplayColumnMode transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the mode is to be computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnMode".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnMode`` transformation.

        Iterates over each DataFrame in the context, computes the mode(s) of the specified column,
        and prints the results as a list.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnVariance(Transformation):
    """
    Displays the variance of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnVariance``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnVariance

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'finance' with a 'revenue' column

        display_variance = DisplayColumnVariance(dataframes='finance', column='revenue')  # Initialize the DisplayColumnVariance step

        pipeline.add_steps([display_variance])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the variance is computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnVariance"):
        """Initialize the ``DisplayColumnVariance`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which variance is computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnVariance".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnVariance`` transformation.

        Iterates over each DataFrame in the context, computes the variance of the specified column,
        and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnStdDev(Transformation):
    """
    Displays the standard deviation of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnStdDev``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnStdDev

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'stats' with a 'duration' column

        display_stddev = DisplayColumnStdDev(dataframes='stats', column='duration')  # Initialize the DisplayColumnStdDev step

        pipeline.add_steps([display_stddev])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the standard deviation is computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnStdDev"):
        """Initialize the ``DisplayColumnStdDev`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column or index for which standard deviation is computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnStdDev".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnStdDev`` transformation.

        Iterates over each DataFrame in the context, computes the standard deviation of the specified
        column, and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnSum(Transformation):
    """
    Displays the sum of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnSum``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnSum

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'transactions' with a 'amount' column

        display_sum = DisplayColumnSum(dataframes='transactions', column='amount')  # Initialize the DisplayColumnSum step

        pipeline.add_steps([display_sum])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the sum is computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnSum"):
        """Initialize the ``DisplayColumnSum`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the sum is computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnSum".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnSum`` transformation.

        Iterates over each DataFrame in the context, computes the sum of the specified column,
        and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnMin(Transformation):
    """
    Displays the minimum value of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnMin``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnMin

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'inventory' with a 'price' column

        display_min = DisplayColumnMin(dataframes='inventory', column='price')  # Initialize the DisplayColumnMin step

        pipeline.add_steps([display_min])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the minimum is computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnMin"):
        """Initialize the ``DisplayColumnMin`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the minimum value is computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnMin".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnMin`` transformation.

        Iterates over each DataFrame in the context, computes the minimum of the specified column,
        and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnMax(Transformation):
    """
    Displays the maximum value of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnMax``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnMax

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'inventory' with a 'price' column

        display_max = DisplayColumnMax(dataframes='inventory', column='price')  # Initialize the DisplayColumnMax step

        pipeline.add_steps([display_max])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the maximum is computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnMax"):
        """Initialize the ``DisplayColumnMax`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column or index for which the maximum value is computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnMax".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnMax`` transformation.

        Iterates over each DataFrame in the context, computes the maximum of the specified column,
        and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column

class DisplayColumnCount(Transformation):
    """
    Displays the count of non-null values in a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnCount``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnCount

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'customers' with a 'email' column

        display_count = DisplayColumnCount(dataframes='customers', column='email')  # Initialize the DisplayColumnCount step

        pipeline.add_steps([display_count])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which the count is computed.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnCount"):
        """Initialize the ``DisplayColumnCount`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which the count is computed.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnCount".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnCount`` transformation.

        Iterates over each DataFrame in the context, computes the count of non-null values
        in the specified column, and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnUnique(Transformation):
    """
    Displays the unique values present in a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnUnique``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnUnique

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'logs' with a 'user_id' column

        display_unique = DisplayColumnUnique(dataframes='logs', column='user_id')  # Initialize the DisplayColumnUnique step

        pipeline.add_steps([display_unique])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index to retrieve unique values from.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnUnique"):
        """Initialize the ``DisplayColumnUnique`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index from which to retrieve unique values.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnUnique".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnUnique`` transformation.

        Iterates over each DataFrame in the context, retrieves the unique values from the
        specified column, and prints them as a list.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnNUnique(Transformation):
    """
    Displays the number of unique values in a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnNUnique``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnNUnique

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'responses' with a 'answer' column

        display_nunique = DisplayColumnNUnique(dataframes='responses', column='answer')  # Initialize the DisplayColumnNUnique step

        pipeline.add_steps([display_nunique])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which to count unique values.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnNUnique"):
        """Initialize the ``DisplayColumnNUnique`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to count unique values.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnNUnique".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnNUnique`` transformation.

        Iterates over each DataFrame in the context, computes the number of unique values
        in the specified column, and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayColumnDType(Transformation):
    """
    Displays the data type of a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayColumnDType``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayColumnDType

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'records' with a 'date' column

        display_dtype = DisplayColumnDType(dataframes='records', column='date')  # Initialize the DisplayColumnDType step

        pipeline.add_steps([display_dtype])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which to display the data type.
    """

    def __init__(self, dataframes, column, step_name="DisplayColumnDType"):
        """Initialize the ``DisplayColumnDType`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to display the data type.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayColumnDType".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayColumnDType`` transformation.

        Iterates over each DataFrame in the context, retrieves the data type of the
        specified column, and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayStringCount(Transformation):
    """
    Displays the frequency count of unique string values in a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayStringCount``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayStringCount

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'reviews' with a 'comment' column

        display_string_count = DisplayStringCount(dataframes='reviews', column='comment')  # Initialize the DisplayStringCount step

        pipeline.add_steps([display_string_count])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which to display value counts.
    """

    def __init__(self, dataframes, column, step_name="DisplayStringItemCount"):
        """Initialize the ``DisplayStringCount`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to display value counts.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayStringItemCount".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayStringCount`` transformation.

        Iterates over each DataFrame in the context, computes value counts for the
        specified column, and prints the counts.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayMostFrequentString(Transformation):
    """
    Displays the most frequent string(s) in a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayMostFrequentString``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayMostFrequentString

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'feedback' with a 'rating' column

        display_most_frequent = DisplayMostFrequentString(dataframes='feedback', column='rating')  # Initialize the DisplayMostFrequentString step

        pipeline.add_steps([display_most_frequent])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index for which to display the most frequent string(s).
    """

    def __init__(self, dataframes, column, step_name="DisplayMostFrequentString"):
        """Initialize the ``DisplayMostFrequentString`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index for which to display the most frequent string(s).
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayMostFrequentString".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayMostFrequentString`` transformation.

        Iterates over each DataFrame in the context, computes the mode of the specified column,
        and prints the most frequent string(s).

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplayAllCategories(Transformation):
    """
    Displays all unique categories present in a specified column for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplayAllCategories``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplayAllCategories

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'products' with a 'category' column

        display_categories = DisplayAllCategories(dataframes='products', column='category')  # Initialize the DisplayAllCategories step

        pipeline.add_steps([display_categories])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index from which to retrieve unique categories.
    """

    def __init__(self, dataframes, column, step_name="DisplayAllCategories"):
        """Initialize the ``DisplayAllCategories`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index from which to retrieve unique categories.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplayAllCategories".
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplayAllCategories`` transformation.

        Iterates over each DataFrame in the context, retrieves unique values from the
        specified column, and prints them.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column


class DisplaySubstringOccurrence(Transformation):
    """
    Counts and displays the total number of occurrences of a specified substring in a given column
    for each DataFrame in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DisplaySubstringOccurrence``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DisplaySubstringOccurrence

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'logs' with a 'message' column

        display_substring = DisplaySubstringOccurrence(dataframes='logs', column='message', substring='error')  # Initialize the DisplaySubstringOccurrence step 

        pipeline.add_steps([display_substring])
        pipeline.execute()

    Attributes:
        dataframes (str or list): The name(s) of the DataFrame(s) in the context.
        column (str or int): The column name or index in which to count substring occurrences.
        substring (str): The substring to count.
    """

    def __init__(self, dataframes, column, substring, step_name="DisplaySubstringOccurrence"):
        """Initialize the ``DisplaySubstringOccurrence`` transformation.

        Args:
            dataframes (str or list): The name(s) of the DataFrame(s) in the context.
            column (str or int): The column name or index in which to count substring occurrences.
            substring (str): The substring to count.
            step_name (str, optional): The name of this transformation step.
                Defaults to "DisplaySubstringOccurrence".
        """
        self.column = column
        self.substring = substring
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        """Execute the ``DisplaySubstringOccurrence`` transformation.

        Iterates over each DataFrame in the context, counts the total occurrences of the specified substring
        in the designated column, and prints the result.

        Args:
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
        """Resolve the column name from the provided column identifier.

        Args:
            df (DataFrame): The DataFrame to check.

        Returns:
            str: The resolved column name, or None if not found.
        """
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
