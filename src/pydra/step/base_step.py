"""
Module: abstract_step

This module defines the AbstractStep class for creating steps.
AbstractStep provides a common interface for initializing, 
cleaning up, and executing Pipeline steps. Subclasses must implement 
the abstract methods start_step(), stop_step(), and execute() 
to provide step-specific functionality.
"""

from abc import ABC, abstractmethod

class AbstractStep(ABC):
    """
    AbstractStep

    An abstract class for defining the structure of a step. This class extends the ABC class
    and provides a common interface for starting, stopping, and executing the main 
    functionality of a step. Subclasses must implement the abstract methods start_step(),
    stop_step(), and execute() to provide step-specific functionality.
    """

    @abstractmethod
    def start_step(self):
        """
        Abstract method: start_step()
        This method should contain logic to initialize the step before execution.
        """

    @abstractmethod
    def stop_step(self):
        """
        Abstract method: stop_step()
        This method should contain logic to clean up the step after execution has completed.
        """

    @abstractmethod
    def execute(self):
        """
        Abstract method: execute()
        This method should contain the main functionality of the step.
        """
