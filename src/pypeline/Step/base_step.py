"""
Module that defines the AbstractStep interface.

This module provides the AbstractStep abstract base class, which outlines the essential
methods for any step in a processing pipeline. Subclasses must implement the methods to
start, stop, and execute the step.
"""

from abc import ABC, abstractmethod


class AbstractStep(ABC):
    """
    Abstract base class for a processing step.

    This class defines the required interface for processing steps. Any subclass must implement
    the `start_step`, `stop_step`, and `execute` methods to manage the lifecycle and operation
    of a step.
    """

    @abstractmethod
    def start_step(self):
        """
        Start or initialize the step.

        This method should contain logic to prepare or initialize the step before execution.
        """

    @abstractmethod
    def stop_step(self):
        """
        Stop or finalize the step.

        This method should contain logic to clean up or finalize the step after execution.
        """

    @abstractmethod
    def execute(self):
        """
        Execute the main functionality of the step.

        This method should contain the core logic of the step's processing operation.
        """
