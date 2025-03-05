import pickle
import gzip
from collections import defaultdict, OrderedDict
from .Cache import abstract_cache

class LFUCache(abstract_cache):
    def __init__(self, capacity = 3):
        self.capacity = capacity
        self.min_freq = 0
        self.keys_to_value_freq = {} # key -> (value, frequency)
        self.freq_to_keys = defaultdict(OrderedDict) # frequency -> keys (recency ordered)

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

    def store(self, file_path):
        state = {
            'cache_type': 'LFU',
            'capacity': self.capacity,
            'min_freq': self.min_freq,
            'key_to_val_freq': self.key_to_val_freq,
            'freq_to_keys': self.freq_to_keys,
        }
        with gzip.open(file_path, 'wb') as f:
            pickle.dump(state, f)
    
    @classmethod
    def load(cls, file_path):
        with gzip.open(file_path, 'rb') as f:
            state = pickle.load(f)
        
        if state.get('cache_type') != 'LFU':
            raise ValueError("The stored file does not contain an LFU cache state.")
        
        cache = cls(state['capacity'])
        cache.min_freq = state['min_freq']
        cache.key_to_val_freq = state['key_to_val_freq']
        cache.freq_to_keys = state['freq_to_keys']
        return cache