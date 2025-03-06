"""
This module provides the `pypeline` class, a framework for constructing and executing ETL (Extract, Transform, Load)
pipelines. The `pypeline` class manages pipeline steps, parameters, caching, and global context to facilitate
efficient ETL processes. It integrates with various helper modules for logging, caching, context management, and
data transformation.

Usage:
    Instantiate the `pypeline` class and add steps to build your ETL pipeline. Then, call the `execute` method to run
    the pipeline. The class supports caching and resuming from checkpoints, making it useful for long-running ETL jobs.
"""

import time
from collections import OrderedDict
from tqdm import tqdm

from .Log import custom_logger
from .Utils import generate_key
from .Types import is_extractor, is_loader, is_step, is_context, is_context_object
from .Cache import LFUCache
from .Context import context as base_context
from .Transform import cache_state
from .Transform import reload_cached_state
from .Transform import reset_cache


class pypeline():
    """
    A class for creating and executing an ETL (Extract, Transform, Load) pipeline.

    This pipeline manages steps, parameters, caching, and global context. It supports
    adding steps, updating parameters, caching state between steps, and executing the
    entire pipeline with logging.

    Attributes:
        logger: Logger instance for logging pipeline events.
        mode (str): The execution mode (e.g., "TEST").
        __target_extractor: The target extractor object.
        __target_loader: The target loader object.
        __cache: The caching mechanism used for saving the pipeline state.
        __parameter_index (dict): A dictionary mapping parameter names to values.
        __step_index (OrderedDict): An ordered dictionary mapping step keys to step objects.
        __step_name_index (OrderedDict): An ordered dictionary mapping step keys to step names.
        __dataframe_index (dict): A dictionary mapping step keys to lists of dataframe names.
        __globalcontext: Global context holding shared dataframes.
    """

    def __init__(self, cache_type=LFUCache, mode="TEST"):
        """
        Initialize a new pypeline instance.

        Args:
            cache_type: The cache class to be used for storing pipeline state.
                        Defaults to LFUCache.
            mode (str): The mode of execution for the pipeline (e.g., "TEST").
                        Defaults to "TEST".
        """
        self.logger = custom_logger("pypeline").logger
        self.mode = mode
        self.__target_extractor = None
        self.__target_loader = None
        self.__cache = cache_type()
        self.__parameter_index = {}
        self.__step_index = OrderedDict()
        self.__step_name_index = OrderedDict()
        self.__dataframe_index = {}
        self.__globalcontext = base_context("globalcontext")

    @property
    def target_extractor(self):
        """
        Get the target extractor.

        Returns:
            The target extractor if set; otherwise, None.
        """
        return self.__target_extractor

    @property
    def target_loader(self):
        """
        Get the target loader.

        Returns:
            The target loader if set; otherwise, None.
        """
        return self.__target_loader

    @property
    def cache(self):
        """
        Get the cache instance used by the pipeline.

        Returns:
            The cache instance.
        """
        return self.__cache

    @property
    def parameter_index(self):
        """
        Get the parameter index dictionary.

        Returns:
            dict: A mapping of parameter names to their current values.
        """
        return self.__parameter_index

    @property
    def step_index(self):
        """
        Get the step index.

        Returns:
            OrderedDict: A mapping of step keys to step objects.
        """
        return self.__step_index

    @property
    def step_name_index(self):
        """
        Get the step name index.

        Returns:
            OrderedDict: A mapping of step keys to step names.
        """
        return self.__step_name_index

    @property
    def dataframe_index(self):
        """
        Get the dataframe index.

        Returns:
            dict: A mapping of step keys to lists of dataframe names.
        """
        return self.__dataframe_index

    @property
    def globalcontext(self):
        """
        Get the global context.

        Returns:
            The global context containing shared dataframes.
        """
        return self.__globalcontext

    @target_extractor.setter
    def target_extractor(self, extractor):
        """
        Set the target extractor.

        Args:
            extractor: An extractor object that satisfies the extractor requirements.

        Side Effects:
            Logs the event when a valid extractor is set.
        """
        if is_extractor(extractor, True):
            self.__target_extractor = extractor
            self.logger.info("Target extractor set...")

    @target_loader.setter
    def target_loader(self, loader):
        """
        Set the target loader.

        Args:
            loader: A loader object that satisfies the loader requirements.

        Side Effects:
            Logs the event when a valid loader is set.
        """
        if is_loader(loader, True):
            self.__target_loader = loader
            self.logger.info("Target loader set...")

    @parameter_index.setter
    def parameter_index(self, parameter_index):
        """
        Set the parameter index.

        Args:
            parameter_index (dict): A dictionary mapping parameter names to values.
        """
        self.__parameter_index = parameter_index

    @globalcontext.setter
    def globalcontext(self, globalcontext):
        """
        Set the global context.

        Args:
            globalcontext: The new global context object.
        """
        self.__globalcontext = globalcontext

    def update_parameter_index(self, parameter, value):
        """
        Update a specific parameter's value in the parameter index.

        Args:
            parameter: The parameter key to update.
            value: The value to assign to the parameter.
        """
        self.parameter_index[parameter] = value

    def update_step_index(self, step_key, step):
        """
        Update the step index by adding a new step.

        Args:
            step_key: The unique key for the step.
            step: The step object to be added.
        """
        self.step_index[step_key] = step

    def update_step_name_index(self, step_key, step_name):
        """
        Update the step name index with a new step name.

        Args:
            step_key: The unique key for the step.
            step_name (str): The name of the step.
        """
        self.step_name_index[step_key] = step_name

    def update_dataframe_index(self, step_key, dataframe_name):
        """
        Update the dataframe index for a given step.

        If the step key does not exist in the index, it is initialized with an empty list.
        Then the dataframe name is appended to the list for that step.

        Args:
            step_key: The key for the step.
            dataframe_name (str): The name of the dataframe to be associated.
        """
        if step_key not in self.dataframe_index:
            self.dataframe_index[step_key] = []
        self.dataframe_index[step_key].append(dataframe_name)

    def update_globalcontext(self, subcontext):
        """
        Merge dataframes from a subcontext into the global context.

        For each dataframe in the subcontext, if it already exists in the global context,
        update its value; otherwise, add it as a new dataframe.

        Args:
            subcontext: The context containing dataframes to merge.
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
                self.logger.info("Added dataframe: %s to globalcontext", dataframe_name)

    def add_steps(self, steps):
        """
        Add multiple steps to the pipeline.

        Args:
            steps (list): A list of step objects.

        Raises:
            TypeError: If the provided steps argument is not a list.
        """
        if not isinstance(steps, list):
            raise TypeError("try using a list...")
        for step in steps:
            self.add_step(step)

    def add_step(self, step):
        """
        Add a single step to the pipeline.

        This method validates the step and adds it to the internal indices.

        Args:
            step: A step object that is validated via `is_step`.

        Side Effects:
            Logs the successful addition of the step.
        """
        if is_step(step, True):
            step_key = self.parse_step(step)
            print("Successfully added step with key: " + str(step_key))
            self.logger.info("Successfully added step with key: %s", step_key)
        else:
            # In case step is not valid, you may add additional handling here.
            pass

    def targets_found(self, _raise=False):
        """
        Check if both target extractor and loader have been set.

        Args:
            _raise (bool): If True, raises an Exception when a target is missing.
                           Defaults to False.

        Returns:
            bool: True if both targets are found; otherwise, False.

        Raises:
            Exception: If either the target extractor or loader is missing and _raise is True.
        """
        if (not self.target_extractor) or (not self.target_loader):
            if _raise:
                raise Exception("Target loader or extractor not found")
            return False
        return True

    def add_targets_to_steps(self):
        """
        Incorporate target extractor and loader into the step indices.

        For non-test modes, this method verifies the existence of both targets.
        It then adds the target extractor to the beginning and the target loader to the end
        of the step order.

        Side Effects:
            Updates the internal step indices and logs the operations.
        """
        if self.mode != "TEST":  # In test mode, targets may not be required.
            self.targets_found(_raise=True)
        if self.target_extractor:
            target_extractor_key = self.parse_step(self.target_extractor)
            self.logger.info("Successfully added step with key: %s", target_extractor_key)
            self.step_index.move_to_end(target_extractor_key, last=False)
            self.step_name_index.move_to_end(target_extractor_key, last=False)
        if self.target_loader:
            target_loader_key = self.parse_step(self.target_loader)
            self.logger.info("Successfully added step with key: %s", target_loader_key)
            self.step_index.move_to_end(target_loader_key)
            self.step_name_index.move_to_end(target_loader_key)

    def parse_step(self, step):
        """
        Parse a step and update internal indices with its details.

        Generates a unique key for the step based on its name and the current number
        of steps. Updates the step index, step name index, parameter index, and dataframe index
        as needed.

        Args:
            step: The step object to parse.

        Returns:
            str: The unique key generated for the step.
        """
        key_index = len(list(self.step_index.keys())) + 1 if self.step_index else 0
        step_key = generate_key(step.step_name + "_" + str(key_index))
        self.update_step_index(step_key, step)
        self.update_step_name_index(step_key, step.step_name)
        if step.params_list:
            for param in step.params_list:
                if param != "context" and param not in self.parameter_index:
                    self.update_parameter_index(param, None)
        if step.dataframes:
            for dataframe_name in step.dataframes:
                self.update_dataframe_index(step_key, dataframe_name)
        return step_key

    def parse_parameters(self, step_key):
        """
        Consolidate parameters for a given step.

        For each parameter in the step's parameter list (except 'context'), this method
        selects the appropriate value from input parameters, the current parameter index, or
        default parameters. For the 'context' parameter, a subcontext is created or updated.

        Args:
            step_key (str): The unique key identifying the step.

        Returns:
            dict: A dictionary of parameters and their resolved values.

        Raises:
            Exception: If a parameter value cannot be resolved.
        """
        kwargs = {}
        for param in self.step_index[step_key].params_list:
            if param != "context":
                if param in self.step_index[step_key].input_params:
                    input_value = self.step_index[step_key].input_params[param]
                else:
                    input_value = None

                curr_value = self.parameter_index[param]

                if param in self.step_index[step_key].default_params:
                    default_value = self.step_index[step_key].default_params[param]
                else:
                    default_value = None
                param_value = input_value or curr_value or default_value
            else:
                param_value = None
                step_name = self.step_name_index[step_key]
                subcontext = base_context(step_name + "_subcontext")

                if is_extractor(self.step_index[step_key], False):
                    param_value = subcontext

                if param_value is None:
                    desired_dataframes = (
                        self.dataframe_index[step_key]
                        if step_key in self.dataframe_index
                        else []
                    )
                    # If no desired dataframes, use the global context.
                    if desired_dataframes == []:
                        subcontext = self.globalcontext
                    else:
                        for dataframe_name in desired_dataframes:
                            subcontext.add_dataframe(
                                dataframe_name,
                                self.globalcontext.get_dataframe(dataframe_name),
                            )
                    param_value = subcontext
            if param_value is None:
                raise Exception("Error parameter value not found in any index")
            kwargs[param] = param_value
        return kwargs

    def parse_step_output(self, step_output, step_key):
        """
        Process the output from a step and update indices accordingly.

        Iterates over the step's output and, based on the type of each value,
        updates either the global context or the parameter index.

        Args:
            step_output (tuple or list): The output returned by the step.
            step_key (str): The unique key identifying the step.
        """
        for param, value in zip(self.step_index[step_key].return_list, step_output):
            if is_context(value):
                self.update_globalcontext(value)  # Update context index if value is a context.
            elif is_context_object(value):
                for _, item in value.items():
                    self.update_globalcontext(item)
            else:
                self.update_parameter_index(param, value)

    def validate_step_output(self, step_output, step_key):
        """
        Validate the output produced by a step.

        Ensures that the output is in tuple or list format and that its length
        matches the expected number of return elements for the step.

        Args:
            step_output: The raw output from the step.
            step_key (str): The unique key identifying the step.

        Returns:
            The validated output if it meets the expected format, or None if the step
            produced no output.

        Raises:
            Exception: If the number of output elements does not match the expected count.
        """
        if not isinstance(step_output, tuple):
            step_output = [step_output]

        if (self.step_index[step_key].return_list == []) and (step_output[0] is None):
            return None
        if len(self.step_index[step_key].return_list) != len(step_output):
            raise Exception("Error incorrect amount of return elements found")
        return step_output

    def cache_state(self, step_name="cache_state"):
        """
        Cache the current state of the pipeline.

        Delegates to the imported `cache_state` function, storing the current
        parameter index and global context.

        Args:
            step_name (str): An optional name for the cache state.
                              Defaults to "cache_state".

        Returns:
            The result from the `cache_state` function.
        """
        return cache_state(
            step_name=step_name,
            cache=self.cache,
            parameter_index=self.parameter_index,
            globalcontext=self.globalcontext,
        )

    def reload_cached_state(self, cache_key, step_name="reload_cached_state"):
        """
        Reload a cached pipeline state.

        Delegates to the imported `reload_cached_state` function, using the
        provided cache key to restore the pipeline's state.

        Args:
            cache_key: The key corresponding to the cached state.
            step_name (str): An optional name for the reload operation.
                             Defaults to "reload_cached_state".

        Returns:
            The result from the `reload_cached_state` function.
        """
        return reload_cached_state(
            step_name=step_name, cache_key=cache_key, cache=self.cache, pypeline=self
        )

    def reset_cache(self, step_name="reset_cache", delete_directory=False):
        """
        Reset the pipeline's cache.

        Delegates to the imported `reset_cache` function to clear the current cache.
        Optionally deletes the cache directory.

        Args:
            step_name (str): An optional name for the reset operation.
                             Defaults to "reset_cache".
            delete_directory (bool): If True, deletes the cache directory.
                                     Defaults to False.

        Returns:
            The result from the `reset_cache` function.
        """
        return reset_cache(
            step_name=step_name, cache=self.cache, delete_directory=delete_directory
        )

    def load_from_cache(self, step_keys):
        """
        Attempt to resume execution from a cached checkpoint.

        Checks if a valid cached checkpoint exists among the provided step keys.
        If found, loads the corresponding parameter index and global context, and
        returns the index from which to resume execution.

        Args:
            step_keys (list): List of step keys in the current pipeline.

        Returns:
            int: The index of the step from which to resume execution.
        """
        cached_checkpoint = self.cache.get_cached_checkpoint(self.step_index)
        if cached_checkpoint and (cached_checkpoint in step_keys):
            self.parameter_index, self.globalcontext = self.cache.load(cached_checkpoint)
            start_index = step_keys.index(cached_checkpoint) + 1
            self.logger.info("Resuming execution from checkpoint: %s", cached_checkpoint)
            print("Resuming execution from checkpoint: " + str(cached_checkpoint))
        else:
            start_index = 0
            self.logger.info("No valid checkpoint found, starting from the beginning...")
            print("No valid checkpoint found, starting from the beginning...")
        return start_index

    def store_in_cache(self, step_key):
        """
        Store the current pipeline state in the cache.

        Saves the current step index, parameter index, and global context using the
        provided step key as the checkpoint identifier.

        Args:
            step_key (str): The key of the step at which to store the checkpoint.
        """
        self.cache.store(self.step_index, self.parameter_index, self.globalcontext, step_key)
        self.logger.info("Checkpoint stored for step: %s", step_key)

    def execute(self, use_cache=True):
        """
        Execute the entire ETL pipeline.

        Performs the following operations:
          - Incorporates target extractor and loader into the step indices.
          - Determines the starting point based on available cache.
          - Iterates over each step, parsing parameters, executing the step,
            validating its output, and updating the global context.
          - Stores checkpoints after each step if caching is enabled.
          - Logs execution time and status for each step.

        Args:
            use_cache (bool): Whether to use caching to resume execution.
                              Defaults to True.
        """
        self.add_targets_to_steps()

        step_keys = list(self.step_index.keys())
        start_index = 0 if not use_cache else self.load_from_cache(step_keys)

        start_time = time.time()  # Start timer
        self.logger.info("Beginning ETL Execution at time: %s ...", start_time)
        for step_key in tqdm(step_keys[start_index:], desc="Executing Pypeline"):
            step_name = self.step_name_index[step_key]
            print("Executing Step: " + str(step_name))
            self.logger.info("Executing Step: %s", step_name)

            step_params = self.parse_parameters(step_key)
            step_output = self.validate_step_output(self.step_index[step_key](**step_params), step_key)
            if step_output:
                self.parse_step_output(step_output, step_key)

            if use_cache:
                self.store_in_cache(step_key)
            self.logger.info("Step: %s completed...", step_name)
        end_time = time.time()  # End timer
        self.logger.info("ETL Execution Finished at time: %s ...", end_time)
        elapsed_time = end_time - start_time
        self.logger.info("Total Execution Time: %.2f seconds", elapsed_time)

    def __str__(self):
        """
        Return a string representation of the pipeline's current state.

        This includes printing the parameter index, step index, step name index,
        and dataframe index.

        Returns:
            str: A summary string representing the pipeline.
        """
        print(self.parameter_index)
        print(self.step_index)
        print(self.step_name_index)
        print(self.dataframe_index)
        return "pypeline object"
