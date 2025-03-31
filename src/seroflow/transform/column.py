"""
This module implements a collection of transformation classes that perform various column operations on DataFrames.
These transformations update the DataFrame stored in the ``Pipeline`` context.
Each transformation class extends the base ``Transformation`` class and provides a specific column operation.

- **ConvertColumnType**: Converts a specified column of a DataFrame to a new data type.
- **RenameColumns**: Renames one or more columns based on a provided mapping.
- **DropColumn**: Drops a single specified column from a DataFrame.
- **DropColumns**: Drops multiple specified columns from a DataFrame.
- **AddColumn**: Adds a new column to a DataFrame computed from a function.
- **MergeColumns**: Merges multiple columns into a single column by concatenating their string representations.
- **SplitColumn**: Splits a single column into multiple new columns based on a delimiter.
- **ExplodeColumn**: Explodes a column containing list-like elements into multiple rows.
- **CreateColumnFromVariable**: Creates a new column in a DataFrame using a constant value provided via a variable.

Each transformation retrieves the target DataFrame from the ``Pipeline`` context, performs the operation, updates the DataFrame, and returns the modified context.
"""

import pandas as pd
from .transformation import Transformation

class ConvertColumnType(Transformation):
    """
    Converts a specified column of a DataFrame to a new data type.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``ConvertColumnType``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import ConvertColumnType

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'sales_data' with a 'price' column

        convert_col_type = ConvertColumnType(column="price", dataframe="sales_data", new_type=int) # Initialize the ConvertColumnType to convert the 'price' column to type 'int'

        pipeline.add_steps([convert_col_type])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The column to be converted.
        new_type (type): The target data type to convert the column to.
    """
    def __init__(self,
                 dataframe,
                 column,
                 new_type,
                 step_name="ConvertColumnType",
                 on_error=None):
        """
        Initializes the ``ConvertColumnType`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            column (str): The name of the column whose type is to be converted.
            new_type (type): The target data type for the column.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "ConvertColumnType".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.new_type = new_type
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the conversion of the column type.

        Retrieves the DataFrame from the context, converts the specified column to the new type,
        updates the DataFrame in the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the converted column.
        """
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__convert_column_type(df, self.column, self.new_type)
        context.set_dataframe(self.dataframe, df)
        return context

    def __convert_column_type(self, df, column, new_type):
        """
        Converts the specified column to the new data type.

        Arguments:
            df (DataFrame): The DataFrame containing the column.
            column (str): The column to convert.
            new_type (type): The target data type.

        Returns:
            Series: The converted column.
        """
        return df[column].astype(new_type)


class RenameColumns(Transformation):
    """
    Renames one or more columns in a DataFrame based on a provided mapping.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``RenameColumns``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import RenameColumns

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads a DataFrame called 'sales_data' with 'price' and 'quantity' columns

        rename_columns = RenameColumns(dataframe="sales_data", columns_mapping={"price": "unit_price", "quantity": "units_sold"})  # Initialize RenameColumns to rename 'price' → 'unit_price' and 'quantity' → 'units_sold'

        pipeline.add_steps([rename_columns])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        columns_mapping (dict): A dictionary mapping current column names to new column names.
    """
    def __init__(self,
                 dataframe,
                 columns_mapping,
                 step_name="RenameColumns",
                 on_error=None):
        """
        Initializes the ``RenameColumns`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            columns_mapping (dict): Mapping of existing column names to new names.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "RenameColumns".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.columns_mapping = columns_mapping
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the column renaming transformation.

        Retrieves the DataFrame from the context, renames the columns based on the mapping,
        updates the DataFrame in the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with renamed columns.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__rename_columns(df))
        return context

    def __rename_columns(self, df):
        """
        Renames columns in the DataFrame based on the mapping.

        Arguments:
            df (DataFrame): The DataFrame whose columns are to be renamed.

        Returns:
            DataFrame: The DataFrame with renamed columns.
        """
        # inplace renaming returns None, so we perform renaming and then return the DataFrame.
        df.rename(columns=self.columns_mapping, inplace=True)
        return df


class DropColumn(Transformation):
    """
    Drops a specified column from a DataFrame.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DropColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DropColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

        drop_column = DropColumn(column="price", dataframe="sales_data")  # Initialize DropColumn to drop the 'price' column

        pipeline.add_steps([drop_column])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column to drop.
    """
    def __init__(self,
                 dataframe,
                 column,
                 step_name="DropColumn",
                 on_error=None):
        """
        Initializes the ``DropColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            column (str): The column to drop.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "DropColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``DropColumn`` transformation.

        Retrieves the DataFrame from the context, drops the specified column,
        updates the DataFrame in the context, and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the column dropped.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__drop_column(df))
        return context

    def __drop_column(self, df):
        """
        Drops the specified column from the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to modify.
        
        Returns:
            DataFrame: The DataFrame after dropping the column.
        """
        return df.drop(columns=[self.column])


