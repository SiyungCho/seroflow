from .transformation import Transformation

class RemoveCharacterFromColumn(Transformation):
    """
    Removes all occurrences of a specific character from a string column.
    """
    def __init__(self, dataframe, column, char_to_remove, step_name="RemoveCharacterFromColumn"):
        self.dataframe = dataframe
        self.column = column
        self.char_to_remove = char_to_remove
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__remove_char(df)
        context.set_dataframe(self.dataframe, df)
        return context
    
    def __remove_char(self, df):
        return df[self.column].str.replace(self.char_to_remove, "", regex=False)

class RemoveCharactersFromColumn(Transformation):
    """
    Removes a list of characters from a string column.
    """
    def __init__(self, dataframe, column, chars_to_remove, step_name="RemoveCharactersFromColumn"):
        self.dataframe = dataframe
        self.column = column
        self.chars_to_remove = chars_to_remove  # list or iterable of characters
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__remove_chars(df))
        return context
    
    def __remove_chars(self, df):
        for char in self.chars_to_remove:
            df[self.column] = df[self.column].str.replace(char, "", regex=False)
        return df

# class CountCharacterOccurrences(Transformation):

class ReplaceStringInColumn(Transformation):
    """
    Replaces occurrences of a substring with another string in a column.
    """
    def __init__(self, dataframe, column, to_replace, replacement, step_name="ReplaceStringInColumn"):
        self.dataframe = dataframe
        self.column = column
        self.to_replace = to_replace
        self.replacement = replacement
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        
    def func(self, context):
        df = context.dataframes[self.dataframe]
        df[self.column] = self.__replace_string(df)
        context.set_dataframe(self.dataframe, df)
        return context
    
    def __replace_string(self, df):
        return df[self.column].str.replace(self.to_replace, self.replacement, regex=False)