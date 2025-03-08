"""Module that implements a Least Frequently Used (LFU) cache.

This module defines the LFUCache class, which provides a caching mechanism
that evicts the least frequently used items when the cache reaches its capacity.
It also includes functionality to persist and load the cache state to/from
disk, as well as to maintain a configuration of processing steps.
"""

import os
import json
from collections import defaultdict, OrderedDict
import gzip
import dill

from ..utils.utils import create_file, create_directory, get_function_hash
from .abstract_cache import AbstractCache


class LFUCache(AbstractCache):
    """LFUCache implements a least frequently used caching strategy.

    The cache evicts the item with the lowest access frequency when its
    capacity is exceeded. Additionally, LFUCache supports persisting its
    state and configuration to disk.
    """

    def __init__(self, capacity=3, cache_dir=None):
        """
        Initialize a new LFUCache instance.

        Args:
            capacity (int, optional): Maximum number of items in the cache.
                Defaults to 3.
            cache_dir (str, optional): Directory path for storing cache files.
                If None, a default '.cache' directory in the current working
                directory will be used.
        """
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

        self.__source_directory = os.path.abspath(os.getcwd())
        self.__cache_directory_path, self.__cache_config_path = self.init_directory(cache_dir)

    def init_directory(self, cache_dir):
        """
        Initialize the cache directory and configuration file.

        This method determines the appropriate directory for cache storage.
        If a cache directory is provided, it uses that directory and looks for an
        existing JSON configuration file; otherwise, it creates a default '.cache'
        directory in the current working directory and creates a new configuration file.

        Args:
            cache_dir (str or None): Custom directory for cache storage. If None,
                the default directory is used.

        Returns:
            tuple: A tuple containing the cache directory path and the cache
            configuration file path.
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
        Retrieve a value from the cache and update its access frequency.

        If the key is not present, returns (None, None). Otherwise, the method
        increments the frequency count of the key and returns its associated value.

        Args:
            key: The cache key to retrieve.

        Returns:
            The value associated with the key if it exists; otherwise, (None, None).
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
        Add a value to the cache, evicting the least frequently used item if necessary.

        If the value is a dictionary containing "parameter_index" and "globalcontext",
        it converts it into a tuple. If the key already exists, it updates the value
        and its frequency. Otherwise, if the cache is full, the least frequently used
        entry is evicted before inserting the new value.

        Args:
            value: The value to be cached.
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
        Read and return the cache configuration from the configuration file.

        If the configuration file is missing or contains invalid JSON,
        an empty dictionary is returned.

        Returns:
            dict: The cache configuration.
        """
        try:
            with open(self.__cache_config_path, 'r', encoding="utf-8") as config_file:
                conf = json.load(config_file)
        except (json.JSONDecodeError, FileNotFoundError):
            conf = {}
        return conf

    def write_config(self, conf):
        """
        Write the provided configuration dictionary to the configuration file.

        Args:
            conf (dict): The configuration data to be written.
        """
        with open(self.__cache_config_path, 'w', encoding="utf-8") as config_file:
            json.dump(conf, config_file, indent=4)

    def delete_cached_file(self, step_key):
        """
        Delete the cached file associated with the given step key, if it exists.

        Args:
            step_key: The key identifying the cached checkpoint file to delete.
        """
        file_to_delete = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

    def update_config(self, step_func, step_key, step_num):
        """
        Update the cache configuration with information about a processing step.

        This method updates the configuration file to record the last completed step,
        and maintains an ordered list of steps with their source code and function hash.
        If an existing step's function code has changed, the corresponding cached file is deleted.

        Args:
            step_func (callable): The function associated with the step.
            step_key: The unique identifier for the step.
            step_num (int): The index of the step in the processing sequence.
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
        Compare the source code and hash of a function against the configuration.

        Args:
            conf (dict): The current cache configuration.
            step_key: The key identifying the step in the configuration.
            func (callable): The function to compare.

        Returns:
            bool: True if the function's source code and hash match those stored
                  in the configuration; otherwise, False.
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
        Retrieve the key of the latest valid checkpoint based on the configuration.

        The method compares the stored configuration with the provided step index mapping.
        It returns:
            - The last completed step if no changes are detected,
            - The previous step if a change is detected,
            - None if the first step was modified.

        Args:
            step_index (dict): A mapping of step keys to step objects, where each
                step object has an attribute 'step_func'.

        Returns:
            The step key of the valid checkpoint, or None if no valid checkpoint exists.
        """
        conf = self.read_config()
        if conf == OrderedDict():
            # No cached files found
            return None

        last_completed_step = conf['last_completed_step']
        conf_steps = conf['steps']
        previous_step_key = None
        for conf_step_key, pypeline_step_key in zip(conf_steps.keys(), step_index.keys()):
            if conf_step_key != pypeline_step_key:
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
        Store the current cache state to a checkpoint file.

        This method updates the configuration with the current step's function
        information, then saves the cache state along with the provided parameter_index
        and global_context using gzip and dill.

        Args:
            step_index (dict): A mapping of step keys to step objects.
            parameter_index: The parameter index data to store.
            global_context: The global context data to store.
            step_key: The key identifying the current step.
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
        Load a cached checkpoint and restore the cache state.

        This method loads the checkpoint file identified by step_key, restores
        the cache state, and returns the parameter_index and global_context that
        were stored in the checkpoint.

        Args:
            step_key: The key identifying the checkpoint to load.

        Returns:
            tuple: A tuple containing parameter_index and global_context.
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
        Reset the cache to an empty state.

        This method clears the in-memory cache data. If delete_directory is True,
        it also deletes all files in the cache directory.

        Args:
            delete_directory (bool, optional): If True, delete all files in the
                cache directory. Defaults to False.
        """
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

        if delete_directory:
            for file in os.listdir(self.__cache_directory_path):
                file_path = os.path.join(self.__cache_directory_path, file)
                os.remove(file_path)
