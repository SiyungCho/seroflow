"""
This module implements a suite of transformation classes that can manipulate internal DataFrames within the ``Pipeline`` Context.
Each transformation class extends the base ``Transformation`` class and is designed to operate with ``Pipeline`` Object.
The available transformations include:

- **AddDataFrame**: Adds a new DataFrame to the context.
- **DeleteDataFrame**: Deletes a DataFrame from the context.
- **RenameDataFrame**: Renames an existing DataFrame in the context.
- **CopyDataFrame**: Creates a copy of an existing DataFrame under a new name.
"""

from .transformation import Transformation

class AddDataFrame(Transformation):
    """
    A transformation that adds a new DataFrame to the ``Pipeline`` context. The DataFrame is
    stored in the context under the specified name.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``AddDataFrame``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import AddDataFrame

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        df = pd.DataFrame(...)

        add_df = AddDataFrame(dataframe=df, name="new_df") # Initialize the AddDataFrame Step

        pipeline.add_steps([add_df])
        pipeline.execute()

    Attributes:
        dataframe (DataFrame): The DataFrame to be added.
        name (str): The name under which the DataFrame will be stored in the context.
    """

    def __init__(self, dataframe, name, step_name="AddDataFrame", on_error=None):
        """Initialize a new ``AddDataFrame`` transformation.

        Args:
            dataframe (DataFrame): The DataFrame to be added.
            name (str): The name under which the DataFrame will be stored in the context.
            step_name (str, optional): The name of the transformation step.
                Defaults to "AddDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.name = name
        super().__init__(step_name=step_name, func=self.func, on_error=on_error)

    def func(self, context):
        """Execute the ``AddDataFrame`` transformation.

        Adds the specified DataFrame to the context under the provided name.

        Args:
            context (Context): The context object where the DataFrame will be added.

        Returns:
            Context: The updated context with the new DataFrame.
        """
        context.add_dataframe(self.name, self.dataframe)
        return context


class DeleteDataFrame(Transformation):
    """
    A transformation that deletes a DataFrame from the ``Pipeline`` context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DeleteDataFrame``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DeleteDataFrame

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        del_df = DeleteDataFrame(dataframe="df1") # Initialize the DeleteDataFrame Step

        pipeline.add_steps([del_df])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame to be deleted from the context.
    """

    def __init__(self, dataframe, step_name="DeleteDataFrame", on_error=None):
        """Initialize a new ``DeleteDataFrame`` transformation.

        Args:
            dataframe (str): The name of the DataFrame to be deleted from the context.
            step_name (str, optional): The name of the transformation step.
                Defaults to "DeleteDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)

    def func(self, context):
        """Execute the ``DeleteDataFrame`` transformation.

        Deletes the specified DataFrame from the context.

        Args:
            context (Context): The context object containing the DataFrame.

        Returns:
            Context: The updated context with the DataFrame removed.
        """
        del context.dataframes[self.dataframe]
        return context


class RenameDataFrame(Transformation):
    """
    A transformation that renames a DataFrame within the ``Pipeline`` context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``RenameDataFrame``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import RenameDataFrame

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        rename_df = RenameDataFrame(old_name="sales", new_name="updated_sale") # Initialize the RenameDataFrame Step

        pipeline.add_steps([rename_df])
        pipeline.execute()


    Attributes:
        old_name (str): The current name of the DataFrame in the context.
        new_name (str): The new name to assign to the DataFrame.
    """

    def __init__(self, old_name, new_name, step_name="RenameDataFrame", on_error=None):
        """Initialize a new ``RenameDataFrame`` transformation.

        Args:
            old_name (str): The current name of the DataFrame in the context.
            new_name (str): The new name to assign to the DataFrame.
            step_name (str, optional): The name of the transformation step.
                Defaults to "RenameDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.old_name = old_name
        self.new_name = new_name
        super().__init__(step_name=step_name, func=self.func, dataframes=old_name, on_error=on_error)

    def func(self, context):
        """Execute the ``RenameDataFrame`` transformation.

        Renames the specified DataFrame in the context by removing it under the old name
        and re-adding it under the new name.

        Args:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the DataFrame renamed.
        """
        if self.old_name in context.dataframes:
            df = context.dataframes.pop(self.old_name)
            context.set_dataframe(self.new_name, df)
        return context


class CopyDataFrame(Transformation):
    """
    A transformation that creates a copy of an existing DataFrame under a new name in the
    ``Pipeline`` context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``CopyDataFrame``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import CopyDataFrame

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        df = pd.DataFrame(...)

        copy_df = CopyDataFrame(source_dataframe="revenue", target_dataframe="finances") # Initialize the CopyDataFrame Step

        pipeline.add_steps([copy_df])
        pipeline.execute()

    Attributes:
        source_dataframe (str): The name of the existing DataFrame to copy.
        target_dataframe (str): The name under which the copy will be stored in the context.
    """

    def __init__(self, source_dataframe, target_dataframe, step_name="CopyDataFrame", on_error=None):
        """Initialize a new ``CopyDataFrame`` transformation.

        Args:
            source_dataframe (str): The name of the existing DataFrame to copy.
            target_dataframe (str): The name under which the copy will be stored in the context.
            step_name (str, optional): The name of this transformation step.
                Defaults to "CopyDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.source_dataframe = source_dataframe
        self.target_dataframe = target_dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=source_dataframe, on_error=on_error)

    def func(self, context):
        """Execute the ``CopyDataFrame`` transformation.

        Retrieves the source DataFrame from the context, creates a copy of it, stores the copy
        under the target name, and returns the updated context.

        Args:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the new copy of the DataFrame.
        """
        df = context.dataframes[self.source_dataframe].copy()
        context.set_dataframe(self.target_dataframe, df)
        return context