from abc import ABC, abstractmethod

class abstract_cache(ABC):

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def store(self, file_path):
        pass
    
    @classmethod
    def load(cls, file_path):
        pass