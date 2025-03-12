"""
Module for defining a Loader step in the data processing pipeline.

This module provides the Loader class, an abstract base class that extends the step class.
The Loader is responsible for loading data (dataframes) and managing behavior related to
existing data, such as appending, failing, or replacing data.
"""

from abc import abstractmethod
from ..step.step import Step


class Loader(Step):
    """
    Abstract base class for loader steps in a data processing pipeline.

    The Loader class is designed to load data from dataframes and handle cases where data
    already exists. It manages the 'exists' parameter and requires subclasses to implement
    the loading logic and mapping of the 'exists' parameter.
    """

    def __init__(self, step_name, dataframes, exists, func):
        """
        Initialize a Loader instance.

        Args:
            step_name (str): The name of the loader step.
            dataframes (list or dict): The dataframes to be processed or loaded.
            exists (str): Behavior if data already exists. 
            Must be one of 'append', 'fail', or 'replace'.
            func (callable): The function to execute for the loading process.
        """
        super().__init__(step_name=step_name, dataframes=dataframes, func=func)
        self.exists = self._check_exists_parameter(exists)

    def _check_exists_parameter(self, exists):
        """
        Validate the 'exists' parameter.

        Ensures the 'exists' parameter is one of the allowed values: 'append', 'fail', or 'replace'.
        If not, an Exception is raised.

        Args:
            exists (str): The parameter to validate.

        Returns:
            str: The validated exists parameter.

        Raises:
            Exception: If the 'exists' parameter is not one of the allowed values.
        """
        if exists not in ['append', 'fail', 'replace']:
            raise ValueError("exists param must be either 'append', 'fail' or 'replace'")
        return exists

    def start_step(self):
        """
        Begin the loader step.

        This method is intended to perform any necessary initialization before the loading process.
        For example, it could check that the input context is of the correct type.
        """
        # Check that inputted context is of context type
        return

    def stop_step(self):
        """
        Terminate the loader step.

        Clears any stored parameters, effectively resetting the step's state.
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        Execute the loading process.

        Subclasses must implement this method to define the logic for loading data.
        """

    @abstractmethod
    def map_exists_parameter(self):
        """
        Map the 'exists' parameter to the appropriate behavior.

        Subclasses must implement this method to translate the 'exists' parameter into the
        corresponding operation (e.g., append, fail, or replace).

        Returns:
            The mapped behavior for handling existing data.
        """

class MultiLoader(Step):
    def __init__(self, step_name, type, exists='append'):
        super().__init__(step_name=step_name, func=self.func)
        self.loaders = []
        self.type = type
        self.exists = exists

    def add_loaders(self, it, **kwargs):
        for item in it:
            self.loaders.append(self.type(source=item, exists=self.exists, **kwargs))

    def func(self):
        pass
