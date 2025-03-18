"""
Module: transformation.py

This module implements the base Transformation class, which serves as an abstract extension of the Step class.
Transformation provides a common structure for all transformation operations in the ETL pypeline. These operations
typically modify or analyze DataFrames and update the pypeline context accordingly. Subclasses must implement the
abstract method func() to define their specific transformation logic.
"""

from abc import abstractmethod
from ..step.step import Step

class Transformation(Step):
    """
    Transformation Class

    The Transformation class is an abstract base class for defining data transformations within the ETL pypeline.
    It extends the Step class and provides a common framework for executing transformations on DataFrames.
    Subclasses must implement the abstract func() method to provide the actual transformation logic.
    """

    def __init__(self,
                 step_name,
                 func,
                 dataframes=None,
                 on_error=None):
        """
        Initializes the Transformation object.

        Arguments:
            step_name (str): The name of the transformation step.
            func (function): The function that implements the transformation logic.
            dataframes (str or list, optional): The name(s) of the DataFrame(s) in the context that the transformation will operate on.
                                                If a single DataFrame name is provided, it is converted to a list.
            on_error (str, optional): The error handling strategy.
        """
        super().__init__(step_name=step_name,
                         func=func,
                         dataframes=dataframes if isinstance(dataframes, list) else [dataframes],
                         on_error=on_error)

    def start_step(self):
        """
        Prepares the transformation for execution.

        This method is called before the transformation function (func) is executed.
        In this base class, no initialization is required, so it simply returns.
        """
        return

    def stop_step(self):
        """
        Cleans up after the transformation execution.

        Clears the parameters dictionary to reset the transformation state,
        ensuring the step can be executed again if necessary.
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        Abstract method: func()

        Defines the core transformation logic to be applied to the DataFrame(s) in the context.
        Subclasses must override this method to implement specific transformations.

        Arguments:
            context (Context): The pypeline context containing the DataFrame(s) to be transformed.

        Returns:
            Context: The updated context after applying the transformation.
        """
