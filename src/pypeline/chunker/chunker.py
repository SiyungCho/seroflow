"""
Module: chunker

This module defines the base functionality for partitioning (chunking). 
It provides an abstract Chunker class that is responsible for calculating chunk coordinates,
managing a queue of chunking coordinates, and saving/restoring the chunker's state. 
The Chunker class is designed to work with pypeline steps that support chunking,
ensuring that data is processed in manageable segments.
"""
from abc import abstractmethod
from collections import OrderedDict
from queue import Queue
from copy import deepcopy
from ..types import is_extractor, is_loader

class Chunker:
    """
    Chunker

    The Chunker class is responsible for dividing a large dataset into smaller chunks for processing.
    It examines the Pypeline's step index for steps that have a defined 'chunk_size' and, if applicable,
    calculates the coordinates for each chunk. It also manages a coordinate queue for chunk processing
    and provides methods for saving and reloading the state of the chunker.

    In addition, the class validates that any loader steps used in chunking are configured to append data.
    """
    def __init__(self, step_index):
        """
        Chunker Class Constructor method

        Iterates through the provided step index to identify steps that support chunking. For each step
        that has a 'chunk_size' attribute and is an extractor, it initializes the chunk coordinates as a tuple
        containing:
            - The chunk size.
            - A starting index (initially 0).
            - The maximum row count as provided by step.get_max_row_count().
            - A flag (initially False) indicating completion status.

        Also validates that any loader step (identified via is_loader) has its 'exists' attribute set to 'append',
        as required when using chunking.
        Finally, it initializes a queue for managing chunk coordinates, a state dictionary for saving the chunker state,
        and invokes the calculate_chunks() method to populate the coordinate queue.

        Arguments:
            step_index (OrderedDict): 
                An ordered dictionary mapping step keys to step objects in the pipeline.
        """
        self.chunk_index = OrderedDict()
        for step_key, step in step_index.items():
            if hasattr(step, 'chunk_size') and is_extractor(step, _raise=False):
                if not(step.chunk_size is None):
                    self.chunk_index[step_key] = (step.chunk_size, 0, step.get_max_row_count(), False)
	
            if is_loader(step, _raise=False) and hasattr(step, 'exists'):
                if step.exists != 'append':
                    raise ValueError("All loaders must be set to 'append' when using chunking")
        self.keep_executing = True
        self.coordinate_queue = Queue()
        self.saved_state = {}
        self.calculate_chunks()

    def check_keep_executing(self):
        """
        Public method: check_keep_executing()
        Checks if the coordinate queue is empty

        Returns:
            bool: 
                True: if the queue is not empty
                False: otherwise
        """
        if self.coordinate_queue.qsize() == 0:
            return False
        return True

    def enqueue(self, value):
        """
        Public method: enqueue()
        Adds a value to the coordinate queue.
        Chunking coordinates are tuples containing start and stop index values.

        Arguments:
            value (tuple): 
                A tuple containing start and stop index values corresponding to a chunk
        """
        self.coordinate_queue.put(value)

    def dequeue(self):
        """
        Public method: dequeue()
        Removes a value from the coordinate queue.

        Returns:
            tuple: 
                A tuple containing start and stop index values corresponding to a chunk
        """
        value = self.coordinate_queue.get()
        self.keep_executing = self.check_keep_executing()
        return value

    def reload(self):
        """
        Public method: reload()
        Reloads the chunker state

        Returns:
            tuple: 
                A tuple containing the parameter index and global context
        """
        return self.saved_state['parameter_index'], self.saved_state['globalcontext']

    def save(self, **kwargs):
        """
        Public method: save()
        Saves the chunker state

        Arguments:
            **kwargs: 
                Keyword arguments to save, passed as key-value pairs
                In this case, the parameter index and global context
        """
        for key, value in kwargs.items():
            self.saved_state[key] = deepcopy(value)

    @abstractmethod
    def calculate_chunks(self):
        """
        Abstract method: calculate_chunks()
        Calculates coordinate values for the chunker.
        Each chunk is defined by a start and stop index value.
        """
