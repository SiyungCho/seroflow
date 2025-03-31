"""
LFU Cache Module.

This module provides a concrete cache implementation using the least frequently used (LFU)
strategy. It implements the AbstractCache interface, supporting automatic eviction of the least
frequently used items, persisting cache state to disk, and restoring from checkpoints.
"""

import os
import json
from collections import defaultdict, OrderedDict
import gzip
import dill

from ..utils.utils import create_file, create_directory, get_function_hash
from .cache import AbstractCache


class LFUCache(AbstractCache):
    """A cache implementation using the Least Frequently Used (LFU) strategy.

    This class manages a cache with a limited capacity, automatically evicting the least
    frequently used items when full. It supports persisting cache state to disk and restoring
    from checkpoints, along with maintaining a configuration file to track cached steps.
    """

    def __init__(self, capacity=3, cache_dir=None, on_finish='delete'):
        """Initialize a new LFUCache instance.

        Args:
            capacity (int, optional): Maximum number of items to store in the cache. Defaults to 3.
            cache_dir (str, optional): Path to the cache directory. If ``None``, a ``.cache`` directory is
                created in the current working directory. Defaults to ``None``.
            on_finish (str, optional): Action to perform on object deletion. If set to ``delete``,
                cached files will be removed upon object deletion. Defaults to ``delete``.
        """
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)
        self.on_finish = on_finish

        self.__source_directory = os.path.abspath(os.getcwd())
        self.__cache_directory_path, self.__cache_config_path = self.__init_directory(cache_dir)

    def __del__(self):
        """Destructor that cleans up cached files if configured to do so.

        If the ``on_finish`` attribute is set to ``delete``, all files in the cache directory will
        be removed when the object is deleted.
        """
        if self.on_finish == 'delete':
            for file in os.listdir(self.__cache_directory_path):
                file_path = os.path.join(self.__cache_directory_path, file)
                os.remove(file_path)

    def __init_directory(self, cache_dir):
        """Initialize the cache directory and configuration file.

        If a cache directory is provided, it uses that directory; otherwise, it creates a ``.cache``
        directory in the current working directory. A configuration file ``config.json`` is created
        in the cache directory if it does not already exist.

        Args:
            cache_dir (str): Path to the cache directory. If ``None``, a ``.cache`` directory is created.

        Returns:
            tuple:
                - cache_directory_path (str): The path to the cache directory.
                - cache_config_file_path (str): The path to the cache configuration file.
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
        """Retrieve the value associated with the given key and update its frequency.

        If the key is not present in the cache, returns a ``tuple`` ``(None, None)``. Otherwise, the method
        increments the usage frequency of the item and returns its value.

        Args:
            key (int): The key of the cached item.

        Returns:
            Any: The cached value if found; otherwise, a tuple ``(None, None)``.
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
        """Insert a value into the cache, evicting the least frequently used item if necessary.

        If the value is a dictionary containing ``parameter_index`` and ``globalcontext`` keys, the method
        extracts these values. If the cache already contains an item with the generated key, it updates
        its value and frequency. When the cache is at capacity, it evicts the least frequently used item.

        Args:
            value (Any): The value to be inserted into the cache.

        Returns:
            ``None``
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
        """Read the cache configuration from the configuration file.

        Attempts to load the ``JSON`` configuration from the file. If the file is missing or contains
        invalid ``JSON``, an empty dictionary is returned.

        Returns:
            dict: The cache configuration, or an empty dictionary if reading fails.
        """
        try:
            with open(self.__cache_config_path, 'r', encoding="utf-8") as config_file:
                conf = json.load(config_file)
        except (json.JSONDecodeError, FileNotFoundError):
            conf = {}
        return conf

    def write_config(self, conf):
        """Write the provided configuration to the configuration file.

        The configuration is stored in ``JSON`` format in the cache configuration file.

        Args:
            conf (dict): The configuration data to write.
        """
        with open(self.__cache_config_path, 'w', encoding="utf-8") as config_file:
            json.dump(conf, config_file, indent=4)

    def delete_cached_file(self, step_key):
        """Delete the cached file associated with the given ``step_key``.

        Args:
            step_key (str): The key identifying the cached file to be deleted.
        """
        file_to_delete = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

    def update_config(self, step_func, step_key, step_num):
        """Update the cache configuration with new step information.

        The method reads the current configuration, updates the last completed step, and inserts or
        overrides the step information at the specified position. If an existing ``Step's`` function code
        differs from the new one, the associated cache file is deleted.

        Args:
            step_func (function): The function associated with the cache step.
            step_key (str): The key of the step to update.
            step_num (int): The index at which to insert the step information.
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
        """Compare the function's source code and hash with those stored in the configuration.

        Args:
            conf (dict): The cache configuration containing step information.
            step_key (str): The ``step_key`` corresponding to the step in the configuration.
            func (function): The function to compare.

        Returns:
            bool: ``True`` if the function's source code and hash match the configuration, ``False`` otherwise.
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
        """Retrieve the key of the last completed checkpoint from the configuration.

        The method compares the function codes of cached steps with the provided ``step_index``. If a
        mismatch is found, it returns the key of the previous step. If no cached files are found,
        the method returns None.

        Args:
            step_index (OrderedDict): An ordered dictionary representing the ``Pipeline's`` ``step_index``.

        Returns:
            str or None: The key of the last completed step if available; otherwise, ``None``.
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
        """Store the current cache state and ``Pipeline`` parameters to a checkpoint file.

        The method updates the configuration with the new step and writes a checkpoint file containing
        the cache state along with ``Pipeline`` parameters and global context.

        Args:
            step_index (OrderedDict): The ``step_index`` of the ``Pipeline``.
            parameter_index (dict): The ``Pipeline's`` ``parameter_index``.
            global_context (dict): The ``Pipeline's`` ``global_context``.
            step_key (str): The ``step_key`` identifying the step to be stored.
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
        """Load the cache state and ``Pipeline`` parameters from a checkpoint file.

        Reads the checkpoint file corresponding to the provided ``step_key``, restores the cache state,
        and returns the ``Pipeline`` parameters.

        Args:
            step_key (str): The key identifying the step to load from the cache.

        Returns:
            tuple: A tuple containing:
                - parameter_index (dict): The ``Pipeline's`` ``parameter_index``.
                - global_context (dict): The ``Pipeline's`` ``global_context``.
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
        """Reset the cache state and optionally delete cached files.

        This method clears all in-memory cache data. If ``delete_directory`` is ``True``, it also removes
        all files from the cache directory.

        Args:
            delete_directory (bool, optional): If ``True``, deletes all files in the cache directory.
                Defaults to ``False``.
        """
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

        if delete_directory:
            for file in os.listdir(self.__cache_directory_path):
                file_path = os.path.join(self.__cache_directory_path, file)
                os.remove(file_path)