from collections import OrderedDict

from pypeline.Log.logger import *
from Wrappers.wrappers import *
from Utils.utils import *
from Types.type_validation import *
from Cache.LFUCache import LFUCache
from Step.step import step as base_step
from Context.context import context as base_context

class pypeline():
    def __init__(self, mode = "TEST", cache_type = LFUCache):
        self.logger = custom_logger().logger
        self.mode = mode
        self.__target_extractor = None
        self.__target_loader = None

        #check if cache is derived from abstract cache class
        self.__cache = cache_type()
        self.__parameter_index = {}
        self.__step_index = OrderedDict()
        self.__step_name_index = OrderedDict()
        self.__dataframe_index = {}
        self.__cache_index = {}
        self.__globalcontext = base_context("globalcontext")

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
    def step_name_index(self):
        return self.__step_name_index
    
    @property
    def dataframe_index(self):
        return self.__dataframe_index
    
    @property
    def cache_index(self):
        return self.__cache_index
        
    @property
    def globalcontext(self):
        return self.__globalcontext
        
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
    
    def update_step_name_index(self, step_key, step_name):
        self.step_name_index[step_key] = step_name
        return
    
    def update_dataframe_index(self, step_key, dataframe_name):
        if step_key not in self.dataframe_index:
            self.dataframe_index[step_key] = []
        self.dataframe_index[step_key].append(dataframe_name)
        return
    
    def update_cache_index(self, step_key, cache_step_key):
        self.cache_index[step_key].append(cache_step_key)
        return

    def update_globalcontext(self, subcontext):
        for dataframe_name in subcontext.get_dataframe_names():
            if dataframe_name in self.globalcontext.get_dataframe_names():
                self.globalcontext.set_dataframe(dataframe_name, subcontext.get_dataframe(dataframe_name))
            else:
                self.globalcontext.add_dataframe(dataframe_name, subcontext.get_dataframe(dataframe_name))
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

    def add_steps(self, steps):
        if not isinstance(steps, list):
            raise TypeError("try using a list...")
        for step in steps:
            step_key = self.add_step(step)

    def add_step(self, step):
        if is_step(step, _raise=True):
            step_key = self.parse_step(step)
        print("Successfully added step with key: " + str(step_key))

    def targets_found(self, _raise=False):
        if (not self.target_extractor) or (not self.target_loader):
            if raise_:
                raise Exception("Target loader or extractor not found please ensure they are present.")
            return False
        return True

    def add_targets_to_steps(self):
        if self.mode != "TEST": # if the mode is set to test then targets don't have to be set
            self.targets_found(_raise=True)
        target_extractor_key = self.parse_step(self.target_extractor)
        target_loader_key = self.parse_step(self.target_loader)
        self.step_index.move_to_end(target_extractor_key, last=False)
        self.step_index.move_to_end(target_loader_key)

    def parse_step(self, step):
        step_key = generate_key()
        self.update_step_index(step_key, step)
        self.update_step_name_index(step_key, step.step_name)
        if step.dataframes is not None:
            for dataframe_name in step.dataframes:
                self.update_dataframe_index(step_key, dataframe_name)
        return step_key

    def parse_parameters(self, step_key):
        kwargs = {}
        for param in self.step_index[step_key].params_list:
            if param != 'context':
                input_value = self.step_index[step_key].input_params[param] if param in self.step_index[step_key].input_params else None
                curr_value = self.parameter_index[param]
                default_value = self.step_index[step_key].default_params[param] if param in self.step_index[step_key].default_params else None
                param_value = input_value or curr_value or default_value
            else:
                desired_dataframes = self.dataframe_index[step_key]
                step_name = self.step_name_index[step_key]
                subcontext = base_context(step_name)
                if not is_extractor(extractor, False):
                    for dataframe_name in desired_dataframes:
                        subcontext.add_dataframe(self.globalcontext.get_dataframe(dataframe_name))
                param_value = subcontext      
            if param_value is None:
                raise Exception("Error parameter value not found in any index")
            kwargs[param] = param_value
        return kwargs

    def parse_step_output(self, step_output, step_key):
        for param, value in zip(self._steps[step_key].return_list, step_output):
            if is_context(value):
                self.update_globalcontext(value)  # Update context index if value is a context
            elif is_context_object(value):
                for _, item in value.items():
                    self.update_globalcontext(item)
            else:
                self.update_parameter_index(param, value)
        return
    
    def validate_step_output(self, step_output, step_key):
        if not isinstance(step_output, tuple):
            step_output = [step_output]

        if (self.step_index[step_key].return_list == []) and (step_output[0] is None):
            return None
        elif len(self.step_index[step_key].return_list) != len(step_output):
            raise Exception("Error incorrect amount of return elements found")
        return step_output

    def execute(self, on_fail="skip"):
        self.logger.info("Beginning ETL Execution...")
        self.add_targets_to_steps()

        # search for init cache file
        # if one is present then we are in dev and want to figure out which cache file to start from (ie can be newest file or check functions for changes and go from most recent that has not been changed)
        # if one is not present then we start from the beginning

        for step_key in self.step_index.keys():
            # print(f"{self.step_index[step_key]}: {step_key}")

            step_params = self.parse_parameters(step_key)
            step_output = self.validate_step_output(self.step_index[step_key](**step_params), step_key)
            if not step_output:
                self.parse_step_output(step_output, step_key)

            self.logger.info(f"step: {step_key} completed...")
            #step was successful
            #start new thread
            #inside thread we cache the current state of all indexes and outputs
            #upload to corresponding cache file
        self.logger.info("ETL Execution Finished...")
