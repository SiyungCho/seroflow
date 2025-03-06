from abc import ABC, abstractmethod

class abstract_cache(ABC):

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def store(self):
        pass
    
    @abstractmethod
    def load(self):
        pass