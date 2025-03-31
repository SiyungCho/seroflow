"""
This module implements transformation classes for manipulating the index of a DataFrame.
Each transformation class extends the base ``Transformation`` class and operates on a specified DataFrame stored in the ``Pipeline`` context.
The available transformations include:

- **SetIndex**: Sets a specified column as the DataFrame’s index.
- **ResetIndex**: Resets the DataFrame’s index, with an option to drop the existing index.
"""

from .transformation import Transformation

class SetIndex(Transformation):
    """
    A transformation that sets a specified column as the index of a DataFrame.
    The transformation updates the DataFrame in the ``Pipeline`` context by using the
    ``pandas`` ``set_index`` method.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``SetIndex``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import SetIndex

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Extractor extracts 'sample_data' with 'id' column

        # Initialize and execute SetIndex
        set_index = SetIndex(dataframe="sample_data", index_column="id")
        pipeline.add_steps([set_index])
        pipeline.execute()

    
    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        index_column (str): The column to be set as the new index.
    """
    def __init__(self,
                 dataframe,
                 index_column,
                 step_name="SetIndex",
                 on_error=None):
        """
        Initializes the ``SetIndex`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update in the context.
            index_column (str): The name of the column to set as the index.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "SetIndex".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.index_column = index_column
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``SetIndex`` transformation.

        Retrieves the DataFrame from the context, sets the specified column as the index,
        updates the DataFrame in the context, and returns the updated context.

        Arguments:
            context (Context): The Pipeline context containing the DataFrame.

        Returns:
            Context: The updated context with the new index set.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__set_index(df))
        return context

    def __set_index(self, df):
        """
        Sets the specified column as the index of the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to modify.
        """
        # Note: Using inplace=True modifies the DataFrame in place and returns None.
        return df.set_index(self.index_column, inplace=True)


class ResetIndex(Transformation):
    """
    A transformation that resets the index of a DataFrame.
    The transformation updates the DataFrame in the ``Pipeline`` context by resetting its index,
    optionally dropping the existing index.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``ResetIndex``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import ResetIndex

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Extractor extracts 'sample_data'

        # Initialize and execute ResetIndex (dropping the index)
        reset_index = ResetIndex(dataframe="sample_data", drop=True)
        pipeline.add_steps([reset_index])
        pipeline.execute()
    
    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        drop (bool): Whether to drop the existing index. Defaults to False.
    """
    def __init__(self,
                 dataframe,
                 drop=False,
                 step_name="ResetIndex",
                 on_error=None):
        """
        Initializes the ``ResetIndex`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update in the context.
            drop (bool, optional): Whether to drop the current index. Defaults to False.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "ResetIndex".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.drop = drop
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``ResetIndex`` transformation.

        Retrieves the DataFrame from the context, resets its index according to the
        specified parameters, updates the DataFrame in the context, and returns the
        updated context.

        Arguments:
            context (Context): The Pipeline context containing the DataFrame.

        Returns:
            Context: The updated context with the index reset.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__reset_index(df))
        return context

    def __reset_index(self, df):
        """
        Resets the index of the DataFrame.

        Arguments:
            df (DataFrame): The DataFrame to modify.
        """
        return df.reset_index(drop=self.drop, inplace=True)
