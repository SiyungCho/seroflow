from abc import abstractmethod
from ..Step.step import step
from ..Utils.utils import *
from ..Wrappers.wrappers import log_error

class extractor(step):
    def __init__(self, step_name, func):
        super().__init__(step_name=step_name, func=func)

    def start_step(self):
        return

    def stop_step(self):
        #check that the returned item is of context type
        self.params.clear()
        return

    @abstractmethod
    def func(self):
        pass