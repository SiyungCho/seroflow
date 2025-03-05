from collections import OrderedDict

from .Log import *
from .Wrappers import *
from .Utils import *
from .Types import *
from .Cache import LFUCache as LFUCache
from .Step import step as base_step
from .Context import context as base_context

class pypeline():
    def __init__(self, cache_type=LFUCache, mode = "TEST"):
        self.logger = custom_logger("pypeline").logger
        self.mode = mode
        self.__target_extractor = None
        self.__target_loader = None

        #check if cache is derived from abstract cache class
        self.__cache = cache_type()
        self.__parameter_index = {}
        self.__step_index = OrderedDict()
        self.__step_name_index = OrderedDict()
        self.__dataframe_index = {}
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
    
    def update_globalcontext(self, subcontext):
        for dataframe_name in subcontext.get_dataframe_names():
            if dataframe_name in self.globalcontext.get_dataframe_names():
                self.globalcontext.set_dataframe(dataframe_name, subcontext.get_dataframe(dataframe_name))
            else:
                self.globalcontext.add_dataframe(dataframe_name, subcontext.get_dataframe(dataframe_name))
                self.logger.info(f"Added dataframe: {dataframe_name} to globalcontext")
        return
    
    def add_steps(self, steps):
        if not isinstance(steps, list):
            raise TypeError("try using a list...")
        for step in steps:
            self.add_step(step)

    def add_step(self, step):
        if is_step(step, True):
            step_key = self.parse_step(step)
        print("Successfully added step with key: " + str(step_key))

    def targets_found(self, _raise=False):
        if (not self.target_extractor) or (not self.target_loader):
            if _raise:
                raise Exception("Target loader or extractor not found please ensure they are present.")
            return False
        return True

    def add_targets_to_steps(self):
        if self.mode != "TEST": # if the mode is set to test then targets don't have to be set
            self.targets_found(_raise=True)

        if self.target_extractor:
            target_extractor_key = self.parse_step(self.target_extractor)
            self.step_index.move_to_end(target_extractor_key, last=False)
            self.step_name_index.move_to_end(target_extractor_key, last=False)
        if self.target_loader:
            target_loader_key = self.parse_step(self.target_loader)
            self.step_index.move_to_end(target_loader_key)
            self.step_name_index.move_to_end(target_loader_key)
        return

    def parse_step(self, step):
        step_key = generate_key()
        self.update_step_index(step_key, step)
        self.update_step_name_index(step_key, step.step_name)
        if step.params_list:
            for param in step.params_list:
                if param != 'context' and param not in self.parameter_index:
                    self.update_parameter_index(param, None)
        if step.dataframes:
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
                param_value = None
                step_name = self.step_name_index[step_key]
                subcontext = base_context(step_name+"_subcontext")

                if is_extractor(self.step_index[step_key], False):
                    param_value = subcontext  

                if param_value is None:
                    desired_dataframes = self.dataframe_index[step_key] if step_key in self.dataframe_index else []

                    if desired_dataframes == []:
                        subcontext = self.globalcontext
                    else:
                        for dataframe_name in desired_dataframes:
                            subcontext.add_dataframe(dataframe_name, self.globalcontext.get_dataframe(dataframe_name))
                    param_value = subcontext
            if param_value is None:
                raise Exception("Error parameter value not found in any index")
            kwargs[param] = param_value
        return kwargs

    def parse_step_output(self, step_output, step_key):
        for param, value in zip(self.step_index[step_key].return_list, step_output):
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

        #check cache:
        # search for init cache file
        # if one is present then we are in dev and want to figure out which cache file to start from (ie can be newest file or check functions for changes and go from most recent that has not been changed)
        # if one is not present then we start from the beginning

        for step_key in self.step_index.keys():
            print(f"Executing Step: {self.step_name_index[step_key]}")
            self.logger.info(f"Executing Step: {self.step_name_index[step_key]}")

            step_params = self.parse_parameters(step_key)
            step_output = self.validate_step_output(self.step_index[step_key](**step_params), step_key)
            if step_output:
                self.parse_step_output(step_output, step_key)

            self.logger.info(f"Step: {self.step_name_index[step_key]} completed...")

            #update cache:
            #step was successful
            #start new thread
            #inside thread we cache the current state of all indexes and outputs
            #upload to corresponding cache file
        self.logger.info("ETL Execution Finished...")

    def __str__(self):
        print(self.parameter_index)
        print(self.step_index)
        print(self.step_name_index)
        print(self.dataframe_index)
        print(self.cache_index)
        return "pypeline object"
