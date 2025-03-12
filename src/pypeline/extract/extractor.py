"""
Module for defining extractor steps.

This module provides the Extractor class, which is a specialized type of step used
for data extraction processes. It inherits from the base step class and adds extractor-specific
functionality.
"""

from abc import abstractmethod
from ..step.step import Step


class Extractor(Step):
    """
    A base class for extractor steps.

    The Extractor class extends the base step functionality to provide a framework
    for defining data extraction operations. Subclasses must implement the abstract
    'func' method to perform the actual extraction logic.
    """

    def __init__(self, step_name, func, chunk_size=None):
        """
        Initialize an Extractor instance.

        Args:
            step_name (str): The name of the extractor step.
            func (callable): The function to execute for the extraction process.
        """
        super().__init__(step_name=step_name, func=func)
        self.chunk_size = chunk_size

    def start_step(self):
        """
        Begin the extractor step.

        This method is intended to be overridden if initialization or pre-processing
        is required before extraction begins. By default, it performs no action.
        """
        return

    def stop_step(self):
        """
        Terminate the extractor step.

        This method clears any parameters stored in the step, effectively resetting
        its state after execution.
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        Execute the extraction logic.

        Subclasses must implement this method to define the extraction process.
        """

    @abstractmethod
    def chunk_func(self, context, chunk_coordinates):
        """
        Execute the extraction logic.

        Subclasses must implement this method to define the extraction process.
        """

    @abstractmethod
    def get_max_row_count(self):
        """
        Gets largest number of rows extracted.

        Returns:
            int: The largest number of rows extracted.
        """
