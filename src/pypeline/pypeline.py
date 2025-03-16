"""
"""
import logging
import time
from collections import OrderedDict
import os
from datetime import datetime
from tqdm import tqdm
import pandas as pd

from .log import CustomLogger
from .cache import AbstractCache, LFUCache
from .context import Context as base_context
from .transform import CacheState, ReloadCacheState, ResetCache
from .chunker import Chunker
from .wrappers import log_error
from .utils import generate_key
from .types import is_extractor, is_multiextractor, is_loader, is_step, is_context, is_context_object

class Pypeline():
    """
    """

    def __init__(self, cache=False, logger=False, mode="DEV"):
        """
        """
        self.logger = logger
        self.mode = mode # DEV, TEST, PROD
        self.checked_targets = False
        self.globalcontext = base_context("globalcontext")
        self.cache = cache
        self.__target_extractor = None
        self.__target_loader = None
        self.__chunker = None
        self.__parameter_index = {}
        self.__step_index = OrderedDict()
        self.__step_name_index = OrderedDict()
        self.__dataframe_index = {}

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
    
    def __display_message(self, message, _print=False):
        """
        """
        if self.logger_is_set():
            self.logger.info(message)
        if _print:
            print(message)
    
    @property
    def logger(self):
        """
        """
        return self.__logger

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
    
    @logger.setter
    @log_error("Logger must be a logging object")
    def logger(self, logger):
        """
        """
        if not logger:
            self.__logger = None
        elif isinstance(logger, logging.Logger):
            self.__logger = logger
            self.__display_message("Logger set...")
        elif logger == True:
            self.__logger = CustomLogger("pypeline").logger
            self.__display_message("Logger set...")
        else:
            raise TypeError("Logger must be a logging object")

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
        self.__display_message("Target extractor set...")

    @target_loader.setter
    @log_error("Target extractor must be an extractor or multiextractor")
    def target_loader(self, loader):
        """
        """
        if is_loader(loader, True):
            self.__target_loader = loader
            self.__display_message("Target loader set...")

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

    @cache.setter
    @log_error("Cache must be an instance of AbstractCache")
    def cache(self, cache):
        """
        """
        if not cache:
            self.__cache = None
            self.__display_message("Cache not set...")
        elif isinstance(cache, AbstractCache):
            self.__cache = cache
            self.__display_message("Cache set...")
        elif cache == True:
            self.__cache = LFUCache()
            self.__display_message("Cache set...")
        else:
            raise TypeError("Cache must be an instance of AbstractCache, True, or False")

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
        if self.__cache_is_set():
            self.add_step(self.reset_cache(delete_directory=True))
        if self.chunker is None:
            self.__chunker = chunker(self.step_index)
            self.__chunker.save(parameter_index=self.parameter_index, globalcontext=self.globalcontext)
            self.__display_message("Chunker initialized...")

    def logger_is_set(self):
        """
        """
        if not self.logger:
            return False
        return True

    def __cache_is_set(self):
        """
        """
        if not self.cache:
            return False
        return True
    
    def __chunker_is_set(self):
        """
        """
        if not self.chunker:
            return False
        return True

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
        if self.__cache_is_set() and (not isinstance(self.step_index[step_key], ResetCache)):
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
        self.__display_message("Successfully added step with key: " + str(target_key))

    @log_error("Error adding targets to step index")
    def __add_targets(self):
        """
        """
        if not self.checked_targets:
            self.checked_targets = True
            if (self.mode != "TEST") and (not self.target_extractor):
                raise ValueError("Target extractor must be set before executing pypeline")
            if self.target_extractor:
                if is_multiextractor(self.target_extractor):
                    for extractor in self.target_extractor.extractors:
                        self.__add_target_to_step(extractor, last=False)
                else:
                    self.__add_target_to_step(self.target_extractor, last=False)
            if self.target_loader:
                self.__add_target_to_step(self.target_loader, last=True)
            self.__display_message("Successfully added targets to steps")

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

    # @log_error("Error Parsing Parameters, proper parameter value not found")
    # def __parse_parameters(self, step_key):
    #     """
    #     """
    #     kwargs = {}
    #     step = self.step_index[step_key]

    #     if step.needs_context:
    #         subcontext = self.__create_subcontext(step, step_key)
    #         kwargs["context"] = subcontext

    #     for param in step.params_list:
    #         if param == "chunk_coordinates":
    #             param_value = self.chunker.dequeue()
    #         else:
    #             input_value = step.input_params.get(param)
    #             curr_value = self.parameter_index.get(param)
    #             default_value = step.default_params.get(param)
    #             param_value = input_value or curr_value or default_value
    #         kwargs[param] = param_value
    #     self.__check_parsed_parameters(kwargs)
    #     return kwargs

    @log_error("Error Parsing Parameters, proper parameter value not found")
    def __parse_parameters(self, step_key):
        """
        Parse parameters for a step.
        In TEST mode, if a parameter is a DataFrame, sample it.
        """
        kwargs = {}
        step = self.step_index[step_key]

        if step.needs_context:
            subcontext = self.__create_subcontext(step, step_key)
            if self.mode == "TEST":
                for df_name in subcontext.get_dataframe_names():
                    df = subcontext.get_dataframe(df_name)
                    if isinstance(df, pd.DataFrame):
                        subcontext.set_dataframe(df_name, df.sample(frac=0.1, random_state=42))
            kwargs["context"] = subcontext

        for param in step.params_list:
            if param == "chunk_coordinates":
                param_value = self.chunker.dequeue()
            else:
                input_value = step.input_params.get(param)
                curr_value = self.parameter_index.get(param)
                default_value = step.default_params.get(param)
                param_value = input_value or curr_value or default_value
            if self.mode == "TEST" and isinstance(param_value, pd.DataFrame):
                param_value = param_value.sample(frac=0.1, random_state=42)
            kwargs[param] = param_value
        self.__check_parsed_parameters(kwargs)
        return kwargs


    @log_error("Error Parsing Step Output")
    def __parse_step_output(self, step_output, step_key):
        """
        """
        checked_output = self.__check_step_output(step_output, step_key)
        if checked_output is None:
            return
        for param, value in zip(self.step_index[step_key].return_list, checked_output):
            if is_context(value):
                self.__update_globalcontext(value)
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
            self.__display_message("Resuming execution from checkpoint: " + str(cached_checkpoint), True)
        else:
            self.__display_message("No valid checkpoint found, starting from the beginning...", True)
        return start_index

    def __store_in_cache(self, step_key):
        """
        """
        self.cache.store(self.step_index, self.parameter_index, self.globalcontext, step_key)
        self.__display_message("Checkpoint stored for step: " + str(step_key))

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
            self.__display_message("Successfully added step: " + str(step.step_name) + " with key: " +  str(step_key))

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

    def __perform_step(self, step_key):
        """
        """
        if is_loader(self.step_index[step_key], _raise=False) and self.mode == "DEV":
            return
        step_params = self.__parse_parameters(step_key)
        step_output = self.step_index[step_key](**step_params)
        self.__parse_step_output(step_output, step_key)
        self.__update_cache(step_key)

    @log_error("Error executing pypeline...")
    def execute(self, chunker=None):
        """
        """
        self.__add_targets()
        if chunker is not None:
            self.chunker = chunker

        step_keys = self.__get_step_keys()
        start_index = 0 if not self.__cache_is_set() else self.__load_from_cache(step_keys)

        start_time = time.time()
        self.__display_message("Beginning ETL Execution at time: " + str(start_time) + " ...")

        total_steps = self.__get_number_of_steps() - start_index
        with tqdm(total=total_steps, desc="Executing Pypeline") as pbar:
            for step_key in step_keys[start_index:]:
                self.__display_message("Executing Step: " + str(self.step_name_index[step_key]), True)
                self.__perform_step(step_key)
                self.__display_message("Step: " + self.step_name_index[step_key] + " completed...")
                pbar.update(1)

        if self.chunker is not None:
            if self.chunker.keep_executing:
                self.parameter_index, self.globalcontext = self.chunker.reload()
                self.execute(chunker=chunker)
        else:
            end_time = time.time()
            self.__display_message("ETL Execution Finished at time: " + str(end_time) + " ...")
            elapsed_time = end_time - start_time
            self.__display_message("Total Execution Time: " + str(elapsed_time) + " seconds")
            # self._generate_review()
    
    # def _generate_review(self):
    #     """
    
    #     """
    #     review_details = {}
    #     review_details['mode'] = self.mode
    #     review_details['global_context'] = str(self.globalcontext)
    #     review_details['parameters'] = str(self.parameter_index)
        
    #     message_lines = []
        
    #     if self.mode == "DEV":
    #         message_lines.append("DEV Mode: Global Context Detailed Review:")
    #         message_lines.append("Global Context:")
    #         message_lines.append(str(self.globalcontext))
    #         message_lines.append("\nParameter Index:")
    #         message_lines.append(str(self.parameter_index))
            
    #     elif self.mode == "TEST":
    #         message_lines.append("TEST Mode: Detailed Review for Sampled Data:")
    #         message_lines.append("Global Context (Sampled):")
    #         message_lines.append(str(self.globalcontext))
    #         message_lines.append("\nParameter Index (Sampled):")
    #         message_lines.append(str(self.parameter_index))
    #         # Include step-level metrics if collected.
    #         if hasattr(self, "step_metrics"):
    #             message_lines.append("\nStep Execution Metrics:")
    #             message_lines.append(str(self.step_metrics))
    #             review_details['step_metrics'] = self.step_metrics
                
    #     elif self.mode == "PROD":
    #         message_lines.append("PROD Mode: Detailed Execution Review:")
    #         message_lines.append("Global Context:")
    #         message_lines.append(str(self.globalcontext))
    #         message_lines.append("\nParameter Index:")
    #         message_lines.append(str(self.parameter_index))
    #         if hasattr(self, "step_metrics"):
    #             message_lines.append("\nStep Execution Metrics:")
    #             message_lines.append(str(self.step_metrics))
    #             review_details['step_metrics'] = self.step_metrics
    #         if self.__cache_is_set():
    #             message_lines.append("\nCache Details:")
    #             message_lines.append(str(self.cache))
    #             review_details['cache'] = str(self.cache)
        
    #     # Combine the review message.
    #     message = "\n".join(message_lines)
    #     review_details['message'] = message
        
    #     # Display the detailed review using the pipeline's logger.
    #     self.__display_message(message)
        
    #     # Determine the log folder from the logger's file handler.
    #     log_folder = None
    #     for handler in self.logger.handlers:
    #         if hasattr(handler, 'baseFilename'):
    #             log_folder = os.path.dirname(handler.baseFilename)
    #             break
    #     # Fallback if no file handler is found.
    #     if log_folder is None:
    #         log_folder = os.path.join(os.getcwd(), "logs")
        
    #     # Create a unique review filename with a timestamp.
    #     review_filename = os.path.join(
    #         log_folder, f"pypeline_review_{datetime.now():%Y_%m_%d_%H_%M_%S}.log"
    #     )
        
    #     # Export the review to the determined file.
    #     try:
    #         with open(review_filename, "a") as review_file:
    #             review_file.write("\n" + message + "\n")
    #         self.__display_message(f"Review exported to: {review_filename}")
    #     except Exception as e:
    #         self.__display_message("Warning: Could not export review to file. " + str(e))
        
    #     # Optionally, return the review details if needed elsewhere.
    #     return review_details