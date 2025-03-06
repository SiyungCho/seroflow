import pickle
import gzip
import dill
from collections import defaultdict, OrderedDict
import os
import inspect
import hashlib
import json

from ..Utils.utils import *
from .Cache import abstract_cache

class LFUCache(abstract_cache):
    def __init__(self, capacity = 3, cache_dir = None):
        self.capacity = capacity
        self.min_freq = 0
        self.keys_to_value_freq = {} # key -> (value, frequency)
        self.freq_to_keys = defaultdict(OrderedDict) # frequency -> keys (recency ordered)

        self.__source_directory = os.path.abspath(os.getcwd())
        self.__cache_directory_path, self.__cache_config_path = self.init_directory(cache_dir)

    def init_directory(self, cache_dir):
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
        if key not in self.key_to_val_freq:
            return -1

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

    def put(self, key, value):
        if self.capacity <= 0:
            return

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

    def read_config(self):
        try:
            with open(self.__cache_config_path, 'r') as config_file:
                conf = json.load(config_file)
        except (json.JSONDecodeError, FileNotFoundError):
            conf = {}
        return conf

    def write_config(self, conf):
        with open(self.__cache_config_path, 'w') as config_file:
            json.dump(conf, config_file, indent=4)

    def update_config(self, pypeline, step_key):
        conf = self.read_config()
        conf['last_completed_step'] = step_key

        hash_code = get_function_hash(pypeline.step_index[step_key].step_func)
        conf[step_key] = {
            "func_hash": hash_code
        }
        #store function code for step_key inside json file
        self.write_config(conf)
        return

    def store(self, pypeline, step_key):
        checkpoint_file = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        with gzip.open(checkpoint_file, 'wb') as f:
            dill.dump(pypeline, f)
        self.update_config(pypeline, step_key)

    def compare_function_code(self, conf, step_key, func):
        current_hash_code = get_function_hash(func)
        conf_hash_code = conf[step_key].get("func_hash")
        if current_hash_code != conf_hash_code:
            return False
        return True

    def load(self, pypeline):
        conf = self.read_config()
        if conf == {}:
            return None
        
        last_completed_step = conf['last_completed_step']
        for step_key in pypeline.step_index.keys(): #actually we want to iterate through the step_keys in the config file not the pypeline
            if step_key == last_completed_step:
                break
            else:
                if not (self.compare_function_code(conf, step_key, pypeline.step_index[step_key].step_func)):
                    return previous_step_key if previous_step_key is not None else step_key
            previous_step_key = step_key
        return last_completed_step
        