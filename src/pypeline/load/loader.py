"""
"""

from abc import abstractmethod
from ..step.step import Step


class Loader(Step):
    """
    """

    def __init__(self, step_name, dataframes, exists, func):
        """
        """
        super().__init__(step_name=step_name, dataframes=dataframes, func=func)
        self.exists = self._check_exists_parameter(exists)

    def _check_exists_parameter(self, exists):
        """
        """
        if exists not in ['append', 'fail', 'replace']:
            raise ValueError("exists param must be either 'append', 'fail' or 'replace'")
        return exists

    def start_step(self):
        """
        """
        # Check that inputted context is of context type
        return

    def stop_step(self):
        """
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        """

    @abstractmethod
    def map_exists_parameter(self):
        """
        """
