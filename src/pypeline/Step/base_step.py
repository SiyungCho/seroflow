from abc import ABC, abstractmethod

class abstract_step(ABC):
    @abstractmethod
    def start_step(self):
        pass

    @abstractmethod
    def stop_step(self):
        pass

    @abstractmethod
    def execute(self):
        pass