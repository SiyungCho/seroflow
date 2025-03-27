"""
Module: lfu_cache

This module provides a concrete implementation of a cache using the Least Frequently Used strategy.
The LFUCache class implements the AbstractCache interface to store, retrieve, and manage the states.
It supports caching of Pipeline parameters and global context, along with mechanisms to evict the 
least frequently used items when the cache capacity is exceeded, persist cache state to disk, and 
restore the state from saved checkpoints.
"""

import os
import json
from collections import defaultdict, OrderedDict
import gzip
import dill

from ..utils.utils import create_file, create_directory, get_function_hash
from .abstract_cache import AbstractCache


class LFUCache(AbstractCache):
    """
    LFUCache

    A concrete cache implementation that uses the Least Frequently Used (LFU) strategy.
    Class manages a cache of limited capacity, evicting the least frequently used items when full.
    Also supports persisting cache state to disk (using gzip and dill) and restoring it,
    as well as maintaining a configuration file to track cached steps.
    """

    def __init__(self, capacity=3, cache_dir=None, on_finish='delete'):
        """
        LFUCache Class Constructor method
        Initializes LFUCache Object with necessary parameters:
            - capacity
            - cache_dir
            - on_finish

        Arguments:
            capacity (int): 
                Default: 3
                    Stores a maximum of 3 items in cache at a time.
                int:
                    Maxmimum Number of Items to store in cache at a time.
            cache_dir (string):
                Default: None
                    Cache creates .cache directory using current working directory.
                string:
                    Specific cache directory path can be given.
            on_finish (str: "delete", None):
                Default: "delete"
                    Uses object destructor to delete files and directory when called.
                None:
                    Does nothing when destructor called.
        """
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)
        self.on_finish = on_finish

        self.__source_directory = os.path.abspath(os.getcwd())
        self.__cache_directory_path, self.__cache_config_path = self.__init_directory(cache_dir)

    def __del__(self):
        """
        LFUCache Destructor method.
        Deletes necessary components on Program Completion or Object Deletion.
        Uses on_finish property to specify certain actions.
        """
        if self.on_finish == 'delete':
            for file in os.listdir(self.__cache_directory_path):
                file_path = os.path.join(self.__cache_directory_path, file)
                os.remove(file_path)

    def __init_directory(self, cache_dir):
        """
        Public Method: __init_directory()
        Initializes Cache Directory and Configuration File.
        Creates .cache directory in current working directory if cache_dir is None.
        Creates config.json file in cache directory if not present.

        Arguments:
            cache_dir (string):
                Default: None
                    Cache creates .cache directory using current working directory.
                string:
                    Specific cache directory path can be given.

        Returns:
            cache_directory_path (string):
                Path to Cache Directory.
            cache_config_file_path (string):
                Path to Cache Configuration
        """
        if cache_dir is not None:
            cache_directory_path = cache_dir
            cache_config_file_path = None
            for file in os.listdir(cache_directory_path):
                if file.endswith(".json"):
                    cache_config_file_path = os.path.join(cache_directory_path, file)
                    break
            if cache_config_file_path is None:
                cache_config_file_path = os.path.join(cache_directory_path, "config.json")
                create_file(cache_config_file_path)
        else:
            cache_directory_path = os.path.join(self.__source_directory, ".cache")
            create_directory(cache_directory_path)
            cache_config_file_path = os.path.join(cache_directory_path, "config.json")
            create_file(cache_config_file_path)
        return cache_directory_path, cache_config_file_path

    def get(self, key):
        """
        Public Method: get()
        Retrieves value from cache using key.
        Increments Frequency of Key by 1.
        If Key is not present in cache, returns None.

        Arguments:
            key (int):
                Key to retrieve value from cache.

        Returns:
            value (Any):
                Value stored in cache.
            None:
                If Key is not present in cache.
        """
        if key not in self.key_to_val_freq:
            return (None, None)

        value, freq = self.key_to_val_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        new_freq = freq + 1
        self.freq_to_keys[new_freq][key] = None
        self.key_to_val_freq[key] = (value, new_freq)
        return value

    def put(self, value):
        """
        Public Method: put()
        Inserts value into cache.
        If cache is full, evicts least frequently used item.
        If value is a dictionary, extracts parameter_index and globalcontext.

        Arguments:
            value (Any):
                Value to be inserted into cache.

        Returns:
            None:
                If capacity is 0.
        """
        if self.capacity <= 0:
            return

        if isinstance(value, dict) and "parameter_index" in value and "globalcontext" in value:
            value = (value["parameter_index"], value["globalcontext"])

        key = len(self.key_to_val_freq)

        if key in self.key_to_val_freq:
            _, freq = self.key_to_val_freq[key]
            self.key_to_val_freq[key] = (value, freq)
            self.get(key)
            return

        if len(self.key_to_val_freq) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val_freq[evict_key]

        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

    def read_config(self):
        """
        Public Method: read_config()
        Reads Cache Configuration from config.json file.
        If file is not present, returns empty dictionary.

        Returns:
            conf (dict):
                Cache Configuration stored in config.json file.
            {}:
                If config.json file is not present.
        """
        try:
            with open(self.__cache_config_path, 'r', encoding="utf-8") as config_file:
                conf = json.load(config_file)
        except (json.JSONDecodeError, FileNotFoundError):
            conf = {}
        return conf

    def write_config(self, conf):
        """
        Public Method: write_config()
        Writes Cache Configuration to config.json file.
        If file is not present, creates new file.

        Arguments:
            conf (dict):
                Cache Configuration to be stored in config.json file.
        """
        with open(self.__cache_config_path, 'w', encoding="utf-8") as config_file:
            json.dump(conf, config_file, indent=4)

    def delete_cached_file(self, step_key):
        """
        Public Method: delete_cached_file()
        Deletes cached file from cache directory.

        Arguments:
            step_key (string):
                Key of the step to be deleted from cache.
        """
        file_to_delete = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

    def update_config(self, step_func, step_key, step_num):
        """
        Public Method: update_config()
        Updates Cache Configuration with new step information.
        If step information is already present, overrides it.
        If step information is not present, adds it to configuration.

        Arguments:
            step_func (function):
                Function to be stored in cache.
            step_key (string):
                Key of the step to be stored in cache.
            step_num (int):
                Index of the step to be stored in cache.
        """
        conf = self.read_config()
        conf['last_completed_step'] = step_key

        if 'steps' not in conf:
            conf['steps'] = OrderedDict()

        source_code, hash_code = get_function_hash(step_func)
        data = {
            "source_code": source_code,
            "func_hash": hash_code
        }
        steps_list = list(conf['steps'].items())

        if step_num < len(steps_list):
            overridden_key, _ = steps_list[step_num]
            if not self.compare_function_code(conf, overridden_key, step_func):
                self.delete_cached_file(overridden_key)
                steps_list.pop(step_num)

        steps_list.insert(step_num, (step_key, data))
        conf['steps'] = OrderedDict(steps_list)

        self.write_config(conf)

    def compare_function_code(self, conf, step_key, func):
        """
        Public Method: compare_function_code()
        Compares function code with configuration function code.
        If function code is same, returns True.
        If function code is different, returns False.

        Arguments:
            conf (dict):
                Cache Configuration to be compared.
            step_key (string):
                Key of the step to be compared.
            func (function):
                Function to be compared.

        Returns:
            True:
                If function code is same.
            False:
                If function code is different.
        """
        current_source_code, current_hash_code = get_function_hash(func)
        conf_source_code = conf['steps'][step_key].get("source_code")
        conf_hash_code = conf['steps'][step_key].get("func_hash")
        if current_hash_code != conf_hash_code:
            return False
        if current_source_code != conf_source_code:
            return False
        return True

    def get_cached_checkpoint(self, step_index):
        """
        Public Method: get_cached_checkpoint()
        Retrieves last completed step from cache configuration.
        Compares function code with configuration function code.
        If function code is different, returns previous step key.
        If function code is same, returns last completed step key.
        If no cached files found, returns None.

        Arguments:
            step_index (OrderedDict):
                Step Index of the Pipeline.

        Returns:
            None:
                If no cached files found.
            previous_step_key (string):
                Key of the previous step to be executed
        """
        conf = self.read_config()
        if conf == OrderedDict():
            # No cached files found
            return None

        last_completed_step = conf['last_completed_step']
        conf_steps = conf['steps']
        previous_step_key = None
        for conf_step_key, pipeline_step_key in zip(conf_steps.keys(), step_index.keys()):
            if conf_step_key != pipeline_step_key:
                return previous_step_key
            if not self.compare_function_code(conf,
                                              conf_step_key,
                                              step_index[conf_step_key].step_func):
                return previous_step_key
            if conf_step_key == last_completed_step:
                break
            previous_step_key = conf_step_key
        return last_completed_step

    def store(self, step_index, parameter_index, global_context, step_key):
        """
        Public Method: store()
        Stores cache state in cache directory.
        Creates a checkpoint file with cache state and step information.

        Arguments:
            step_index (OrderedDict):
                Step Index of the Pipeline.
            parameter_index (dict):
                Parameter Index of the Pipeline.
            global_context (dict):
                Global Context of the Pipeline.
            step_key (string):
                Key of the step to be stored in cache.
        """
        step_num = list(step_index.keys()).index(step_key)
        self.update_config(step_index[step_key].step_func, step_key, step_num)
        checkpoint_file = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        cache_state = {
            "capacity": self.capacity,
            "min_freq": self.min_freq,
            "key_to_val_freq": self.key_to_val_freq,
            "freq_to_keys": self.freq_to_keys
        }
        with gzip.open(checkpoint_file, 'wb') as f:
            dill.dump((parameter_index, global_context, cache_state), f)

    def load(self, step_key):
        """
        Public Method: load()
        Loads cache state from cache directory.
        Retrieves cache state and step information from checkpoint file.

        Arguments:
            step_key (string):
                Key of the step to be loaded from cache.

        Returns:
            parameter_index (dict):
                Parameter Index of the Pipeline.
            global_context (dict):
                Global Context of the Pipeline
        """
        checkpoint_file = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        with gzip.open(checkpoint_file, 'rb') as f:
            parameter_index, global_context, cache_state = dill.load(f)

        self.capacity = cache_state["capacity"]
        self.min_freq = cache_state["min_freq"]
        self.key_to_val_freq = cache_state["key_to_val_freq"]
        self.freq_to_keys = cache_state["freq_to_keys"]

        return parameter_index, global_context

    def reset(self, delete_directory=False):
        """
        Public Method: reset()
        Resets Cache State.
        Deletes all files in cache directory.
        Deletes cache directory if delete_directory is True.

        Arguments:
            delete_directory (bool):
                Default: False
                    Does not delete cache directory.
                True:
                    Deletes cache directory.
        """
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

        if delete_directory:
            for file in os.listdir(self.__cache_directory_path):
                file_path = os.path.join(self.__cache_directory_path, file)
                os.remove(file_path)
