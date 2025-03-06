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
        self.key_to_val_freq = {}  # key -> (value, frequency)
        self.freq_to_keys = defaultdict(OrderedDict)  # frequency -> keys (ordered by recency)

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
            # Return a tuple of two Nones so that the caller can unpack safely.
            return (None, None)
        
        value, freq = self.key_to_val_freq[key]
        # Remove from the current frequency list
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Increase frequency count and add to the new frequency list
        new_freq = freq + 1
        self.freq_to_keys[new_freq][key] = None
        self.key_to_val_freq[key] = (value, new_freq)
        return value

    def put(self, key, value):
        if self.capacity <= 0:
            return

        # If the value is a dict with state info, convert it to a tuple.
        if isinstance(value, dict) and "parameter_index" in value and "globalcontext" in value:
            value = (value["parameter_index"], value["globalcontext"])

        if key in self.key_to_val_freq:
            # Update value (if necessary) and bump the frequency.
            _, freq = self.key_to_val_freq[key]
            self.key_to_val_freq[key] = (value, freq)
            self.get(key)  # Update frequency count.
            return

        if len(self.key_to_val_freq) >= self.capacity:
            # Evict the least frequently used key (the oldest one among those).
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            if not self.freq_to_keys[self.min_freq]:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val_freq[evict_key]

        # Insert new key with frequency 1.
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

    def delete_cached_file(self, step_key):
        file_to_delete = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
        return

    def update_config(self, step_func, step_key, step_num):
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

        if (step_num < len(steps_list)):
            overridden_key, _ = steps_list[step_num]
            if not self.compare_function_code(conf, overridden_key, step_func):
                self.delete_cached_file(overridden_key)
                steps_list.pop(step_num)

        steps_list.insert(step_num, (step_key, data))
        conf['steps'] = OrderedDict(steps_list)

        self.write_config(conf)
        return

    def compare_function_code(self, conf, step_key, func):
        current_source_code, current_hash_code = get_function_hash(func)
        conf_source_code = conf['steps'][step_key].get("source_code")
        conf_hash_code = conf['steps'][step_key].get("func_hash")
        if current_hash_code != conf_hash_code:
            return False
        if current_source_code != conf_source_code:
            return False
        return True

    def get_cached_checkpoint(self, step_index):
        #Load cases:
        #case 1: no changes made to steps before last completed step return last completed step
        #case 2: change was found in step before last completed step return step right before change
        #case 3: first step was changed return None
        #case 4: last completed step is the last step return last completed step
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
            if not self.compare_function_code(conf, conf_step_key, step_index[conf_step_key].step_func):
                return previous_step_key
            if conf_step_key == last_completed_step:
                break
            previous_step_key = conf_step_key
        return last_completed_step
    
    def store(self, step_index, parameter_index, global_context, step_key):
        step_num = list(step_index.keys()).index(step_key)
        self.update_config(step_index[step_key].step_func, step_key, step_num)
        checkpoint_file = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        with gzip.open(checkpoint_file, 'wb') as f:
            #want to save pypeline.parameter_index and pypeline.global_context in the same dump
            dill.dump((parameter_index, global_context), f)
    
    def load(self, step_key):
        checkpoint_file = os.path.join(self.__cache_directory_path, f"{step_key}.pkl.gz")
        with gzip.open(checkpoint_file, 'rb') as f:
            parameter_index, global_context = dill.load(f)
        return parameter_index, global_context