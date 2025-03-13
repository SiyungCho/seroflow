"""
This module provides the transformation class, an abstract subclass of step,
which defines the interface and common behaviors for transformation steps
within an ETL pipeline framework.

The transformation class inherits from the step class and provides default
implementations for starting and stopping the step. It also defines an abstract
method 'func' that must be implemented by all concrete transformation steps.
"""

from abc import abstractmethod
from ..step.step import Step

class Transformation(Step):
    """
    Abstract class representing a transformation step in an ETL pipeline.

    This class inherits from the step class and defines common behavior for
    transformation steps. It provides default implementations for starting
    and stopping the step, and declares an abstract method 'func' that must be
    implemented by subclasses.

    Attributes:
        (Attributes are inherited from the base 'step' class.)
    """

    def __init__(self, step_name, func, dataframes=None):
        """
        Initialize a new transformation instance.

        Args:
            step_name (str): The name of the transformation step.
            func (callable): The function implementing the transformation logic.
        """
        super().__init__(step_name=step_name, func=func, dataframes=dataframes)

    def start_step(self):
        """
        Start the transformation step.

        This method can be overridden by subclasses to perform any initialization
        or setup actions required before the transformation is executed.

        Returns:
            None
        """
        return

    def stop_step(self):
        """
        Stop the transformation step.

        Clears the parameters associated with the transformation step to reset its state.

        Returns:
            None
        """
        self.params.clear()

    @abstractmethod
    def func(self):
        """
        Abstract method that defines the transformation logic.

        Concrete subclasses must implement this method to perform the actual
        transformation.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
