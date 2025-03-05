from abc import ABC, abstractmethod

class abstract_step(ABC):
    @abstractmethod
    def __start_step(self):
        pass

    @abstractmethod
    def __stop_step(self):
        pass

    @abstractmethod
    def execute(self):
        pass