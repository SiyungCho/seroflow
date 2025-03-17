"""
"""

from abc import abstractmethod
from ..step.step import Step

class Transformation(Step):
    """
    """

    def __init__(self,
                 step_name,
                 func,
                 dataframes=None,
                 on_error=None):
        """
        """
        super().__init__(step_name=step_name,
                         func=func,
                         dataframes=dataframes if isinstance(dataframes, list) else [dataframes],
                         on_error=on_error)

    def start_step(self):
        """
        """
        return

    def stop_step(self):
        """
        """
        self.params.clear()

    @abstractmethod
    def func(self, context):
        """
        """
