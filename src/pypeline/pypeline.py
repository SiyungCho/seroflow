from collections import OrderedDict

from Log.log_base import *
from Wrappers.wrappers import *
from Utils.utils import *
from Types.type_validation import *
# from Cache.LFUCache import CustomLFUCache
# from Step.step import step as base_step
# from Context.context import context as base_context

class pypeline():
    def __init__(self, mode = "TEST", cache_type = "LFU"):
        # self.logger = custom_logger().logger
        self.mode = mode
        self.__target_extractor = None
        self.__target_loader = None
        
        # init_cache(cache_type)

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
    

    # def init_cache(cache_type):
    #     match cache_type:
    #         case "LFU":
    #             self.__cache = CustomLFUCache
    #         case _:
    #             self.__cache = CustomLFUCache