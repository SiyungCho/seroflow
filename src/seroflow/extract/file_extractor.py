"""
Module: file_extractor

This module defines abstract classes for file extraction.
It provides two main classes:
    - FileExtractor: An abstract base class that extends Extractor for reading a single file.
      It validates the source file, extracts the file name (without extension),
      and defines an interface for reading the file either entirely or in chunks.
    - MultiFileExtractor: A concrete extractor that extends MultiExtractor to handle files.
      It gathers files from a specified source directory based on a given extension type and
      creates multiple extractor instances to process each file individually.
"""

from abc import abstractmethod
from ..utils.utils import check_directory, check_file, gather_files, remove_extension
from .extractor import Extractor, MultiExtractor

class FileExtractor(Extractor):
    """
    FileExtractor

    An abstract extractor for reading data from a single file.
    This class extends the Extractor class and validates the source file, extracts the file 
    name, and defines abstract methods for reading the file fully, reading the file in chunks,
    and obtaining the maximum row count.
    """
    def __init__(self,
                 source,
                 func,
                 chunk_size,
                 on_error,
                 step_name="FileExtractor",
                 **kwargs):
        """
        FileExtractor Class Constructor
        Initializes the FileExtractor object.

        Arguments:
            source (str):
                The source directory where the file is located
            func (function):
                The function to be executed by the extractor
            chunk_size (int):
                The number of rows to read at a time
            on_error (str):
                The error handling strategy
            step_name (str):
                The name of the step
            **kwargs:
                Additional keyword arguments for the read_csv() method

        Raises:
            FileNotFoundError: If the source directory is not found
        """
        super().__init__(step_name=step_name,
                         func=func,
                         chunk_size=chunk_size,
                         on_error=on_error)
        if not check_file(source):
            raise FileNotFoundError("Error directory not found")

        self.source = source
        self.file_path = source
        self.file_name = remove_extension(source.split('/')[-1])
        self.kwargs = kwargs

    @abstractmethod
    def func(self, context):
        """
        Abstract method: func()
        Reads the file and adds the DataFrame to the context

        Arguments:
            context (Context):
                Blank context object where the DataFrame will be added

        Returns:
            Context:
                The context object with the DataFrame added
        """

    @abstractmethod
    def get_max_row_count(self):
        """
        Abstract method: get_max_row_count()
        Returns the number of rows in the file

        Returns:
            int:
                The number of rows in the file
        """

class MultiFileExtractor(MultiExtractor):
    """
    MultiFileExtractor

    A concrete extractor for reading data from multiple files within a directory.
    This class extends the MultiExtractor and gathers file paths and file names from
    the source directory based on a specified file extension type.
    It then creates and adds individual extractor instances for each file.
    """
    def __init__(self,
                 source,
                 type,
                 extension_type,
                 chunk_size,
                 on_error,
                 step_name="MultiFileExtractor",
                 **kwargs):
        """
        MultiFileExtractor Class Constructor
        Initializes the MultiFileExtractor object.

        Arguments:
            source (str):
                The source directory where the file is located
            type (str):
                The type of the extractor
            extension_type (str):
                The type of the file extension
            chunk_size (int):
                The number of rows to read at a time
            on_error (str):
                The error handling strategy
            step_name (str):
                The name of the step
            **kwargs:
                Additional keyword arguments for the read_csv() method

        Raises:
            FileNotFoundError: If the source directory is not found
        """
        super().__init__(step_name=step_name,
                         type=type,
                         chunk_size=chunk_size,
                         on_error=on_error)
        if not check_directory(source):
            raise FileNotFoundError("Error directory not found")

        self.source = source
        extension = self.identify_type(extension_type)
        self.file_paths, self.file_names = gather_files(self.source, extension)
        self.add_extractors(self.file_paths, kwargs)

    def identify_type(self, extension_type):
        """
        Public method: identify_type()
        Identifies the file extension type

        Arguments:
            extension_type (str):
                The type of the file extension

        Returns:
            list:
                The list of file extensions

        Raises:
            ValueError: If the file type is invalid
        """
        if extension_type == 'csv':
            return ["csv"]
        if extension_type == 'excel':
            return ["xlsx", "xls"]
        raise ValueError("Invalid file type")
