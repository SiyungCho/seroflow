from collections import OrderedDict

from pypeline.Log.logger import *
from Wrappers.wrappers import *
from Utils.utils import *
from Types.type_validation import *
from Cache.LFUCache import LFUCache
# from Step.step import step as base_step
# from Context.context import context as base_context

class pypeline():
    def __init__(self, mode = "TEST", cache_type = "LFU"):
        self.logger = custom_logger().logger
        self.mode = mode
        self.__target_extractor = None
        self.__target_loader = None
        
        self.__cache = None
        self.init_cache(cache_type)

        self.__parameter_index = {}
        self.__step_index = OrderedDict()
        self.__step_key_index = OrderedDict()
        self.__dataframe_index = {}
        self.__cache_index = {}

    @property
    def target_extractor(self):
        return self.__target_extractor
    
    @property
    def target_loader(self):
        return self.__target_loader
    
    @property
    def cache(self):
        return self.__cache
    
    @property
    def parameter_index(self):
        return self.__parameter_index

    @property
    def step_index(self):
        return self.__step_index
    
    @property
    def step_key_index(self):
        return self.__step_key_index
    
    @property
    def dataframe_index(self):
        return self.__dataframe_index
    
    @property
    def cache_index(self):
        return self.__cache_index
    
    @target_extractor.setter
    def target_extractor(self, extractor):
        if is_extractor(extractor, True):
            self.__target_extractor = extractor
            self.logger.info("Target extractor set...")
        return
    
    @target_loader.setter
    def target_loader(self, loader):
        if is_loader(loader, True):
            self.__target_loader = loader
            self.logger.info("Target loader set...")
        return

    @cache.setter
    def cache(self, cache):
        self.__cache = cache
        return
    
    def update_parameter_index(self, parameter, value):
        self.parameter_index[parameter] = value
        return
    
    def update_step_index(self, step_key, step):
        self.step_index[step_key] = step
        return
    
    def update_step_key_index(self, step_name, step_key):
        self.step_key_index[step_name] = step_key
        return
    
    def update_dataframe_index(self, step_key, dataframe_name):
        self.dataframe_index[step_key] = dataframe_name
        return
    
    def update_cache_index(self, step_key, cache_step_key):
        self.cache_index[step_key].append(cache_step_key)
        return

    def put_cache(self, key, value):
        self.cache.put(key, value)
        return

    def get_cache(self, key):
        self.cache.get(key)
        return

    def store_cache(self, file_path):
        self.cache.store(file_path)
        return

    def load_cache(self, file_path):
        self.cache.load(file_path)
        return
    
    def init_cache(self, cache_type):
        match cache_type:
            case "LFU":
                self.cache = LFUCache()
            case "Manual":
                self.cache = None
            case _:
                self.cache = LFUCache()