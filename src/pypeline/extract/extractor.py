"""
Module: extractor

This module defines abstract classes for data extraction steps.
It includes two primary classes:
    - Extractor: An abstract base class for reading data from a single source and adding the resulting DataFrame
                 to the pypeline context. It defines the interface for full reads, chunked reads, and obtaining the
                 maximum number of rows from the source.
    - MultiExtractor: A concrete extractor that aggregates multiple extractor instances to handle multiple sources.
                      It facilitates the creation and management of multiple extractors using a specified extractor type.
"""

from abc import abstractmethod
from ..step.step import Step

class Extractor(Step):
    """
    Extractor

    An abstract base class for reading data from a single source. Subclasses of Extractor must implement
    the abstract methods:
        - func(): to read the source entirely and add the resulting DataFrame to the context.
        - chunk_func(): to read a chunk of the source and add the resulting DataFrame to the context.
        - get_max_row_count(): to return the total number of rows in the source.
    
    This class also manages an optional chunk_size attribute that, if provided, enables chunked reading.
    """
    def __init__(self, step_name, func, on_error, chunk_size=None):
        """
        Extractor Class Constructor
        Initializes the Extractor object.

        Arguments:
            step_name (str): 
                The name of the step
            func (function): 
                The function to be executed by the extractor
            on_error (str): 
                The error handling strategy
            chunk_size (int): 
                The number of rows to read at a time
        """
        super().__init__(step_name=step_name, func=func, on_error=on_error)
        self.chunk_size = chunk_size

    def start_step(self):
        """
        Public method: start_step()
        """
        return

    def stop_step(self):
        """
        Public method: stop_step()
        Clears the parameters dictionary
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        Abstract method: func()
        Reads the source and adds the DataFrame to the context

        Arguments:
            context (Context): 
                Blank context object where the DataFrame will be added

        Returns:
            Context: 
                The context object with the DataFrame added
        """

    @abstractmethod
    def chunk_func(self, context, chunk_coordinates):
        """
        Abstract method: chunk_func()
        Reads the source in chunks and adds the DataFrame to the context

        Arguments:
            context (Context): 
                Blank context object where the DataFrame will be added
            chunk_coordinates (tuple): 
                The start and stop indices of the chunk to read

        Returns:
            Context: 
                The context object with the DataFrame added
        """

    @abstractmethod
    def get_max_row_count(self):
        """
        Abstract method: get_max_row_count()
        Returns the number of rows in the source

        Returns:
            int: 
                The number of rows in the source
        """

class MultiExtractor(Step):
    """
    MultiExtractor

    A concrete extractor that aggregates multiple extractor instances to handle multiple sources.
    It enables the creation of multiple extractors of a specified type to process each source individually.
    """
    def __init__(self, step_name, type, on_error, chunk_size=None):
        """
        MultiExtractor Class Constructor
        Initializes the MultiExtractor object.

        Arguments:
            step_name (str): 
                The name of the step
            type (type): 
                The type of extractor to use
            on_error (str): 
                The error handling strategy
            chunk_size (int): 
                The number of rows to read at a time
        """
        super().__init__(step_name=step_name, func=self.func, on_error=on_error)
        self.extractors = []
        self.chunk_size = chunk_size
        self.type = type

    def add_extractors(self, it, kwargs):
        """
        Public method: add_extractors()
        Initializes single extractors for each item in the iterable

        Arguments:
            it (iterable): 
                The iterable containing the extractors to add
            kwargs (dict): 
                Additional keyword arguments for the extractors
        """
        for item in it:
            self.extractors.append(self.type(source=item, chunk_size=self.chunk_size, **kwargs))

    def func(self):
        """
        Public method: func()
        Should be blank
        """