class DropColumns(Transformation):
    """
    Drops multiple specified columns from a DataFrame.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DropColumns``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DropColumns

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'price' and 'quantity' columns

        drop_columns = DropColumns(columns=["price", "quantity"], dataframe="sales_data")  # Initialize DropColumns to drop both 'price' and 'quantity'

        pipeline.add_steps([drop_columns])
        pipeline.execute()


    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        columns (list): A list of columns to drop.
    """
    def __init__(self,
                 dataframe,
                 columns,
                 step_name="DropColumns",
                 on_error=None):
        """
        Initializes the ``DropColumns`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            columns (list): A list of column names to drop.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "DropColumns".
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
        Executes the ``DropColumns`` transformation.

        Retrieves the DataFrame from the context, drops the specified columns
        (ignoring errors if columns are missing), updates the DataFrame in the context,
        and returns the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the specified columns dropped.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__drop_columns(df))
        return context

    def __drop_columns(self, df):
        """
        Drops the specified columns from the DataFrame, ignoring errors if column does not exist.

        Arguments:
            df (DataFrame): The DataFrame to modify.
        
        Returns:
            DataFrame: The DataFrame after dropping the columns.
        """
        return df.drop(columns=self.columns, errors='ignore')


class AddColumn(Transformation):
    """
    Adds a new column to a DataFrame computed from a provided function.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``AddColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import AddColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'price' and 'quantity' columns

        add_column = AddColumn(
            column="total_sales",
            dataframe="sales_data",
            compute_func=lambda df: df["price"] * df["quantity"]
        )  # Initialize AddColumn to create 'total_sales' by multiplying 'price' × 'quantity'

        pipeline.add_steps([add_column])
        pipeline.execute()
    
    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the new column to add.
        compute_func (function): A function that computes the new column's values from DataFrame.
    """
    def __init__(self,
                 dataframe,
                 column,
                 compute_func,
                 step_name="AddColumn",
                 on_error=None):
        """
        Initializes the ``AddColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            column (str): The name of the new column to add.
            compute_func (function): A function that accepts a DataFrame and returns a
                                     Series representing the new column.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "AddColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.compute_func = compute_func
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``AddColumn`` transformation.

        Retrieves the DataFrame from the context, computes the new column values using
        compute_func, adds the new column to the DataFrame, updates the context, and returns it.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the new column added.
        """
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__compute_column(df)
        context.set_dataframe(self.dataframe, df)
        return context

    def __compute_column(self, df):
        """
        Computes the new column using the provided compute function.

        Arguments:
            df (DataFrame): The DataFrame to use for computation.

        Returns:
            Series: The computed column as a pandas Series.
        """
        return self.compute_func(df)


class MergeColumns(Transformation):
    """
    Merges multiple columns into a single column by concatenating their string
    representations using a specified separator.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``MergeColumns``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import MergeColumns

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'first_name' and 'last_name' columns

        merge_columns = MergeColumns(
            columns=["first_name", "last_name"],
            new_column="full_name",
            dataframe="sales_data",
            separator=" "
        )  # Initialize MergeColumns to concatenate first_name and last_name into 'full_name'

        pipeline.add_steps([merge_columns])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        columns (list): The list of column names to merge.
        new_column (str): The name of the new merged column.
        separator (str): The string used to separate the merged values.
    """
    def __init__(self,
                 dataframe,
                 columns,
                 new_column,
                 separator=" ",
                 step_name="MergeColumns",
                 on_error=None):
        """
        Initializes the ``MergeColumns`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            columns (list): A list of column names to merge.
            new_column (str): The name of the new column that will contain the merged values.
            separator (str, optional): The separator to use between merged column values.
                                       Defaults to a space.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "MergeColumns".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.columns = columns
        self.new_column = new_column
        self.separator = separator
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``MergeColumns`` transformation.

        Retrieves the DataFrame from the context, merges the specified columns by concatenating
        their string representations, adds the new merged column to the DataFrame, updates
        the context, and returns it.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the merged column.
        """
        df = context.dataframes[self.dataframe]
        df[self.new_column] = self.__merge_columns(df)
        context.set_dataframe(self.dataframe, df)
        return context

    def __merge_columns(self, df):
        """
        Merges the specified columns by concatenating their string representations.

        Arguments:
            df (DataFrame): The DataFrame containing the columns.

        Returns:
            Series: A Series with the merged column values.
        """
        return df[self.columns].astype(str).agg(self.separator.join, axis=1)


class SplitColumn(Transformation):
    """
    Splits a single column in a DataFrame into multiple new columns based on a delimiter.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``SplitColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import SplitColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'full_name' column

        split_column = SplitColumn(
            column="full_name",
            new_columns=["first_name", "last_name"],
            dataframe="sales_data",
            delimiter=" "
        )  # Initialize SplitColumn to split 'full_name' into 'first_name' and 'last_name'

        pipeline.add_steps([split_column])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column to split.
        new_columns (list): The list of new column names to create.
        delimiter (str): The delimiter used to split the column's values.
    """
    def __init__(self,
                 dataframe,
                 column,
                 new_columns,
                 delimiter=" ",
                 step_name="SplitColumn",
                 on_error=None):
        """
        Initializes the ``SplitColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            column (str): The name of the column to split.
            new_columns (list): A list of new column names to assign to the split parts.
            delimiter (str, optional): The delimiter used to split the column values.
                                       Defaults to a space.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "SplitColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.new_columns = new_columns
        self.delimiter = delimiter
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``SplitColumn`` transformation.

        Retrieves the DataFrame from the context, splits the specified column using the
        delimiter, assigns the resulting parts to new columns, concatenates them with the
        original DataFrame, updates the context, and returns it.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the split columns added.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__split_column(df))
        return context

    def __split_column(self, df):
        """
        Splits the specified column into multiple columns.

        Arguments:
            df (DataFrame): The DataFrame containing the column.

        Returns:
            DataFrame: The DataFrame with the new split columns concatenated.
        """
        splits = df[self.column].str.split(self.delimiter, expand=True)
        splits.columns = self.new_columns
        df = pd.concat([df, splits], axis=1)
        return df


class ExplodeColumn(Transformation):
    """
    Explodes a column containing list-like elements into multiple rows, duplicating the other
    column values.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``ExplodeColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import ExplodeColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'tags' column containing lists

        explode_column = ExplodeColumn(column="tags", dataframe="sales_data")  # Initialize ExplodeColumn to expand each list in 'tags' into separate rows

        pipeline.add_steps([explode_column])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column to explode.
    """
    def __init__(self,
                 dataframe,
                 column,
                 step_name="ExplodeColumn",
                 on_error=None):
        """
        Initializes the ``ExplodeColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            column (str): The name of the column to explode.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "ExplodeColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``ExplodeColumn`` transformation.

        Retrieves the DataFrame from the context, explodes the specified column,
        updates the DataFrame in the context, and returns the updated context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the exploded column.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__explode_column(df))
        return context

    def __explode_column(self, df):
        """
        Explodes the specified column into multiple rows.

        Arguments:
            df (DataFrame): The DataFrame containing the column.

        Returns:
            DataFrame: The DataFrame after exploding the column.
        """
        return df.explode(self.column)


class CreateColumnFromVariable(Transformation):
    """
    Creates a new column in a DataFrame with a constant value derived from a variable.
    This transformation is used to add a new column whose values are all set to the provided
    variable's value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``CreateColumnFromVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import CreateColumnFromVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ...  # Extractor loads 'sales_data'

        create_column = CreateColumnFromVariable(column="region", dataframe="sales_data", variable="North_America")  # Initialize CreateColumnFromVariable to add a 'region' column with constant value 'North America'

        pipeline.add_steps([create_column])
        pipeline.execute()


    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the new column to be created.
        variable: The constant value to assign to the new column.
    """
    def __init__(self,
                 dataframe,
                 column,
                 variable,
                 step_name="CreateColumnFromVariable",
                 on_error=None):
        """
        Initializes the ``CreateColumnFromVariable`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update.
            column (str): The name of the new column to create.
            variable: The constant value to assign to the new column.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "CreateColumnFromVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.variable = variable
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, context, **kwargs):
        """
        Executes the ``CreateColumnFromVariable`` transformation.

        Retrieves the DataFrame from the context, creates a new column with the constant
        value provided by the variable, updates the DataFrame in the context, and returns
        the modified context.

        Arguments:
            context (Context): The context containing the DataFrame.
            **kwargs: Keyword arguments that should include the variable value.

        Returns:
            Context: The updated context with the new column added.
        """
        df = context.dataframes[self.dataframe]
        df[self.column] = kwargs[self.variable]
        context.set_dataframe(self.dataframe, df)
        return context
