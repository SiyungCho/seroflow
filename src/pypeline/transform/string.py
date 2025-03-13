from .transformation import Transformation

class RemoveCharacterFromColumn(Transformation):
    """
    Removes all occurrences of a specific character from a string column.
    """
    def __init__(self, dataframe_name, column, char_to_remove, step_name="RemoveCharacterFromColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.char_to_remove = char_to_remove
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df[self.column] = df[self.column].str.replace(self.char_to_remove, "", regex=False)
        context.set_dataframe(self.dataframe_name, df)
        return context

class RemoveCharactersFromColumn(Transformation):
    """
    Removes a list of characters from a string column.
    """
    def __init__(self, dataframe_name, column, chars_to_remove, step_name="RemoveCharactersFromColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.chars_to_remove = chars_to_remove  # list or iterable of characters
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        for char in self.chars_to_remove:
            df[self.column] = df[self.column].str.replace(char, "", regex=False)
        context.set_dataframe(self.dataframe_name, df)
        return context

# class CountCharacterOccurrences(Transformation):

class ReplaceStringInColumn(Transformation):
    """
    Replaces occurrences of a substring with another string in a column.
    """
    def __init__(self, dataframe_name, column, to_replace, replacement, step_name="ReplaceStringInColumn"):
        self.dataframe_name = dataframe_name
        self.column = column
        self.to_replace = to_replace
        self.replacement = replacement
        super().__init__(step_name=step_name, func=self.func)
        
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        df[self.column] = df[self.column].str.replace(self.to_replace, self.replacement, regex=False)
        context.set_dataframe(self.dataframe_name, df)
        return context