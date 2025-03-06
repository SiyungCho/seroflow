from abc import ABC, abstractmethod

class abstract_cache(ABC):

    @abstractmethod #don't 100% know if this is needed cause parameter index kinda does the same thing
    def put(self):
        pass

    @abstractmethod #don't 100% know if this is needed cause parameter index kinda does the same thing
    def get(self): #maybe this should be more like reload the state of pypeline when called
        pass
    
    @abstractmethod
    def store(self):
        pass
    
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def reset(self):
        pass