from abc import abstractmethod
from ..Step.step import step
from ..Utils.utils import *
from ..Wrappers.wrappers import log_error

class extractor(step):
    def __init__(self, step_name, description, mode, contexts, func):
        super().__init__(description=description, mode=mode, contexts=contexts, func=func)

    def __start_step(self):
        return

    def __stop_step(self):
        return

    @abstractmethod
    def func(self):
        pass