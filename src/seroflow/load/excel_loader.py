"""
Module: excel_loader

This module provides concrete implementations for writing DataFrames to Excel files.
It defines two loader classes:
    - ExcelLoader: A loader that writes a single DataFrame to an Excel file.
    - MultiExcelLoader: A loader that handles writing multiple DataFrames to Excel files.
These classes extend the FileLoader class and implement Excel-specific functionality,
including determining the target file path, handling file modes based on the 'exists'
parameter, and managing Excel writing engines.
"""
import os
import pandas as pd
from .file_loader import FileLoader

class ExcelLoader(FileLoader):
    """
    ExcelLoader

    A concrete loader for writing a DataFrame to an Excel file.
    This class extends FileLoader and provides methods to convert DataFrames into Excel format,
    determine the target file path, and handle file modes to the specified existence parameter.
    """

    def __init__(self,
                 target,
                 dataframe,
                 file_extension=".xlsx",
                 exists="append",
                 step_name="ExcelLoader",
                 on_error=None,
                 **kwargs):
        """
        ExcelLoader Class Constructor
        Initializes the ExcelLoader object.

        Arguments:
            target (str): 
                The target directory where the Excel file will be written
            dataframe (DataFrame): 
                The DataFrame to be written to the Excel file
            file_extension (str): 
                The file extension to use when writing the Excel file
            exists (str): 
                The file mode to use when writing the Excel file
            step_name (str): 
                The name of the step
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the to_excel() method
        """
        super().__init__(target=target,
                         dataframe=dataframe,
                         exists=exists,
                         func=self.func,
                         step_name=step_name,
                         file_extension=file_extension,
                         on_error=on_error,
                         **kwargs)

    def func(self, context):
        """
        Public method: func()
        Reads the DataFrame from the context and writes it to an Excel file

        Arguments:
            context (Context): 
                The context object containing the dataframes to be written to the Excel
        """
        for key, df in context.dataframes.items():
            if self.target_file_path is None:
                file_path = key+self.file_extension
                target_file_path = os.path.join(self.target, file_path)
            else:
                target_file_path = self.target_file_path
            self.__to_excel(df, target_file_path, self.kwargs)

    def __to_excel(self, df, target_file_path, kwargs):
        """
        Private method: __to_excel()
        Writes the DataFrame to an Excel file

        Arguments:
            df (DataFrame): 
                The DataFrame to be written to the Excel file
            target_file_path (str): 
                The target file path where the Excel file will be written
            kwargs (dict): 
                Additional keyword arguments for the to_excel() method
        """
        directory = os.path.dirname(target_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        engine = 'openpyxl'
        if self.file_extension == '.xls':
            engine = 'xlrd'

        if os.path.exists(target_file_path):
            with pd.ExcelWriter(target_file_path,
                                engine=engine,
                                mode='a',
                                if_sheet_exists=self.map_exists_parameter()
                                ) as f:
                df.to_excel(f, **kwargs)
        else:
            with pd.ExcelWriter(target_file_path,
                                engine=engine,
                                mode='w'
                                ) as f:
                df.to_excel(f, **kwargs)

    def map_exists_parameter(self):
        """
        Public method: map_exists_parameter()
        Maps the exists parameter to the if_sheet_exists parameter for the ExcelWriter object

        Returns:
            str (['error', 'replace', 'append'], None): 
                The appropriate if_sheet_exists parameter for the ExcelWriter object
        """
        if self.exists == "append":
            return 'overlay'
        if self.exists == "fail":
            return 'error'
        if self.exists == "replace":
            return 'replace'
        return None

class MultiExcelLoader(ExcelLoader):
    """
    MultiExcelLoader

    A concrete loader for writing multiple DataFrames to multiple Excel files.
    This class extends ExcelLoader and provides methods to write multiple DataFrames
    to Excel files in the specified target directory.
    """
    def __init__(self,
                 target,
                 dataframes=None,
                 file_extension=".xlsx",
                 exists="append",
                 step_name="MultiExcelLoader",
                 on_error=None,
                 **kwargs):
        """
        MultiExcelLoader Class Constructor
        Initializes the MultiExcelLoader object.

        Arguments:
            target (str): 
                The target directory where the Excel files will be written
            dataframes (dict): 
                A dictionary mapping keys to DataFrames to be written to the Excel files
            file_extension (str): 
                The file extension to use when writing the Excel files
            exists (str): 
                The file mode to use when writing the Excel files
            step_name (str): 
                The name of the step
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the to_excel() method
        """
        super().__init__(target=target,
                         dataframe=dataframes,
                         file_extension=file_extension,
                         exists=exists,
                         step_name=step_name,
                         on_error=on_error,
                         **kwargs)
