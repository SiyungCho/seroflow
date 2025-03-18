"""
Module: internal.py

This module implements transformation classes for managing DataFrames within the pypeline context.
It provides functionality for adding, deleting, renaming, and copying DataFrames in the context.
These operations help maintain and modify the state of DataFrames as the pypeline executes, ensuring that
the context reflects the desired DataFrame structure for subsequent processing steps.

Classes:
    AddDataFrame: Adds a new DataFrame to the context.
    DeleteDataFrame: Deletes a DataFrame from the context.
    RenameDataFrame: Renames an existing DataFrame in the context.
    CopyDataFrame: Creates a copy of an existing DataFrame under a new name.
"""

from .transformation import Transformation

class AddDataFrame(Transformation):
    """
    AddDataFrame

    A transformation that adds a new DataFrame to the pypeline context.
    The DataFrame is stored in the context under the specified name.
    """
    def __init__(self,
                 dataframe,
                 name,
                 step_name="AddDataFrame",
                 on_error=None):
        """
        Initializes the AddDataFrame transformation.

        Arguments:
            dataframe (DataFrame): The DataFrame to be added.
            name (str): The name under which the DataFrame will be stored in the context.
            step_name (str, optional): The name of the transformation step. Defaults to "AddDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.name = name
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the AddDataFrame transformation.

        Adds the specified DataFrame to the context under the provided name.

        Arguments:
            context (Context): The context object where the DataFrame will be added.

        Returns:
            Context: The updated context with the new DataFrame.
        """
        context.add_dataframe(self.name, self.dataframe)
        return context

class DeleteDataFrame(Transformation):
    """
    DeleteDataFrame

    A transformation that deletes a DataFrame from the pypeline context.
    """
    def __init__(self,
                 dataframe,
                 step_name="DeleteDataFrame",
                 on_error=None):
        """
        Initializes the DeleteDataFrame transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to be deleted from the context.
            step_name (str, optional): The name of the transformation step. Defaults to "DeleteDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the DeleteDataFrame transformation.

        Deletes the specified DataFrame from the context.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            Context: The updated context with the DataFrame removed.
        """
        del context.dataframes[self.dataframe]
        return context

class RenameDataFrame(Transformation):
    """
    RenameDataFrame

    A transformation that renames a DataFrame within the pypeline context.
    """
    def __init__(self,
                 old_name,
                 new_name,
                 step_name="RenameDataFrame",
                 on_error=None):
        """
        Initializes the RenameDataFrame transformation.

        Arguments:
            old_name (str): The current name of the DataFrame in the context.
            new_name (str): The new name to assign to the DataFrame.
            step_name (str, optional): The name of the transformation step. Defaults to "RenameDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.old_name = old_name
        self.new_name = new_name
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=old_name,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the RenameDataFrame transformation.

        Renames the specified DataFrame in the context by removing it under the old name and re-adding it under the new name.

        Arguments:
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
    CopyDataFrame

    A transformation that creates a copy of an existing DataFrame under a new name in the pypeline context.
    """
    def __init__(self,
                 source_dataframe,
                 target_dataframe,
                 step_name="CopyDataFrame",
                 on_error=None):
        """
        Initializes the CopyDataFrame transformation.

        Arguments:
            source_dataframe (str): The name of the existing DataFrame to copy.
            target_dataframe (str): The name under which the copy will be stored in the context.
            step_name (str, optional): The name of this transformation step. Defaults to "CopyDataFrame".
            on_error (str, optional): The error handling strategy.
        """
        self.source_dataframe = source_dataframe
        self.target_dataframe = target_dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=source_dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the CopyDataFrame transformation.

        Retrieves the source DataFrame from the context, creates a copy of it, stores the copy under the target name,
        and returns the updated context.

        Arguments:
            context (Context): The context containing the DataFrame.

        Returns:
            Context: The updated context with the new copy of the DataFrame.
        """
        df = context.dataframes[self.source_dataframe].copy()
        context.set_dataframe(self.target_dataframe, df)
        return context
