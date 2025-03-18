"""
Module: date.py

This module implements transformation classes for converting columns in a DataFrame to datetime format.
It provides functionality to convert a specified column to a datetime type using pandas' to_datetime method,
allowing for an optional format parameter to guide the conversion.
"""
import pandas as pd
from .transformation import Transformation

# class ExtractDateTime(Transformation):

class ConvertToDateTime(Transformation):
    """
    ConvertToDateTime Class

    A transformation that converts a specified column in a DataFrame to datetime format.
    It leverages pandas.to_datetime to perform the conversion, optionally using a provided format.
    
    Attributes:
        dataframe (str): The name of the DataFrame in the context.
        column (str): The name of the column to convert.
        format (str, optional): The datetime format to use for conversion (if provided).
    """
    def __init__(self,
                 dataframe,
                 column,
                 format=None,
                 step_name="ConvertToDateTime",
                 on_error=None):
        """
        Initializes the ConvertToDateTime transformation.

        Arguments:
            dataframe (str): The name of the DataFrame to update in the context.
            column (str): The column in the DataFrame that will be converted to datetime.
            format (str, optional): The datetime format to be used for conversion. Defaults to None.
            step_name (str, optional): The name of this transformation step. Defaults to "ConvertToDateTime".
            on_error (str, optional): The error handling strategy. Defaults to None.
        """
        self.dataframe = dataframe
        self.column = column
        self.format = format
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the ConvertToDateTime transformation.

        Retrieves the specified DataFrame from the context, converts the designated column to datetime format,
        updates the DataFrame in the context, and returns the updated context.

        Arguments:
            context (Context): The pypeline context containing the DataFrame.

        Returns:
            Context: The updated context with the specified column converted to datetime.
        """
        df = context.dataframes[self.dataframe]
        context.set_dataframe(self.dataframe, self.__convert_to_datetime(df))
        return context

    def __convert_to_datetime(self, df):
        """
        Converts the specified column of the DataFrame to datetime format.

        If a format is provided, it uses that format for conversion; otherwise, it relies on pandas' default parsing.

        Arguments:
            df (DataFrame): The DataFrame to process.

        Returns:
            DataFrame: The DataFrame with the specified column converted to datetime.
        """
        if self.format:
            df[self.column] = pd.to_datetime(df[self.column], format=self.format)
        else:
            df[self.column] = pd.to_datetime(df[self.column])
        return df
