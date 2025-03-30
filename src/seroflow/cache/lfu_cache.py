"""
Module: lfu_cache

Provides a concrete cache implementation using the Least Frequently Used (LFU) strategy.
Implements the AbstractCache interface, supporting automatic eviction of least frequently
used items, persisting cache state to disk, and restoring from checkpoints.
"""

import os
import json
from collections import defaultdict, OrderedDict
import gzip
import dill

from ..utils.utils import create_file, create_directory, get_function_hash
from .cache import AbstractCache


class LFUCache(AbstractCache):
    """Concrete cache implementation using Least Frequently Used (LFU) eviction.

    Manages a cache with limited capacity, evicting items based on usage frequency.
    Supports state persistence and restoration.
    """

    def __init__(self, capacity=3, cache_dir=None, on_finish='delete'):
        """Initializes an LFUCache instance.

        Args:
            capacity (int, optional): Maximum number of items to store. Defaults to 3.
            cache_dir (str, optional): Directory for cache storage. Defaults to None (uses CWD).
            on_finish (str or None, optional): Behavior on destruction ('delete' or None).
                Defaults to 'delete'.
        """
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)
        self.on_finish = on_finish

        self.__source_directory = os.path.abspath(os.getcwd())
        self.__cache_directory_path, self.__cache_config_path = self.__init_directory(cache_dir)

    def __del__(self):
        """Deletes cache files/directories upon object deletion if configured."""
        if self.on_finish == 'delete':
            for file in os.listdir(self.__cache_directory_path):
                file_path = os.path.join(self.__cache_directory_path, file)
                os.remove(file_path)

    def __init_directory(self, cache_dir):
        """Initializes cache directory and configuration file.

        Args:
            cache_dir (str): Directory path for cache storage.

        Returns:
            tuple[str, str]: Paths to cache directory and configuration file.
        """
        if cache_dir:
            cache_directory_path = cache_dir
            cache_config_file_path = next(
                (os.path.join(cache_directory_path, f) for f in os.listdir(cache_directory_path)
                 if f.endswith(".json")),
                os.path.join(cache_directory_path, "config.json")
            )
            if not os.path.exists(cache_config_file_path):
                create_file(cache_config_file_path)
        else:
            cache_directory_path = os.path.join(self.__source_directory, ".cache")
            create_directory(cache_directory_path)
            cache_config_file_path = os.path.join(cache_directory_path, "config.json")
            create_file(cache_config_file_path)

        return cache_directory_path, cache_config_file_path

    def get(self, key):
        """Retrieves and updates frequency of a cached item by key.

        Args:
            key (int): Key identifying cached item.

        Returns:
            Any: Cached value or None if not found.
        """
        if key not in self.key_to_val_freq:
            return None, None

        value, freq = self.key_to_val_freq[key]
        self.freq_to_keys[freq].pop(key)

        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        new_freq = freq + 1
        self.freq_to_keys[new_freq][key] = None
        self.key_to_val_freq[key] = (value, new_freq)

        return value

    def put(self, value):
        """Inserts a new item into the cache, evicting if necessary.

        Args:
            value (Any): Value to cache.
        """
        if self.capacity <= 0:
            return

        if isinstance(value, dict) and "parameter_index" in value and "globalcontext" in value:
            value = (value["parameter_index"], value["globalcontext"])

        key = len(self.key_to_val_freq)

        if key in self.key_to_val_freq:
            self.key_to_val_freq[key] = (value, self.key_to_val_freq[key][1])
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

    def store(self, step_index, parameter_index, global_context, step_key):
        """Stores pipeline state and cache state to disk.

        Args:
            step_index (OrderedDict): Pipeline steps.
            parameter_index (dict): Parameters of pipeline.
            global_context (dict): Global pipeline context.
            step_key (str): Step identifier.
        """
        # Implementation details omitted for brevity
        pass

    def load(self, step_key):
        """Loads pipeline and cache state from disk.

        Args:
            step_key (str): Step identifier.

        Returns:
            tuple[dict, dict]: Parameter index and global context.
        """
        # Implementation details omitted for brevity
        pass

    def reset(self, delete_directory=False):
        """Resets cache state and optionally deletes cache directory.

        Args:
            delete_directory (bool, optional): Deletes cache directory if True. Defaults to False.
        """
        self.min_freq = 0
        self.key_to_val_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)

        if delete_directory:
            for file in os.listdir(self.__cache_directory_path):
                os.remove(os.path.join(self.__cache_directory_path, file))
