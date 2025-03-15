"""
"""

import time
from collections import OrderedDict
from tqdm import tqdm

from .log import CustomLogger
from .wrappers import log_error
from .utils import generate_key
from .types import is_extractor, is_multiextractor, is_loader, is_step, is_context, is_context_object
from .cache import AbstractCache, LFUCache
from .context import Context as base_context
from .transform import CacheState
from .transform import ReloadCacheState
from .transform import ResetCache
from .chunker import Chunker

class Pypeline():
    """
    """

    def __init__(self, use_cache=False, cache=None, logger=None, mode="DEV"):
        """
        """
        self.logger = CustomLogger("pypeline").logger if logger is None else logger
        self.mode = mode # DEV, TEST, PROD
        self.checked_targets = False
        self.target_extractor_set = False
        self.globalcontext = base_context("globalcontext")
        self.use_cache = use_cache
        self.cache = (use_cache, cache)
        self.__target_extractor = None
        self.__target_loader = None
        self.__chunker = None
        self.__parameter_index = {}
        self.__step_index = OrderedDict()
        self.__step_name_index = OrderedDict()
        self.__dataframe_index = {}
        self.__chunker = None

    def __del__(self):
        """
        """

    def __str__(self):
        """
        """
        print("----Pypeline Object----")
        print("Parameters Index:")
        print(self.parameter_index)
        print("Step Index:")
        print(self.step_index)
        print("Step Name Index:")
        print(self.step_name_index)
        print("Dataframe Index:")
        print(self.dataframe_index)
        return "-----------------------"

    @property
    def target_extractor(self):
        """
        """
        return self.__target_extractor

    @property
    def target_loader(self):
        """
        """
        return self.__target_loader

    @property
    def cache(self):
        """
        """
        return self.__cache

    @property
    def parameter_index(self):
        """
        """
        return self.__parameter_index

    @property
    def step_index(self):
        """
        """
        return self.__step_index

    @property
    def step_name_index(self):
        """
        """
        return self.__step_name_index

    @property
    def dataframe_index(self):
        """
        """
        return self.__dataframe_index

    @property
    def globalcontext(self):
        """
        """
        return self.__globalcontext
    
    @property
    def chunker(self):
        """
        """
        return self.__chunker
    
    @property
    def mode(self):
        """
        """
        return self.__mode
    
    @property
    def chunker(self):
        """
        """
        return self.__chunker

    @target_extractor.setter
    @log_error("Target extractor must be an extractor or multiextractor")
    def target_extractor(self, extractor):
        """
        """
        if is_extractor(extractor, _raise=False):
            self.__target_extractor = extractor
        elif is_multiextractor(extractor, _raise=False):
            self.__target_extractor = extractor
        else:
            raise TypeError("Target extractor must be an extractor or multiextractor")
        self.target_extractor_set = True
        self.logger.info("Target extractor set...")

    @target_loader.setter
    @log_error("Target extractor must be an extractor or multiextractor")
    def target_loader(self, loader):
        """
        """
        if is_loader(loader, True):
            self.__target_loader = loader
            self.logger.info("Target loader set...")

    @parameter_index.setter
    @log_error("Parameter index must be a dictionary")
    def parameter_index(self, parameter_index):
        """
        """
        if not isinstance(parameter_index, dict):
            raise TypeError("Parameter index must be a dictionary")
        self.__parameter_index = parameter_index

    @globalcontext.setter
    @log_error("Global context must be a context object")
    def globalcontext(self, globalcontext):
        """
        """
        if not is_context(globalcontext):
            raise TypeError("Global context must be a context object")
        self.__globalcontext = globalcontext

    @chunker.setter
    @log_error("Chunker must be of chunker class type")
    def chunker(self, chunker):
        """
        """
        if not isinstance(chunker, AbstractCache):
            raise TypeError("Chunker must be of chunker class type")
        self.__chunker = chunker

    @cache.setter
    @log_error("Cache must be an instance of AbstractCache")
    def cache(self, cache_tuple):
        """
        """
        use_cache, cache = cache_tuple
        if use_cache:
            if (cache is not None) and (not isinstance(cache, AbstractCache)):
                raise TypeError("Cache must be an instance of AbstractCache")
            self.__cache = LFUCache() if cache is None else cache
        else:
            self.__cache = None

    @mode.setter
    @log_error("Mode must be either DEV, TEST, or PROD")
    def mode(self, mode):
        """
        """
        if not isinstance(mode, str):
            raise TypeError("Mode must be a string")
        if mode not in ["DEV", "TEST", "PROD"]:
            raise ValueError("Mode must be either DEV, TEST, or PROD")
        self.__mode = mode

    @chunker.setter
    @log_error("Chunker must be of Chunker class type")
    def chunker(self, chunker):
        """
        """
        if not isinstance(chunker, Chunker):
            raise TypeError("Chunker must be of Chunker class type")
        if self.use_cache:
            self.add_step(self.reset_cache(delete_directory=True))
        if self.chunker is None:
            self.__chunker = chunker(self.step_index)
            self.__chunker.save(parameter_index=self.parameter_index, globalcontext=self.globalcontext)
            self.logger.info("Chunker initialized...")

    def __update_parameter_index(self, parameter, value):
        """
        """
        self.parameter_index[parameter] = value

    def __add_new_parameter(self, parameter):
        """
        """
        if parameter not in self.parameter_index:
            self.parameter_index[parameter] = None

    def __update_step_index(self, step_key, step):
        """
        """
        self.step_index[step_key] = step

    def __update_step_name_index(self, step_key, step_name):
        """
        """
        self.step_name_index[step_key] = step_name

    def __update_dataframe_index(self, step_key, dataframe_name):
        """
        """
        if step_key not in self.dataframe_index:
            self.dataframe_index[step_key] = []
        self.dataframe_index[step_key].append(dataframe_name)

    def __update_globalcontext(self, subcontext):
        """
        """
        for dataframe_name in subcontext.get_dataframe_names():
            if dataframe_name in self.globalcontext.get_dataframe_names():
                self.globalcontext.set_dataframe(
                    dataframe_name, subcontext.get_dataframe(dataframe_name)
                )
            else:
                self.globalcontext.add_dataframe(
                    dataframe_name, subcontext.get_dataframe(dataframe_name)
                )

    def __update_cache(self, step_key):
        """
        """
        if self.use_cache and (not isinstance(self.step_index[step_key], ResetCache)):
            self.__store_in_cache(step_key)

    def __check_parsed_parameters(self, kwargs):
        """
        """
        for key, value in kwargs.items():
            if value is None:
                raise ValueError("Key: %s has no value, check parameter index", key)
            
    def __check_step_output(self, step_output, step_key):
        """
        """
        if not isinstance(step_output, tuple):
            step_output = [step_output]
        
        if (self.step_index[step_key].return_list == []) and (step_output[0] is None):
            return None
        if len(self.step_index[step_key].return_list) != len(step_output):
            raise ValueError("Error incorrect amount of return elements found")
        return step_output

    def __create_subcontext(self, step, step_key):
        step_name = self.step_name_index[step_key]
        subcontext = base_context(step_name + "_subcontext")
        if not is_extractor(step, _raise=False):
            desired_dataframes = self.dataframe_index.get(step_key, [])
            if not desired_dataframes:
                subcontext = self.globalcontext
            else:
                for dataframe_name in desired_dataframes:
                    subcontext.add_dataframe(
                        dataframe_name,
                        self.globalcontext.get_dataframe(dataframe_name)
                    )
        return subcontext

    def __get_current_step_number(self):
        """
        """
        return self.__get_number_of_steps() + 1 if self.step_index else 0

    def __get_number_of_steps(self):
        """
        """
        return len(self.__get_step_keys())
    
    def __get_step_keys(self):
        """
        """
        return list(self.step_index.keys())
    
    @log_error("Error adding target to step index")
    def __add_target_to_step(self, target, last=False):
        target_key = self.__parse_step(target)
        self.step_index.move_to_end(target_key, last=last)
        self.step_name_index.move_to_end(target_key, last=last)
        self.logger.info("Successfully added step with key: %s", target_key)

    @log_error("Error adding targets to step index")
    def __add_targets(self):
        """
        """
        if not self.checked_targets:
            self.checked_targets = True
            if (self.mode != "TEST") and (not self.target_extractor_set):
                raise ValueError("Target extractor must be set before executing pypeline")
            if self.target_extractor:
                if is_multiextractor(self.target_extractor):
                    for extractor in self.target_extractor.extractors:
                        self.__add_target_to_step(extractor, last=False)
                else:
                    self.__add_target_to_step(self.target_extractor, last=False)
            if self.target_loader:
                self.__add_target_to_step(self.target_loader, last=True)
            self.logger.info("Successfully added targets to steps")

    @log_error("Error Parsing Step")
    def __parse_step(self, step):
        """
        """
        key_index = self.__get_current_step_number()
        step_key = generate_key(step.step_name + "_" + str(key_index))
        self.__update_step_index(step_key, step)
        self.__update_step_name_index(step_key, step.step_name)
        for param in step.params_list:
            self.__add_new_parameter(param)
        for dataframe in step.dataframes:
            self.__update_dataframe_index(step_key, dataframe)
        return step_key

    @log_error("Error Parsing Parameters, proper parameter value not found")
    def __parse_parameters(self, step_key):
        """
        """
        kwargs = {}
        step = self.step_index[step_key]

        if step.needs_context:
            subcontext = self.__create_subcontext(step, step_key)
            kwargs["context"] = subcontext

        for param in step.params_list:
            if param == "chunk_coordinates":
                param_value = self.chunker.dequeue()
            else:
                input_value = step.input_params.get(param)
                curr_value = self.parameter_index.get(param)
                default_value = step.default_params.get(param)
                param_value = input_value or curr_value or default_value
            kwargs[param] = param_value
        self.__check_parsed_parameters(kwargs)
        return kwargs

    @log_error("Error Parsing Step Output")
    def __parse_step_output(self, step_output, step_key):
        """
        """
        checked_output = self.__check_step_output(step_output, step_key)
        for param, value in zip(self.step_index[step_key].return_list, checked_output):
            if is_context(value):
                self.__update_globalcontext(value)  # Update context index if value is a context.
            elif is_context_object(value):
                for _, item in value.items():
                    self.__update_globalcontext(item)
            else:
                self.__update_parameter_index(param, value)

    def __load_from_cache(self, step_keys):
        """
        """
        start_index = 0
        cached_checkpoint = self.cache.get_cached_checkpoint(self.step_index)
        if cached_checkpoint and (cached_checkpoint in step_keys):
            self.parameter_index, self.globalcontext = self.cache.load(cached_checkpoint)
            start_index = step_keys.index(cached_checkpoint) + 1
            self.logger.info("Resuming execution from checkpoint: %s", cached_checkpoint)
            print("Resuming execution from: " + str(cached_checkpoint))
        else:
            self.logger.info("No valid checkpoint found, starting from the beginning...")
            print("No checkpoint found...")
        return start_index

    def __store_in_cache(self, step_key):
        """
        """
        self.cache.store(self.step_index, self.parameter_index, self.globalcontext, step_key)
        self.logger.info("Checkpoint stored for step: %s", step_key)

    @log_error("add_steps method requires a list of step objects")
    def add_steps(self, steps):
        """
        """
        if not isinstance(steps, list):
            raise TypeError("try using a list...")
        for step in steps:
            self.add_step(step)

    @log_error("add_step method requires a step object")
    def add_step(self, step):
        """
        """
        if is_multiextractor(step):
            for extractor in step.extractors:
                self.add_step(extractor)
        if is_step(step, _raise=True):
            step_key = self.__parse_step(step)
            self.logger.info("Successfully added step: %s with key: %s", step.step_name, step_key)

    def cache_state(self, step_name="cache_state"):
        """
        """
        return CacheState(
            step_name=step_name,
            cache=self.cache,
            parameter_index=self.parameter_index,
            globalcontext=self.globalcontext,
        )

    def reload_cached_state(self, cache_key, step_name="reload_cached_state"):
        """
        """
        return ReloadCacheState(
            step_name=step_name,
            cache_key=cache_key,
            cache=self.cache,
            pypeline=self
        )

    def reset_cache(self, step_name="reset_cache", delete_directory=False):
        """
        """
        return ResetCache(
            step_name=step_name,
            cache=self.cache,
            delete_directory=delete_directory
        )
    
    def execute(self, chunker=None):
        """
        """
        self.__add_targets()
        if chunker is not None:
            self.chunker = chunker

        step_keys = self.__get_step_keys()
        start_index = 0 if not self.use_cache else self.__load_from_cache(step_keys)

        start_time = time.time()  # Start timer
        self.logger.info("Beginning ETL Execution at time: %s ...", start_time)

        total_steps = self.__get_number_of_steps() - start_index
        with tqdm(total=total_steps, desc="Executing Pypeline") as pbar:
            for step_key in step_keys[start_index:]:
                tqdm.write("Executing Step: " + str(self.step_name_index[step_key]))
                self.logger.info("Executing Step: %s", self.step_name_index[step_key])

                step_params = self.__parse_parameters(step_key)
                step_output = (self.step_index[step_key](**step_params))
                self.__parse_step_output(step_output, step_key)
                self.__update_cache(step_key)
                
                self.logger.info("Step: %s completed...", self.step_name_index[step_key])
                pbar.update(1)

        if self.chunker is not None:
            if self.chunker.keep_executing:
                self.parameter_index, self.globalcontext = self.chunker.reload()
                self.execute(chunker=chunker)
        else:
            end_time = time.time()  # End timer
            self.logger.info("ETL Execution Finished at time: %s ...", end_time)
            elapsed_time = end_time - start_time
            self.logger.info("Total Execution Time: %.2f seconds", elapsed_time)