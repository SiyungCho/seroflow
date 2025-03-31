"""
This module implements a suite of transformation classes that can perform String Manipulations on DataFrames in the ``Pipeline`` Context.
Each transformation class extends the base ``Transformation`` class and is designed to operate with ``Pipeline`` Object.
The available transformations include:

- **RemoveCharacterFromColumn**: Removes all occurrences of a specified character from a string column.
- **RemoveCharactersFromColumn**: Removes all occurrences of a list of characters from a string column.
- **ReplaceStringInColumn**: Replaces occurrences of a specified substring with another string in a column.
"""

from .transformation import Transformation

class RemoveCharacterFromColumn(Transformation):
    """
    A transformation that removes all occurrences of a specific character from a specified
    string column in a DataFrame. The updated DataFrame is stored back in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``RemoveCharacterFromColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import RemoveCharacterFromColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        remove_char = RemoveCharacterFromColumn(dataframe="states", column="name", char_to_remove="&") # Initialize the RemoveCharacterFromColumn Step

        pipeline.add_steps([remove_char])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column from which to remove the character.
        char_to_remove (str): The character to remove from the column.
    """
    def __init__(self,
                 dataframe,
                 column,
                 char_to_remove,
                 step_name="RemoveCharacterFromColumn",
                 on_error=None):
        """
        Initializes the ``RemoveCharacterFromColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to be updated in the context.
            column (str): The name of the column to process.
            char_to_remove (str): The character to remove from the column's string values.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "RemoveCharacterFromColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.char_to_remove = char_to_remove
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``RemoveCharacterFromColumn`` transformation.

        Retrieves the DataFrame from the context, removes the specified character from
        the target column, updates the DataFrame in the context, and returns the updated context.

        Arguments:
            context (Context): The Pipeline context containing the DataFrame.

        Returns:
            Context: The updated context with the modified DataFrame.
        """
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__remove_char(df)
        context.set_dataframe(self.dataframe, df)
        return context

    def __remove_char(self, df):
        """
        Removes all occurrences of the specified character from the target column.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            Series: The modified column with the character removed.
        """
        return df[self.column].str.replace(self.char_to_remove, "", regex=False)


class RemoveCharactersFromColumn(Transformation):
    """
    A transformation that removes all occurrences of a list of specified characters from
    a target string column in a DataFrame. The updated DataFrame is stored back in the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``RemoveCharactersFromColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import RemoveCharactersFromColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        remove_chars = RemoveCharactersFromColumn(dataframe="states", column="name", char_to_remove=["&", "#", "*"]) # Initialize the RemoveCharactersFromColumn Step

        pipeline.add_steps([remove_chars])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column to process.
        chars_to_remove (iterable): An iterable of characters to remove from the column.
    """
    def __init__(self,
                 dataframe,
                 column,
                 chars_to_remove,
                 step_name="RemoveCharactersFromColumn",
                 on_error=None):
        """
        Initializes the ``RemoveCharactersFromColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update in the context.
            column (str): The name of the column to process.
            chars_to_remove (iterable): A list or iterable of characters to remove from
                                        the column's string values.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "RemoveCharactersFromColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.chars_to_remove = chars_to_remove  # list or iterable of characters
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``RemoveCharactersFromColumn`` transformation.

        Retrieves the DataFrame from the context, removes all specified characters from
        the target column, updates the DataFrame in the context, and returns the updated
        context.

        Arguments:
            context (Context): The Pipeline context containing the DataFrame.

        Returns:
            Context: The updated context with the modified DataFrame.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__remove_chars(df))
        return context

    def __remove_chars(self, df):
        """
        Iteratively removes all specified characters from the target column.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame with the specified characters removed from the target column.
        """
        for char in self.chars_to_remove:
            df[self.column] = df[self.column].str.replace(char, "", regex=False)
        return df


class ReplaceStringInColumn(Transformation):
    """
    A transformation that replaces all occurrences of a specified substring with another
    string in a target column of a DataFrame. The updated DataFrame is stored back in
    the context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``ReplaceStringInColumn``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import ReplaceStringInColumn

        pipeline = Pipeline()
        pipeline.target_extractor = ... # Add Extractor which gathers data

        replace_string = ReplaceStringInColumn(dataframe="states", column="name", to_replace="and", replacement="&") # Initialize the ReplaceStringInColumn Step

        pipeline.add_steps([replace_string])
        pipeline.execute()

    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column to process.
        to_replace (str): The substring to be replaced.
        replacement (str): The string to replace with.
    """
    def __init__(self,
                 dataframe,
                 column,
                 to_replace,
                 replacement,
                 step_name="ReplaceStringInColumn",
                 on_error=None):
        """
        Initializes the ``ReplaceStringInColumn`` transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update in the context.
            column (str): The name of the column in which the replacement is to occur.
            to_replace (str): The substring to be replaced.
            replacement (str): The string to replace the substring with.
            step_name (str, optional): The name of the transformation step.
                                       Defaults to "ReplaceStringInColumn".
            on_error (str, optional): The error handling strategy.
        """
        self.dataframe = dataframe
        self.column = column
        self.to_replace = to_replace
        self.replacement = replacement
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ``ReplaceStringInColumn`` transformation.

        Retrieves the DataFrame from the context, replaces occurrences of the specified
        substring in the target column, updates the DataFrame in the context, and
        returns the updated context.

        Arguments:
            context (Context): The Pipeline context containing the DataFrame.

        Returns:
            Context: The updated context with the modified DataFrame.
        """
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__replace_string(df)
        context.set_dataframe(self.dataframe, df)
        return context

    def __replace_string(self, df):
        """
        Replaces all occurrences of the specified substring in the target column with the
        replacement string.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            Series: The modified column with the substring replaced.
        """
        return df[self.column].str.replace(self.to_replace, self.replacement, regex=False)
