"""
Module: seroflow

This module implements a data pipeline framework using the Pipeline class.
It provides functionality for managing and executing a sequence of data processing
steps with support for caching, logging, parameter management, and execution chunking.

The module integrates with several sub-components such as custom logging, caching,
context management, transformation utilities, chunking, and type validation to offer
a robust and extensible architecture.

Classes:
    Pipeline: Core class to construct, manage, and execute an ETL Pipeline.
              It enables the addition of steps, manages dependencies via a global context
              and parameter index, and supports various execution modes.
"""

import logging
import time
from collections import OrderedDict
from tqdm.auto import tqdm

from .log.logger import CustomLogger
from .cache.cache import AbstractCache
from .cache.lfu_cache import LFUCache
from .context.context import Context as base_context
from .transform.cache import CacheState, ReloadCacheState, ResetCache
from .chunker.chunker import Chunker
from .wrappers.wrappers import log_error
from .utils.utils import generate_key
from .types.type_validation import is_step, is_extractor, is_multiextractor
from .types.type_validation import is_loader, is_context, is_context_object


class Pipeline:
    """Pipeline Class.

    Provides a framework for constructing and executing data pipelines with built-in
    support for state caching, logging, and chunked execution. Allows dynamic addition
    of processing steps while managing inter-step dependencies through a global context
    and parameter index. The Pipeline can operate in different modes ("DEV" or "PROD"),
    which alter its execution behavior (e.g., DEV mode skips loader steps).

    Attributes:
        logger (logging.Logger or None): Logger instance used for tracking execution details.
        mode (str): Current execution mode ("DEV" or "PROD").
        cache (AbstractCache or None): Caching mechanism for storing intermediate Pipeline states.
        parameter_index (dict): Dictionary for storing parameters and variables shared across steps.
        step_index (OrderedDict): Mapping of unique step keys to their corresponding step objects.
        step_name_index (OrderedDict): Mapping of unique step keys to the step names.
        dataframe_index (dict): Mapping of step keys to lists of requested dataframe names.
        globalcontext (Context): Global context object holding all dataframes used in the pipeline.
        chunker (Chunker or None): Optional chunker object for partitioning and managing segmented execution.
    """

    def __init__(self, cache=False, logger=False, mode="DEV"):
        """Initializes a Pipeline instance.

        Args:
            cache (AbstractCache subclass or bool, optional): If False, no cache is used.
                If True, the default cache (LFUCache) is instantiated. Alternatively, a user-defined
                cache object (derived from AbstractCache) can be provided. Defaults to False.
            logger (logging.Logger or bool, optional): If False, no logger is used.
                If True, the default logger (CustomLogger) is instantiated. Alternatively, a user-defined
                logger can be provided. Defaults to False.
            mode (str, optional): Execution mode. Must be either "DEV" or "PROD".
                "DEV" mode skips loader steps, while "PROD" mode executes all steps.
                Defaults to "DEV".
        """
        self.logger = logger
        self.mode = mode  # "DEV" or "PROD"
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
        """Destructor.

        Deletes internal components when the Pipeline object is deleted.
        """
        del self.__logger
        del self.__target_extractor
        del self.__target_loader
        del self.__chunker
        del self.__parameter_index
        del self.__step_index
        del self.__step_name_index
        del self.__dataframe_index
        del self.__globalcontext
        del self.__cache

    def __str__(self):
        """Returns a string representation of the Pipeline.

        Prints the internal parameter index, step index, step name index, and dataframe index.

        Returns:
            str: A summary string of the pipeline's internal state.
        """
        print("----Seroflow Pipeline----")
        print(f"Parameters Index: {self.parameter_index}")
        print(f"Step Index: {self.step_index}")
        print(f"Step Name Index: {self.step_name_index}")
        print(f"Dataframe Index: {self.dataframe_index}")
        return "-----------------------"

    def __display_message(self, message, _print=False):
        """Displays or logs a message.

        If a logger is set, logs the message. Optionally prints the message if _print is True.

        Args:
            message (str): The message to be logged/printed.
            _print (bool): If True, prints the message. Defaults to False.
        """
        if self.logger_is_set():
            self.logger.info(message)
        if _print:
            print(message)

    @property
    def logger(self):
        """Gets the logger.

        Returns:
            logging.Logger or None: The current logger.
        """
        return self.__logger

    @logger.setter
    @log_error("Logger must be a logging object")
    def logger(self, logger):
        """Sets the logger.

        Args:
            logger (logging.Logger or bool): If True, initializes default CustomLogger.
                If False, no logger is used. If a logging.Logger instance is provided,
                it is used as is.

        Raises:
            TypeError: If logger is not a logging.Logger instance or a valid bool.
        """
        if not logger:
            self.__logger = None
        elif isinstance(logger, logging.Logger):
            self.__logger = logger
            self.__display_message("Logger set...")
        elif logger is True:
            self.__logger = CustomLogger("Pipeline").logger
            self.__display_message("Logger set...")
        else:
            raise TypeError("Logger must be a logging object")

    @property
    def target_extractor(self):
        """Gets the target extractor.

        Returns:
            object: The target extractor.
        """
        return self.__target_extractor

    @target_extractor.setter
    @log_error("Verify Extractor Type")
    def target_extractor(self, extractor):
        """Sets the target extractor.

        Args:
            extractor (Extractor or MultiExtractor): The extractor to set.

        Raises:
            TypeError: If the extractor is not a valid extractor or multiextractor.
        """
        if is_extractor(extractor, _raise=False):
            self.__target_extractor = extractor
        elif is_multiextractor(extractor, _raise=False):
            self.__target_extractor = extractor
        else:
            raise TypeError("Extractor must be extractor or multiextractor")
        self.__display_message("Target extractor set...")

    @property
    def target_loader(self):
        """Gets the target loader.

        Returns:
            object: The target loader.
        """
        return self.__target_loader

    @target_loader.setter
    @log_error("Verify Loader Type")
    def target_loader(self, loader):
        """Sets the target loader.

        Args:
            loader (Loader): The loader to set.

        Raises:
            TypeError: If the loader is not a valid loader.
        """
        if is_loader(loader, _raise=True):
            self.__target_loader = loader
            self.__display_message("Target loader set...")

    @property
    def cache(self):
        """Gets the cache object.

        Returns:
            AbstractCache or None: The cache used by the pipeline.
        """
        return self.__cache

    @cache.setter
    @log_error("Cache must be an instance of AbstractCache")
    def cache(self, cache):
        """Sets the cache object.

        Args:
            cache (AbstractCache subclass or bool): If True, initializes default LFUCache.
                If False, no cache is used. Alternatively, a user-defined cache instance
                (derived from AbstractCache) can be provided.

        Raises:
            TypeError: If cache is not a bool or a valid AbstractCache subclass.
        """
        if not cache:
            self.__cache = None
            self.__display_message("Cache not set...")
        elif isinstance(cache, AbstractCache):
            self.__cache = cache
            self.__display_message("Cache set...")
        elif cache is True:
            self.__cache = LFUCache()
            self.__display_message("Cache set...")
        else:
            raise TypeError("Cache must be type AbstractCache or Bool")

    @property
    def parameter_index(self):
        """Gets the parameter index.

        Returns:
            dict: The parameter index mapping parameter names to values.
        """
        return self.__parameter_index

    @parameter_index.setter
    @log_error("Parameter index must be a dictionary")
    def parameter_index(self, parameter_index):
        """Sets the parameter index.

        Args:
            parameter_index (dict): Dictionary to initialize the parameter index.

        Raises:
            TypeError: If parameter_index is not a dictionary.
        """
        if not isinstance(parameter_index, dict):
            raise TypeError("Parameter index must be a dictionary")
        self.__parameter_index = parameter_index

    @property
    def step_index(self):
        """Gets the step index.

        Returns:
            OrderedDict: Mapping of step keys to step objects.
        """
        return self.__step_index

    @property
    def step_name_index(self):
        """Gets the step name index.

        Returns:
            OrderedDict: Mapping of step keys to step names.
        """
        return self.__step_name_index

    @property
    def dataframe_index(self):
        """Gets the dataframe index.

        Returns:
            dict: Mapping of step keys to lists of dataframe names.
        """
        return self.__dataframe_index

    @property
    def globalcontext(self):
        """Gets the global context.

        Returns:
            Context: The global context object containing all dataframes.
        """
        return self.__globalcontext

    @globalcontext.setter
    @log_error("Global context must be a context object")
    def globalcontext(self, globalcontext):
        """Sets the global context.

        Args:
            globalcontext (Context): The context object to set as global.

        Raises:
            TypeError: If globalcontext is not a valid Context.
        """
        if not is_context(globalcontext):
            raise TypeError("Global context must be a Context object")
        self.__globalcontext = globalcontext

    @property
    def chunker(self):
        """Gets the chunker.

        Returns:
            Chunker or None: The chunker object used for partitioning execution.
        """
        return self.__chunker

    @chunker.setter
    @log_error("Chunker must be of Chunker class type")
    def chunker(self, chunker):
        """Sets the chunker.

        Verifies that the provided chunker is a subclass of Chunker, resets the cache if needed,
        and initializes the chunker with the current step index, parameter index, and global context.

        Args:
            chunker (type): A subclass of Chunker.

        Raises:
            TypeError: If chunker is not a subclass of Chunker.
        """
        if not (isinstance(chunker, type) and issubclass(chunker, Chunker)):
            raise TypeError("Chunker must be a subclass of Chunker")
        if self.__cache_is_set():
            self.add_step(self.reset_cache(delete_directory=True))
        if self.chunker is None:
            self.__chunker = chunker(self.step_index)
            self.__chunker.save(parameter_index=self.parameter_index,
                                globalcontext=self.globalcontext)
            self.__display_message("Chunker initialized...")

    @property
    def mode(self):
        """Gets the execution mode.

        Returns:
            str: The current execution mode ("DEV" or "PROD").
        """
        return self.__mode

    @mode.setter
    @log_error("Mode must be either DEV, or PROD")
    def mode(self, mode):
        """Sets the execution mode.

        Args:
            mode (str): The mode to set ("DEV" or "PROD").

        Raises:
            TypeError: If mode is not a string.
            ValueError: If mode is not "DEV" or "PROD".
        """
        if not isinstance(mode, str):
            raise TypeError("Mode must be a string")
        if mode not in ["DEV", "PROD"]:
            raise ValueError("Mode must be either DEV, or PROD")
        self.__mode = mode

    def logger_is_set(self):
        """Checks if a logger is set.

        Returns:
            bool: True if a logger is initialized, False otherwise.
        """
        return bool(self.logger)

    def __cache_is_set(self):
        """Checks if a cache is set.

        Returns:
            bool: True if a cache is initialized, False otherwise.
        """
        return bool(self.cache)

    def __chunker_is_set(self):
        """Checks if a chunker is set.

        Returns:
            bool: True if a chunker is initialized, False otherwise.
        """
        return bool(self.chunker)

    def __update_parameter_index(self, parameter, value):
        """Updates the parameter index.

        Args:
            parameter (str): The parameter name.
            value (Any): The value to update.
        """
        self.parameter_index[parameter] = value

    def __add_new_parameter(self, parameter):
        """Adds a new parameter to the index if it does not exist.

        Args:
            parameter (str): The parameter name.
        """
        if parameter not in self.parameter_index:
            self.parameter_index[parameter] = None

    def __update_step_index(self, step_key, step):
        """Updates the step index.

        Args:
            step_key (str): The unique key for the step.
            step (object): The step object.
        """
        self.step_index[step_key] = step

    def __update_step_name_index(self, step_key, step_name):
        """Updates the step name index.

        Args:
            step_key (str): The unique key for the step.
            step_name (str): The name of the step.
        """
        self.step_name_index[step_key] = step_name

    def __update_dataframe_index(self, step_key, dataframe_name):
        """Updates the dataframe index.

        Args:
            step_key (str): The unique key for the step.
            dataframe_name (str): The name of the dataframe.
        """
        if step_key not in self.dataframe_index:
            self.dataframe_index[step_key] = []
        self.dataframe_index[step_key].append(dataframe_name)

    def __update_globalcontext(self, subcontext):
        """Updates the global context with data from a subcontext.

        Args:
            subcontext (Context): The subcontext containing dataframes to update.
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
        """Updates the cache with the current state if a cache is set.

        Args:
            step_key (str): The key of the completed step.
        """
        if self.__cache_is_set() and (not isinstance(self.step_index[step_key], ResetCache)):
            self.__store_in_cache(step_key)

    def __check_parsed_parameters(self, kwargs):
        """Validates that parsed parameters have non-empty values.

        Args:
            kwargs (dict): Dictionary of parameters to check.

        Raises:
            ValueError: If any parameter value is None.
        """
        for key, value in kwargs.items():
            if value is None:
                raise ValueError(f"Key: {key} has no value, check parameter index")

    def __check_step_output(self, step_output, step_key):
        """Validates the output of a step.

        Converts the output to a list if necessary and verifies the number of returned elements.

        Args:
            step_output (tuple or any): The output from the step function.
            step_key (str): The key of the step that was executed.

        Returns:
            list or None: The validated step output as a list, or None if no output.
        
        Raises:
            ValueError: If the number of returned elements does not match the expected count.
        """
        if not isinstance(step_output, tuple):
            step_output = [step_output]
        if (self.step_index[step_key].return_list == []) and (step_output[0] is None):
            return None
        if len(self.step_index[step_key].return_list) != len(step_output):
            raise ValueError("Error incorrect amount of return elements found")
        return step_output

    def __create_subcontext(self, step, step_key):
        """Creates a subcontext containing only the required dataframes for a step.

        Args:
            step (object): The step object requesting the subcontext.
            step_key (str): The key of the step.

        Returns:
            Context: A subcontext with the requested dataframes.
        """
        step_name = self.step_name_index[step_key]
        subcontext = base_context(f"{step_name}_subcontext")
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
        """Calculates the current step number.

        Returns:
            int: The next step number (number of steps + 1), or 0 if no steps have been added.
        """
        return self.__get_number_of_steps() + 1 if self.step_index else 0

    def __get_number_of_steps(self):
        """Calculates the number of steps added to the pipeline.

        Returns:
            int: The total number of steps.
        """
        return len(self.__get_step_keys())

    def __get_step_keys(self):
        """Retrieves all step keys.

        Returns:
            list: A list of step keys.
        """
        return list(self.step_index.keys())

    @log_error("Error adding target to step index")
    def __add_target_to_step(self, target, last=False):
        """Adds a target (extractor or loader) to the step index.

        Args:
            target (object): The target extractor or loader.
            last (bool): If True, adds the target to the end of the index; otherwise, to the beginning.
        """
        target_key = self.__parse_step(target)
        self.step_index.move_to_end(target_key, last=last)
        self.step_name_index.move_to_end(target_key, last=last)
        self.__display_message(f"Successfully added step with key: {target_key}")

    @log_error("Error adding targets to step index")
    def __add_targets(self):
        """Verifies and adds target extractor and loader to the pipeline.

        Raises:
            ValueError: If in "PROD" mode and no target extractor is set.
        """
        if not self.checked_targets:
            self.checked_targets = True
            if (self.mode != "DEV") and (not self.target_extractor):
                raise ValueError("Target extractor must be set before executing")
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
        """Parses a step and updates indexes.

        Generates a unique key for the step and updates the step index, step name index,
        parameter index, and dataframe index.

        Args:
            step (object): The step object to parse.

        Returns:
            str: The unique key generated for the step.
        """
        key_index = self.__get_current_step_number()
        step_key = generate_key(f"{step.step_name}_{key_index}")
        self.__update_step_index(step_key, step)
        self.__update_step_name_index(step_key, step.step_name)
        for param in step.params_list:
            self.__add_new_parameter(param)
        for dataframe in step.dataframes:
            self.__update_dataframe_index(step_key, dataframe)
        return step_key

    @log_error("Error Parsing Parameters, proper parameter value not found")
    def __parse_parameters(self, step_key):
        """Parses and prepares parameters for a step.

        Retrieves parameters in the following order of precedence:
          1. Value provided in the step instantiation.
          2. Current value in the parameter index.
          3. Default value provided in the step instantiation.
        Also retrieves chunking coordinates if applicable.

        Args:
            step_key (str): The key of the step to be executed.

        Returns:
            dict: A dictionary of parameters (and context if required) for the step.
        """
        kwargs = {}
        step = self.step_index[step_key]

        if step.needs_context:
            subcontext = self.__create_subcontext(step, step_key)
            kwargs["context"] = subcontext

        if (self.__chunker_is_set() and is_extractor(step, _raise=False) and hasattr(step, "chunk_size")):
            skiprows, nrows = self.chunker.dequeue()
            step.kwargs['skiprows'] = skiprows
            step.kwargs['nrows'] = nrows

        for param in step.params_list:
            input_value = step.input_params.get(param)
            curr_value = self.parameter_index.get(param)
            default_value = step.default_params.get(param)
            param_value = input_value or curr_value or default_value
            kwargs[param] = param_value
        self.__check_parsed_parameters(kwargs)
        return kwargs

    @log_error("Error Parsing Step Output")
    def __parse_step_output(self, step_output, step_key):
        """Parses the output from a step and updates indexes.

        Validates the output of the step and updates the global context and parameter index.

        Args:
            step_output (tuple): The output generated by the step.
            step_key (str): The key of the step that was executed.
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
        """Loads the pipeline state from the cache if available.

        Retrieves the last cached checkpoint and updates the parameter index and global context.

        Args:
            step_keys (list): List of current step keys.

        Returns:
            int: The index from which execution should resume.
        """
        start_index = 0
        cached_checkpoint = self.cache.get_cached_checkpoint(self.step_index)
        if cached_checkpoint and (cached_checkpoint in step_keys):
            self.parameter_index, self.globalcontext = self.cache.load(cached_checkpoint)
            start_index = step_keys.index(cached_checkpoint) + 1
            self.__display_message(f"Resuming execution from: {cached_checkpoint}", True)
        else:
            self.__display_message("No checkpoint found, starting from beginning...", True)
        return start_index

    def __store_in_cache(self, step_key):
        """Stores the current pipeline state in the cache.

        Args:
            step_key (str): The key of the completed step.
        """
        self.cache.store(self.step_index, self.parameter_index, self.globalcontext, step_key)
        self.__display_message(f"Checkpoint stored for step: {step_key}")

    @log_error("add_steps method requires a list of step objects")
    def add_steps(self, steps):
        """Adds multiple steps to the pipeline.

        Args:
            steps (list): A list of step objects to add.

        Raises:
            TypeError: If steps is not a list.
        """
        if not isinstance(steps, list):
            raise TypeError("try using a list...")
        for step in steps:
            self.add_step(step)

    @log_error("add_step method requires a step object")
    def add_step(self, step):
        """Adds a single step to the pipeline.

        If the step is a multi-extractor, its internal extractors are added individually.

        Args:
            step (object): The step object to be added.

        Raises:
            TypeError: If the step is not a valid step.
        """
        if is_multiextractor(step):
            for extractor in step.extractors:
                self.add_step(extractor)
        if is_step(step, _raise=True):
            step_key = self.__parse_step(step)
            self.__display_message(f"Successfully added: {step.step_name}, key: {step_key}")

    def cache_state(self, step_name="cache_state"):
        """Creates a cache state step.

        This step caches the current pipeline state and can be used to branch execution.

        Args:
            step_name (str, optional): Name for the cache state step. Defaults to "cache_state".

        Returns:
            CacheState: A predefined step that caches the pipeline state.
        """
        return CacheState(
            step_name=step_name,
            cache=self.cache,
            parameter_index=self.parameter_index,
            globalcontext=self.globalcontext,
        )

    def reload_cached_state(self, cache_key, step_name="reload_cached_state"):
        """Creates a reload cache state step.

        This step reloads a previously cached state, allowing the pipeline to branch.

        Args:
            cache_key (int): The index of the cached state.
            step_name (str, optional): Name for the reload cache state step. Defaults to "reload_cached_state".

        Returns:
            ReloadCacheState: A predefined step that reloads the cached state.
        """
        return ReloadCacheState(
            step_name=step_name,
            cache_key=cache_key,
            cache=self.cache,
            pipeline=self
        )

    def reset_cache(self, step_name="reset_cache", delete_directory=False):
        """Creates a reset cache step.

        This step resets the cache during execution.

        Args:
            step_name (str, optional): Name for the reset cache step. Defaults to "reset_cache".
            delete_directory (bool, optional): If True, deletes the cache directory.
                Defaults to False.

        Returns:
            ResetCache: A predefined step that resets the cache.
        """
        return ResetCache(
            step_name=step_name,
            cache=self.cache,
            delete_directory=delete_directory
        )

    def __perform_step(self, step_key):
        """Executes a single step of the pipeline.

        Retrieves necessary parameters, executes the step, validates its output, and updates the cache.
        Skips loader steps in "DEV" mode.

        Args:
            step_key (str): The key of the step to be executed.
        """
        if is_loader(self.step_index[step_key], _raise=False) and self.mode == "DEV":
            return
        step_params = self.__parse_parameters(step_key)
        step_output = self.step_index[step_key](**step_params)
        self.__parse_step_output(step_output, step_key)
        self.__update_cache(step_key)

    @log_error("Error executing Pipeline...")
    def execute(self, chunker=None):
        """Executes the pipeline.

        Performs validation on targets, chunker, cache, and logger.
        Displays execution messages and times the overall execution.

        Args:
            chunker (subclass of Chunker, optional): A chunker class to partition execution.
                If provided, sets the pipeline's chunker.
        """
        self.__add_targets()
        if chunker is not None:
            self.chunker = chunker

        step_keys = self.__get_step_keys()
        start_index = 0 if not self.__cache_is_set() else self.__load_from_cache(step_keys)

        start_time = time.time()
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
        self.__display_message(f"Beginning ETL Execution at time: {curr_time} ...", True)

        total_steps = self.__get_number_of_steps() - start_index
        with tqdm(total=total_steps, desc="Executing Pipeline") as pbar:
            for step_key in step_keys[start_index:]:
                self.__display_message(f"Executing Step: {self.step_name_index[step_key]} ", True)
                self.__perform_step(step_key)
                self.__display_message(f"Step: {self.step_name_index[step_key]} completed...")
                pbar.update(1)

        if self.chunker is not None:
            if self.chunker.keep_executing:
                self.parameter_index, self.globalcontext = self.chunker.reload()
                self.execute(chunker=chunker)
        else:
            end_time = time.time()
            curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
            self.__display_message(f"ETL Execution Finished at time: {curr_time} ...", True)
            elapsed_time = end_time - start_time
            if elapsed_time > 1.0:
                self.__display_message(f"Total Execution Time: {elapsed_time} seconds", True)