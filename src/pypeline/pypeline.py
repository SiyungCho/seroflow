"""
Module: pypeline

This module implements an ETL pypeline framework using the Pypeline class.
It provides functionality for managing and executing a sequence of data processing
steps with support for caching, logging, parameter management, and execution chunking.

The module integrates with several sub-components such as custom logging, caching,
context management, transformation utilities, chunking, and type validation
to offer a robust and extensible pypeline architecture.

Classes:
    Pypeline: Core class to construct, manage, and execute an ETL pypeline.
              It enables the addition of steps, manages dependencies via a
              global context and parameter index, and supports various execution modes.
"""
import logging
import time
from collections import OrderedDict
from tqdm.auto import tqdm

from .log import CustomLogger
from .cache import AbstractCache, LFUCache
from .context import Context as base_context
from .transform import CacheState, ReloadCacheState, ResetCache
from .chunker import Chunker
from .wrappers import log_error
from .utils import generate_key
from .types import is_step, is_extractor, is_multiextractor
from .types import is_loader, is_context, is_context_object

class Pypeline():
    """
    Pypeline Class

    The Pypeline class provides a framework for constructing and executing ETL pypelines with built-in support 
    for state caching, logging, and chunked execution. It allows dynamic addition of processing steps while 
    managing inter-step dependencies through a global context and parameter index. The pypeline can operate in 
    different modes ("DEV", "TEST", "PROD") which alter its execution behavior (e.g., skipping loader steps in DEV mode).

    Key Features:
        - Dynamically add individual or multiple steps to the pypeline.
        - Manage shared parameters and dataframes across steps via a global context.
        - Support for caching intermediate states to enable execution resumption.
        - Integration with custom or user-defined logging mechanisms to record pypeline events.
        - Optional support for chunking, allowing segmented processing of large datasets.
        - Automatic validation and indexing of extractors, loaders, and step outputs.
        - Flexible configuration through properties and setters ensuring type safety and proper initialization.

    Usage Example:
        >>> from pypeline import Pypeline
        >>> pypeline = Pypeline(cache=True, logger=True, mode="DEV")
        >>> pypeline.add_step(my_step)
        >>> pypeline.execute()

    Attributes:
        logger (logging.Logger or None): 
            Logger instance used for tracking pypeline execution details.
        mode (str): 
            The current execution mode ("DEV", "TEST", or "PROD") that affects how steps are processed.
        cache (AbstractCache or None): 
            Caching mechanism for storing intermediate pypeline states.
        parameter_index (dict): 
            Dictionary for storing parameters and variables shared across steps.
        step_index (OrderedDict): 
            Ordered dictionary mapping unique step keys to their corresponding step objects.
        step_name_index (OrderedDict): 
            Ordered dictionary mapping unique step keys to the step names.
        dataframe_index (dict): 
            Dictionary mapping step keys to requested dataframe names.
        globalcontext (Context): 
            Global context object that holds all dataframes used throughout the pypeline.
        chunker (Chunker or None): 
            Optional chunker object to partition and manage segmented execution.
    """

    def __init__(self, cache=False, logger=False, mode="DEV"):
        """
        Pypeline Class Constructor method.
        Initializes Pypeline Object with necessary parameters
            - cache
            - logger
            - mode

        Arguments: 
            logger (python.logging, Bool): 
                Default: False
                    Does not instantiate a logger, no logging used.
                True:
                    Instantiates default logger: CustomLogger
                python.logging:
                    User defined python.logging object.
            cache (AbstractCache subclass, Bool):
                Default: False
                    Does not instantiate a cache, no cache used.
                True:
                    Instantiates default cache: LFUCache
                AbstractCache subclass:
                    User defined Cache object must be derived from AbstractCache class.
            mode (str: ["DEV", "PROD"]):
                Default: "DEV"
                    Instantiates Pypeline as Development Mode
                "PROD":
                    Instantiates Pypeline as Production Mode

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
        Pypeline Object Destructor method.
        Deletes necessary components on Program Completion or Object Deletion.
        """

    def __str__(self):
        """
        Pypeline Object Custom Print method.
        Used to display internal Parameter Index, Step Index and Dataframe Index.
        """
        print("----Pypeline Object----")
        print(f"Parameters Index: {self.parameter_index}")
        print(f"Step Index: {self.step_index}")
        print(f"Step Name Index: {self.step_name_index}")
        print(f"Dataframe Index: {self.dataframe_index}")
        return "-----------------------"

    def __display_message(self, message, _print=False):
        """
        Custom display method.
        Used to display messages, if necessary or log messages if logger is initialized.

        Arguments:
            message (str): 
                Formatted message to be printed, logged or both.
            _print (bool):
                True:
                    Message is printed.
                False:
                    Message is not printed.
        """
        if self.logger_is_set():
            self.logger.info(message)
        if _print:
            print(message)

    @property
    def logger(self):
        """
        Logger Property Getter Method.
        Logger Property (Optional):
        Used to continuously log any execution info or errors.
        Works with @log_error() wrapper to wrap callable in try-except and log any errors.

        Returns:
            self.__logger
        """
        return self.__logger

    @property
    def target_extractor(self):
        """
        Target Extractor Property Getter Method.
        Target Extractor Property (Required):
        Used to verify that pypeline execution always begins on an Extract Step.
        Ensures that there is always some data in execution of the pypeline object.

        Returns:
            self.__target_extractor
        """
        return self.__target_extractor

    @property
    def target_loader(self):
        """
        Target Loader Property Getter Method.
        Target Loader Property (Optional):
        Used to verify that data is loaded as final step.

        Returns:
            self.__target_loader
        """
        return self.__target_loader

    @property
    def cache(self):
        """
        Cache Property Getter Method.
        Cache Property (Optional):
        Stores cache object.
        Used to cache any steps in development or in execution.
        In execution, cache can be used to 'branch' steps by saving the current state.
        In development, cache is used to store the state on a completed step so that
        on rerun, execution continues from last completed step.

        Returns:
            self.__cache
        """
        return self.__cache

    @property
    def parameter_index(self):
        """
        Parameter Index Property Getter Method.
        Parameter Index Property (Required):
        Used to store parameters/variables to be used across steps.
        Step Functions can pass variables to be saved through the return statement.
        Pypeline object will read the return statement,
        then save/update the value of the variable inside parameter index.
        * Steps are not required to have parameters

        Mapping:
            {
                Parameter name: Parameter value,
                ...
            }

        Returns:
            self.__parameter_index
        """
        return self.__parameter_index

    @property
    def step_index(self):
        """
        Step Index Property Getter Method.
        Step Index Property (Required):
        Used to store Step Objects.
        Step Objects are added using the add_step() or add_steps() public methods.
        Step Objects are then verified, and pass through the parse_step() public method.
        Unique Step key is created by hashing: step name (often function name) and step num.
        Step Object and Key is then stored for future use in step index.
        * All Step Objects are required to be added to step index.

        Mapping:
            {
                Step Key: Step Object,
                ...
            }

        Returns:
            self.__step_index
        """
        return self.__step_index

    @property
    def step_name_index(self):
        """
        Step Name Index Property Getter Method.
        Step Name Index Property (Required):
        Used to Map Step Names to Step Keys.
        Unique Step key is created by hashing: step name (often function name) and step num.
        Step Name and Key is then stored for future use in step name index.
        * All Step Objects are required to be added to step name index.

        Mapping:
            {
                Step Key: Step Name,
                ...
            }

        Returns:
            self.__step_name_index
        """
        return self.__step_name_index

    @property
    def dataframe_index(self):
        """
        DataFrame Index Property Getter Method.
        DataFrame Index Property (Required):
        Used to Map Step Keys with their requested Dataframes.
        Step Key and corresponding list of dataFrame names is stored.
        * Steps are not required to list dataframes needed, 
        * however, if 'context' argument is found in step function signature then global context is given.

        Mapping:
            {
                Step Key: [DataFrame Name, DataFrame Name, ...],
                ...
            }

        Returns:
            self.__dataframe_index
        """
        return self.__dataframe_index

    @property
    def globalcontext(self):
        """
        Global Context Property Getter Method.
        Global Context Property (Required):
        Stores context object.
        Used to store all dataframes in single context object.
        Pypeline will retrieve requested dataframe from global context if specified by step.
        Or, will return entire global context (ie all dataframes).

        Returns:
            self.__globalcontext
        """
        return self.__globalcontext

    @property
    def chunker(self):
        """
        Chunker Property Getter Method.
        Chunker Property (Optional):
        Stores chunker object.
        Used to store/initialize necessary properties to perform chunking on pypeline execution.
        Chunker is passed in the pypeline.execute() method.

        Returns:
            self.__chunker
        """
        return self.__chunker

    @property
    def mode(self):
        """
        Mode Property Getter Method.
        Mode Property (Optional):
        Used to determine current execution Mode: "DEV" or "PROD"
        Pypeline Execution will change depending on mode.
        DEV:
            Loader Steps are skipped so that data can first be tested without actually loading.
        PROD:
            All Loader Steps are executed.

        Returns:
            self.__mode
        """
        return self.__mode

    @logger.setter
    @log_error("Logger must be a logging object")
    def logger(self, logger):
        """
        Logger Property Setter Method.
        Receives argument logger.
        Verifies that argument logger is type Bool or python.logging.

        Arguments:
            logger (python.logging, Bool):
                True:
                    Default CustomLogger is initialized.
                False:
                    No logger is initialized.
                python.logging:
                    Predefined logger is initialized.

        Raises:
            TypeError:
                Argument logger is not of type Bool or python.logging.
        """
        if not logger:
            self.__logger = None
        elif isinstance(logger, logging.Logger):
            self.__logger = logger
            self.__display_message("Logger set...")
        elif logger is True:
            self.__logger = CustomLogger("pypeline").logger
            self.__display_message("Logger set...")
        else:
            raise TypeError("Logger must be a logging object")

    @target_extractor.setter
    @log_error("Verify Extractor Type")
    def target_extractor(self, extractor):
        """
        Target Extractor Property Setter Method.
        Receives argument extractor.
        Verifies that argument extractor is type Extractor or MultiExtractor.

        Arguments:
            extractor (Extractor, MultiExtractor):
                Initializes Target Extractor property.

        Raises:
            TypeError:
                Argument extractor is not of type Extractor or MultiExtractor.
        """
        if is_extractor(extractor, _raise=False):
            self.__target_extractor = extractor
        elif is_multiextractor(extractor, _raise=False):
            self.__target_extractor = extractor
        else:
            raise TypeError("Extractor must be extractor or multiextractor")
        self.__display_message("Target extractor set...")

    @target_loader.setter
    @log_error("Verify Loader Type")
    def target_loader(self, loader):
        """
        Target Loader Property Setter Method.
        Receives argument loader.
        Verifies that argument loader is type Loader.

        Arguments:
            loader (Loader):
                Initializes Target Loader property.

        Raises:
            TypeError:
                Argument loader is not of type Loader.
        """
        if is_loader(loader, _raise=True):
            self.__target_loader = loader
            self.__display_message("Target loader set...")

    @parameter_index.setter
    @log_error("Parameter index must be a dictionary")
    def parameter_index(self, parameter_index):
        """
        Parameter Index Property Setter Method.
        Receives argument parameter_index.
        Verifies that parameter_index loader is type Dict.

        Arguments:
            parameter_index (Dict):
                Initializes Parameter Index property.

        Raises:
            TypeError:
                Argument parameter_index is not of type Dict.
        """
        if not isinstance(parameter_index, dict):
            raise TypeError("Parameter index must be a dictionary")
        self.__parameter_index = parameter_index

    @globalcontext.setter
    @log_error("Global context must be a context object")
    def globalcontext(self, globalcontext):
        """
        Global Context Property Setter Method.
        Receives argument globalcontext.
        Verifies that globalcontext is type Context.

        Arguments:
            globalcontext (Context):
                Initializes Global Context property.

        Raises:
            TypeError:
                Argument globalcontext is not of type Context.
        """
        if not is_context(globalcontext):
            raise TypeError("Global context must be a Context object")
        self.__globalcontext = globalcontext

    @cache.setter
    @log_error("Cache must be an instance of AbstractCache")
    def cache(self, cache):
        """
        Cache Property Setter Method.
        Receives argument cache.
        Verifies that argument cache is type Bool or subclass to AbstractCache.

        Arguments:
            cache (subclass to AbstractCache, Bool):
                True:
                    Default LFUCache is initialized.
                False:
                    No cache is initialized.
                subclass to AbstractCache:
                    Predefined cache is initialized.

        Raises:
            TypeError:
                Argument cache is not of type Bool or subclass to AbstractCache.
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

    @mode.setter
    @log_error("Mode must be either DEV, TEST, or PROD")
    def mode(self, mode):
        """
        Mode Property Setter Method.
        Receives argument mode.
        Verifies that mode is type string and value: "DEV", "TEST" or "PROD".

        Arguments:
            mode (str):
                "DEV":
                    Initializes Mode to value "DEV".
                "TEST":
                    Initializes Mode to value "TEST".
                "PROD":
                    Initializes Mode to value "PROD".

        Raises:
            TypeError:
                Argument mode is not of type str or has value: "DEV", "TEST" or "PROD".
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
        Chunker Property Setter Method.
        Receives argument chunker.
        Verifies that argument chunker is a class and a subclass of Chunker.
        Adds a reset cache step if a cache is also initialized.
        Adding Reset ensures that cache is not used on chunks.
        Saves current state of global context and parameter index.

        Arguments:
            chunker (subclass of Chunker):
                A class that is a subclass of Chunker.

        Raises:
            TypeError:
                If the provided chunker is not a subclass of Chunker.
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

    def logger_is_set(self):
        """
        Public Method: logger_is_set()
        Verifies if logger is initialized.
        Must be public as wrapper, @log_error() uses method.

        Returns (Bool):
            True:
                Logger is initialized.
            False:
                Logger is not initialized.
        """
        if not self.logger:
            return False
        return True

    def __cache_is_set(self):
        """
        Private Method: __cache_is_set()
        Verifies if cache is initialized.

        Returns (Bool):
            True:
                Cache is initialized.
            False:
                Cache is not initialized.
        """
        if not self.cache:
            return False
        return True
    
    def __chunker_is_set(self):
        """
        Private Method: __chunker_is_set()
        Verifies if chunker is initialized.

        Returns (Bool):
            True:
                Chunker is initialized.
            False:
                Chunker is not initialized.
        """
        if not self.chunker:
            return False
        return True

    def __update_parameter_index(self, parameter, value):
        """
        Private Method: __update_parameter_index()
        Updates parameter index values.

        Arguments:
            parameter (string):
                Parameter Name to be updated.
            value (Any):
                Parameter value to add/update.
        """
        self.parameter_index[parameter] = value

    def __add_new_parameter(self, parameter):
        """
        Private Method: __add_new_parameter()
        Adds new empty parameter to parameter index.
        Used in __parse_step() method.

        Arguments:
            parameter (string):
                Parameter Name to be added.
        """
        if parameter not in self.parameter_index:
            self.parameter_index[parameter] = None

    def __update_step_index(self, step_key, step):
        """
        Private Method: __update_step_index()
        Updates step index values.

        Arguments:
            step_key (string):
                Step Key to be updated.
            step (Step Object):
                Step Object to add/update.
        """
        self.step_index[step_key] = step

    def __update_step_name_index(self, step_key, step_name):
        """
        Private Method: __update_step_name_index()
        Updates step name index values.

        Arguments:
            step_key (string):
                Step Key to be updated.
            step_name (string):
                Step Name to add/update.
        """
        self.step_name_index[step_key] = step_name

    def __update_dataframe_index(self, step_key, dataframe_name):
        """
        Private Method: __update_dataframe_index()
        Updates dataframe index values.

        Arguments:
            step_key (string):
                Step Key to be updated.
            dataframe_name (string):
                Dataframe name to add/update.
        """
        if step_key not in self.dataframe_index:
            self.dataframe_index[step_key] = []
        self.dataframe_index[step_key].append(dataframe_name)

    def __update_globalcontext(self, subcontext):
        """
        Private Method: __update_globalcontext()
        Updates global context dataframes.
        Either Updates internal dataframe.
        Or, Adds new dataframe to global context.

        Arguments:
            subcontext (Context):
                Subcontext, contains dataframes to update in global context.
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
        Private Method: __update_cache()
        Updates cache values.
        Once step is completed, cache is then used to store current state of pypeline.

        Arguments:
            step_key (string):
                Parameter Name to be updated.
        """
        if self.__cache_is_set() and (not isinstance(self.step_index[step_key], ResetCache)):
            self.__store_in_cache(step_key)

    def __check_parsed_parameters(self, kwargs):
        """
        Private Method: __check_parsed_parameters()
        Validates created kwargs to be passed in step function.
        Ensures parameters do not contain empty values.

        Arguments:
            kwargs (dict):
                Mapped parameters and values to be passed into step function.
        """
        for key, value in kwargs.items():
            if value is None:
                error_message = f"Key: {key} has no value, check parameter index"
                raise ValueError(error_message)

    def __check_step_output(self, step_output, step_key):
        """
        Private Method: __check_step_output()
        Validates step output with intended step return list.
        Ensures number of returned values matches expected number of returned values.
        Returns step output as list or None.

        Arguments:
            step_output (tuple):
                Output generated by step function.
            step_key (string):
                Step Key for corresponding step function that was just executed.

        Returns:
            step_output (list):
                Verified step output as a list.
            None:
                if no return statement then nothing should be returned.
        Raises:
            ValueError:
                Number of Elements returned by step function 
                does not match expected number of return elements.
        """
        if not isinstance(step_output, tuple):
            step_output = [step_output]

        if (self.step_index[step_key].return_list == []) and (step_output[0] is None):
            return None
        if len(self.step_index[step_key].return_list) != len(step_output):
            raise ValueError("Error incorrect amount of return elements found")
        return step_output

    def __create_subcontext(self, step, step_key):
        """
        Private Method: __create_subcontext()
        Creates subcontext to be passed to step function.
        Subcontext contains only the dataframes needed from the global context.
        If step is of extractor type, then blank subcontext is returned.

        Arguments:
            step (Step Object):
                Step Object requesting dataframes.
            step_key (string):
                Step Key for corresponding step.

        Returns:
            subcontext (Context):
                Context object containing only the requested dataframes.
        """
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
        Private Method: __get_current_step_number()
        Calculates the step number for newest step.

        Returns:
            (Int):
                Number of Steps + 1, or 0 if No steps have been added.
        """
        return self.__get_number_of_steps() + 1 if self.step_index else 0

    def __get_number_of_steps(self):
        """
        Private Method: __get_number_of_steps()
        Calculates the number of steps.

        Returns:
            (Int):
                Number of Steps.
        """
        return len(self.__get_step_keys())

    def __get_step_keys(self):
        """
        Private Method: __get_step_keys()
        Gathers all step keys.

        Returns:
            (List):
                List of step keys.
        """
        return list(self.step_index.keys())

    @log_error("Error adding target to step index")
    def __add_target_to_step(self, target, last=False):
        """
        Private Method: __add_target_to_step()
        Adds targets to step index.

        Arguments:
            target (Extractor, Loader):
                Target Extractor/Loader to be added to step index.
            last (Bool):
                True:
                    target is added to end of step index.
                    Intended to be used with target loader.
                False:
                    target is added to beginning of step index.
                    Intended to be used with target extractor.
        """
        target_key = self.__parse_step(target)
        self.step_index.move_to_end(target_key, last=last)
        self.step_name_index.move_to_end(target_key, last=last)
        self.__display_message(f"Successfully added step with key: {target_key}")

    @log_error("Error adding targets to step index")
    def __add_targets(self):
        """
        Private Method: __add_targets()
        Verifies Targets before adding them to step index.
        If targets have already been checked then method returns.
        In "DEV" Mode target loader and extractor do not have to be set.
        Ensures that MultiExtractors are parsed, by adding single extractor steps.

        Raises:
            ValueError:
                If in "PROD" mode then extractor must be set.
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
        """
        Private Method: __parse_step()
        Creates step key and adds new step to step index and step name index.
        Updates parameter and dataframe index with new values.
        
        Arguments:
            step (Step Object):
                New step object to be added to indexes.

        Returns:
            step_key (string):
                Newly generated unique key for added step.
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
        """
        Private Method: __parse_parameters()
        Retrieves needed parameters and subcontext for step function.
        If chunker is used, then chunking coordinates (ie start position and nrows)
        for current chunk is retrieved.
        Gathers parameter value using hierarchy:
            1. Inputted value set in step object instantiation.
            2. Current value inside parameter index.
            3. Default value set in step object instantiation.

        Arguments:
            step_key (string):
                Step Key for current step function about to be executed.

        Returns:
            kwargs (dict):
                Mapped parameter values and subcontext requested by step function.
        """
        kwargs = {}
        step = self.step_index[step_key]

        if step.needs_context:
            subcontext = self.__create_subcontext(step, step_key)
            kwargs["context"] = subcontext

        if ((self.__chunker_is_set()) and (is_extractor(step, _raise=False)) and (hasattr(step, "chunk_size"))):
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
        """
        Private Method: __parse_step_output()
        Receives step outputs, validates step output, then updates indexes.
        Updates global context and parameter index.

        Arguments:
            step_output (tuple):
                Output generated by step function.
            step_key (string):
                Step Key for corresponding step function that was just executed.
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
        Private Method: __load_from_cache()
        On pypeline execution, if a cache is set then,
        the state of the pypeline object at the last cached completed step is loaded.
        The starting step's index is returned.
        If cache is not set or there is no cached checkpoint, execution starts at step 0.

        Arguments:
            step_keys (list):
                List of step keys currently in step index.

        Returns:
            start_index (int):
                position of first step to be executed.
        """
        start_index = 0
        cached_checkpoint = self.cache.get_cached_checkpoint(self.step_index)
        if cached_checkpoint and (cached_checkpoint in step_keys):
            self.parameter_index, self.globalcontext = self.cache.load(cached_checkpoint)
            start_index = step_keys.index(cached_checkpoint) + 1
            self.__display_message(f"Resuming execution from checkpoint: {cached_checkpoint}", True)
        else:
            self.__display_message("No checkpoint found, starting from the beginning...", True)
        return start_index

    def __store_in_cache(self, step_key):
        """
        Private Method: __store_in_cache()
        If cache is set, then once a step has fully completed,
        the state of execution at that point is cached.

        Arguments:
            step_key (string):
                Step Key for completed step
        """
        self.cache.store(self.step_index, self.parameter_index, self.globalcontext, step_key)
        self.__display_message(f"Checkpoint stored for step: {step_key}")

    @log_error("add_steps method requires a list of step objects")
    def add_steps(self, steps):
        """
        Public Method: add_steps()
        Adds list of steps to pypeline indexes.

        Arguments:
            steps (list):
                list of step objects to be addded.

        Raises:
            TypeError:
                steps argument must be of type list.
        """
        if not isinstance(steps, list):
            raise TypeError("try using a list...")
        for step in steps:
            self.add_step(step)

    @log_error("add_step method requires a step object")
    def add_step(self, step):
        """
        Public Method: add_step()
        Adds single step to pypeline indexes.
        If a multiextractor step is added then verifies internal steps.

        Arguments:
            step (Step Object):
                step object to be addded.

        Raises:
            TypeError:
                step argument must be of type Step.
        """
        if is_multiextractor(step):
            for extractor in step.extractors:
                self.add_step(extractor)
        if is_step(step, _raise=True):
            step_key = self.__parse_step(step)
            self.__display_message(f"Successfully added: {step.step_name} with key: {step_key}")

    def cache_state(self, step_name="cache_state"):
        """
        Public Method: cache_state()
        Intended to be used as a step itself and added using public method, add_step() or add_step().
        Caches the current state of pypeline object in execution.
        Can be used to 'branch' steps.

        Arguments:
            step_name (string):
                Default: "cache_state"
                Name for added cache state step.

        Returns:
            CacheState predefined step, compatible with any cache object 
            derived from AbstractCache class.
        """
        return CacheState(
            step_name=step_name,
            cache=self.cache,
            parameter_index=self.parameter_index,
            globalcontext=self.globalcontext,
        )

    def reload_cached_state(self, cache_key, step_name="reload_cached_state"):
        """
        Public Method: reload_cached_state()
        Intended to be used as a step itself and added using public method, add_step() or add_step().
        Reloads the state of cached state in pypeline execution.
        Can be used to 'branch' steps.

        Arguments:
            step_name (string):
                Default: "reload_cached_state"
                Name for added reload cache state step.
            cache_key (int):
                index for cached state, configuration depends on cache class used.

        Returns:
            ReloadCacheState predefined step, compatible with any cache object 
            derived from AbstractCache class.
        """
        return ReloadCacheState(
            step_name=step_name,
            cache_key=cache_key,
            cache=self.cache,
            pypeline=self
        )

    def reset_cache(self, step_name="reset_cache", delete_directory=False):
        """
        Public Method: reset_cache()
        Intended to be used as a step itself and added using public method, add_step() or add_step().
        Resets the cache in execution.

        Arguments:
            step_name (String):
                Default: "reset_cache"
                Name for added reset cache step.
            delete_directory (Bool):
                True:
                    cache directory is deleted.
                False:
                    cache directory is not deleted.

        Returns:
            ResetCache predefined step, compatible with any cache object 
            derived from AbstractCache class.
        """
        return ResetCache(
            step_name=step_name,
            cache=self.cache,
            delete_directory=delete_directory
        )

    def __perform_step(self, step_key):
        """
        Private Method: __perform_step()
        Executes the current step, by retrieving necessary parameters 
        and updating indexes with returned values.
        Skips loader steps if pypeline mode is set to "DEV"
        Updates Cache if set.

        Arguments:
            step_key (string):
                Step key for current step
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
        Public Method: execute()
        Initializes Pypeline Execution, performing validation on:
        targets, chunker, cache, logger.
        Displays execution messages, times total execution of all steps.

        Arguments:
            chunker (subclass to Chunker):
                Chunker objects which partitions execution depending on Chunker Type.
        """
        self.__add_targets()
        if chunker is not None:
            self.chunker = chunker

        step_keys = self.__get_step_keys()
        start_index = 0 if not self.__cache_is_set() else self.__load_from_cache(step_keys)

        start_time = time.time()
        self.__display_message(f"Beginning ETL Execution at time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))} ...", True)

        total_steps = self.__get_number_of_steps() - start_index
        with tqdm(total=total_steps, desc="Executing Pypeline") as pbar:
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
            self.__display_message(f"ETL Execution Finished at time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))} ...", True)
            elapsed_time = end_time - start_time
            if elapsed_time > 1.0:
                self.__display_message(f"Total Execution Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elapsed_time))} seconds", True)
