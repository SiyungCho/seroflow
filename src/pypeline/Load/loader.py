from abc import abstractmethod
from Step.step import step
from Utils.utils import *
from Wrappers.wrappers import log_err

class loader(step):
    def __init__(self, step_name, description, mode, contexts, exists, func):
        super().__init__(step_name=step_name, description=description, mode=mode, contexts=contexts, func=func)
        self.exists = self._check_exists_parameter(exists)

    def _check_exists_parameter(self, exists):
        if exists not in ['append', 'fail', 'replace']:
            raise Exception("exists param must be either 'append', 'fail' or 'replace'")
        return exists

    def __start_step(self):
        return

    def __stop_step(self):
        self.params.clear()
        return

    @abstractmethod
    def func(self):
        pass

    @abstractmethod
    def map_exists_parameter(self):
        pass