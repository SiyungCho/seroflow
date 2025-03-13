"""
"""

from abc import abstractmethod
from ..step.step import Step


class Extractor(Step):
    """
    """
    def __init__(self, step_name, func, chunk_size=None):
        """
        """
        super().__init__(step_name=step_name, func=func)
        self.chunk_size = chunk_size

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

    @abstractmethod
    def chunk_func(self, context, chunk_coordinates):
        """
        """

    @abstractmethod
    def get_max_row_count(self):
        """
        """

class MultiExtractor(Step):
    """
    """
    def __init__(self, step_name, type, chunk_size=None):
        """
        """
        super().__init__(step_name=step_name, func=self.func)
        self.extractors = []
        self.chunk_size = chunk_size
        self.type = type

    def add_extractors(self, it, kwargs):
        """
        """
        for item in it:
            self.extractors.append(self.type(source=item, chunk_size=self.chunk_size, **kwargs))

    def func(self):
        """
        """
        pass
