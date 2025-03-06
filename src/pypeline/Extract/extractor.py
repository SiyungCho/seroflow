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

    def __init__(self, step_name, func):
        """
        Initialize an Extractor instance.

        Args:
            step_name (str): The name of the extractor step.
            func (callable): The function to execute for the extraction process.
        """
        super().__init__(step_name=step_name, func=func)

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
        return

    @abstractmethod
    def func(self):
        """
        Execute the extraction logic.

        Subclasses must implement this method to define the extraction process.
        """
        pass
