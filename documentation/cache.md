# Cache Module Documentation

This module defines the `AbstractCache` class, an abstract base class that specifies the required interface for caching mechanisms used within the ETL pypeline framework. Any concrete cache implementation must inherit from `AbstractCache` and implement the methods for inserting, retrieving, storing, loading, and resetting cache items. This ensures consistent cache behavior across different caching strategies.

---

## Overview

The `AbstractCache` class declares the following abstract methods that must be implemented by derived classes:

- **`put(value)`**:  
  Insert or update an item in the cache.

- **`get(key)`**:  
  Retrieve an item from the cache using a key.

- **`store(step_index, parameter_index, global_context, step_key)`**:  
  Cache the current state of the pypeline, including step and parameter indexes and global context.

- **`load(step_key)`**:  
  Reload a cached state using a specific step key.

- **`reset(delete_directory=False)`**:  
  Reset the cache, with the option to delete the underlying cache directory.

---

## Class: AbstractCache

### Description

`AbstractCache` is an abstract base class (inheriting from `ABC`) for implementing caching mechanisms within the ETL pypeline framework. Derived classes must implement all the abstract methods below to handle caching operations. This design enforces a standardized interface and behavior across different caching strategies.

### Methods

#### `put(self, value)`
**Abstract Method.**

- **Purpose:**  
  Insert or update an item in the cache.

- **Arguments:**  
  - `value` (*Any*): The value to be cached.

---

#### `get(self, key)`
**Abstract Method.**

- **Purpose:**  
  Retrieve an item from the cache using the provided key.

- **Arguments:**  
  - `key` (*str*): The key corresponding to the cached state to retrieve.

---

#### `store(self, step_index, parameter_index, global_context, step_key)`
**Abstract Method.**

- **Purpose:**  
  Cache the current state of the pypeline. This method stores the step index, parameter index, global context, and a specific step key that marks the current execution checkpoint.

- **Arguments:**  
  - `step_index` (*OrderedDict*): An index containing all steps instantiated in the pypeline object.  
  - `parameter_index` (*dict*): The current state of the parameter index.  
  - `global_context` (*Context*): The current state of the pypeline global context.  
  - `step_key` (*str*): The step key used for caching the current state.

---

#### `load(self, step_key)`
**Abstract Method.**

- **Purpose:**  
  Reload a cached state using the provided step key.

- **Arguments:**  
  - `step_key` (*str*): The step key corresponding to the cached state to reload.

---

#### `reset(self, delete_directory=False)`
**Abstract Method.**

- **Purpose:**  
  Reset the cache to the desired state. Optionally, delete the underlying cache directory.

- **Arguments:**  
  - `delete_directory` (*bool*):  
    - `True`: Delete the cache directory on reset.  
    - `False`: Do not delete the cache directory on reset.

---

## Usage Example

Below is an example demonstrating how a concrete cache implementation might inherit from `AbstractCache` and implement its methods:

```python
from abstract_cache import AbstractCache

class MyCache(AbstractCache):
    def __init__(self):
        self.cache = {}

    def put(self, value):
        # Example implementation: Generate a key and store the value
        key = self.generate_key(value)
        self.cache[key] = value

    def get(self, key):
        # Retrieve the cached value by key
        return self.cache.get(key)

    def store(self, step_index, parameter_index, global_context, step_key):
        # Store the current state in the cache
        self.cache[step_key] = {
            'step_index': step_index,
            'parameter_index': parameter_index,
            'global_context': global_context
        }

    def load(self, step_key):
        # Load the cached state using the step key
        state = self.cache.get(step_key)
        if state:
            return state['parameter_index'], state['global_context']
        return None, None

    def reset(self, delete_directory=False):
        # Reset the cache; if delete_directory is True, delete the underlying cache directory
        self.cache.clear()
        if delete_directory:
            # Add code to delete the cache directory if necessary
            pass

    def generate_key(self, value):
        # Dummy key generation for demonstration purposes
        return str(hash(value))
```

# LFUCache Module Documentation

This module provides a concrete implementation of a cache using the Least Frequently Used (LFU) strategy. The `LFUCache` class implements the `AbstractCache` interface to store, retrieve, and manage states within the ETL pypeline framework. It supports caching of pypeline parameters and global context, along with mechanisms to evict the least frequently used items when the cache capacity is exceeded, persist cache state to disk, and restore the state from saved checkpoints.

---

## Overview

The `LFUCache` class uses the LFU strategy to manage a cache with limited capacity. When the cache is full, the least frequently used item is evicted to make room for new items. The cache state can be persisted to disk using gzip and dill and reloaded later. In addition, the cache configuration is maintained in a JSON file to track cached steps and their corresponding function hashes and source code.

---

## Class: LFUCache

### Constructor

#### `__init__(self, capacity=3, cache_dir=None, on_finish='delete')`

- **Arguments:**
  - `capacity` (*int*):  
    Maximum number of items to store in the cache.  
    *Default: 3*
  - `cache_dir` (*str*):  
    Specific directory path for the cache. If `None`, a default `.cache` directory is created in the current working directory.
  - `on_finish` (*str*):  
    Determines behavior on object deletion.  
    - `'delete'`: Deletes cache files and directory when the object is destroyed.  
    - `None`: Does nothing on destruction.

- **Behavior:**
  - Initializes internal variables such as `min_freq`, `key_to_val_freq`, and `freq_to_keys`.
  - Calls `__init_directory(cache_dir)` to set up the cache directory and configuration file.

---

### Destructor

#### `__del__(self)`

- **Behavior:**
  - If `on_finish` is set to `'delete'`, iterates over the files in the cache directory and deletes each one when the object is destroyed.

---

### Directory and Configuration Initialization

#### `__init_directory(self, cache_dir)`

- **Arguments:**
  - `cache_dir` (*str*):  
    The specified cache directory or `None` to use the default directory.
- **Returns:**
  - A tuple `(cache_directory_path, cache_config_file_path)` where:
    - `cache_directory_path` is the path to the cache directory.
    - `cache_config_file_path` is the path to the configuration JSON file.
- **Behavior:**
  - If `cache_dir` is provided, it checks for an existing JSON configuration file; otherwise, it creates a default `.cache` directory and a `config.json` file within it.
  - Uses helper functions `create_directory` and `create_file` to ensure the required paths exist.

---

### Cache Operations

#### `get(self, key)`

- **Purpose:**  
  Retrieves a value from the cache using the specified key and increments its usage frequency.
- **Arguments:**
  - `key` (*int*): The key used to retrieve the cached value.
- **Returns:**  
  - The cached value if found; otherwise, returns `(None, None)`.

---

#### `put(self, value)`

- **Purpose:**  
  Inserts a new value into the cache. If the cache is full, the least frequently used item is evicted.
- **Arguments:**
  - `value` (*Any*): The value to be inserted into the cache.
- **Behavior:**
  - If `value` is a dictionary containing `"parameter_index"` and `"globalcontext"`, it stores the tuple `(parameter_index, globalcontext)`.
  - Uses the current length of `key_to_val_freq` as a key if the key is not already present.
  - Updates frequency counts by invoking `get(key)` when a duplicate key is found.
  - Evicts the least frequently used item if the cache capacity is exceeded.

---

### Configuration Methods

#### `read_config(self)`

- **Purpose:**  
  Reads the cache configuration from the `config.json` file.
- **Returns:**  
  - A dictionary representing the cache configuration; returns an empty dictionary if the file is not found or cannot be decoded.

---

#### `write_config(self, conf)`

- **Purpose:**  
  Writes the provided configuration dictionary to the `config.json` file.
- **Arguments:**
  - `conf` (*dict*): The cache configuration to be saved.

---

#### `delete_cached_file(self, step_key)`

- **Purpose:**  
  Deletes a cached checkpoint file corresponding to the given step key.
- **Arguments:**
  - `step_key` (*str*): The key of the step whose cache file should be deleted.

---

#### `update_config(self, step_func, step_key, step_num)`

- **Purpose:**  
  Updates the cache configuration with new step information.
- **Arguments:**
  - `step_func` (*function*): The step function to be stored in the configuration.
  - `step_key` (*str*): The key for the step.
  - `step_num` (*int*): The index of the step in the pypeline.
- **Behavior:**
  - Reads the current configuration.
  - Updates the configuration with the latest completed step and step-specific function hash and source code (obtained via `get_function_hash`).
  - Rewrites the configuration to disk.

---

#### `compare_function_code(self, conf, step_key, func)`

- **Purpose:**  
  Compares the function code of a given function with the stored configuration for a specific step.
- **Arguments:**
  - `conf` (*dict*): The cache configuration.
  - `step_key` (*str*): The key of the step to compare.
  - `func` (*function*): The function to compare.
- **Returns:**  
  - `True` if the function's current hash and source code match the configuration; otherwise, `False`.

---

#### `get_cached_checkpoint(self, step_index)`

- **Purpose:**  
  Retrieves the last completed step from the cache configuration, comparing function code for consistency.
- **Arguments:**
  - `step_index` (*OrderedDict*): The current step index of the pypeline.
- **Returns:**  
  - The key of the last completed step if available; otherwise, `None`.

---

### State Persistence Methods

#### `store(self, step_index, parameter_index, global_context, step_key)`

- **Purpose:**  
  Stores the current cache state to a checkpoint file.
- **Arguments:**
  - `step_index` (*OrderedDict*): The pypeline's step index.
  - `parameter_index` (*dict*): The current parameter index.
  - `global_context` (*dict*): The current global context.
  - `step_key` (*str*): The step key for which to store the checkpoint.
- **Behavior:**
  - Updates the configuration using `update_config`.
  - Serializes the cache state along with the provided parameters using `dill` and writes it to a gzip-compressed file named `{step_key}.pkl.gz`.

---

#### `load(self, step_key)`

- **Purpose:**  
  Loads the cached state from a checkpoint file.
- **Arguments:**
  - `step_key` (*str*): The step key of the checkpoint to load.
- **Returns:**  
  - A tuple `(parameter_index, global_context)` representing the cached state.
- **Behavior:**
  - Reads the checkpoint file, updates internal cache state (e.g., capacity, min frequency, key mappings), and returns the cached parameters and global context.

---

#### `reset(self, delete_directory=False)`

- **Purpose:**  
  Resets the cache state.
- **Arguments:**
  - `delete_directory` (*bool*):  
    - `False` (default): Clears the cache state without deleting the cache directory.
    - `True`: Deletes all files in the cache directory.
- **Behavior:**
  - Resets internal data structures (`min_freq`, `key_to_val_freq`, `freq_to_keys`).
  - Optionally deletes cache files from the cache directory.

---

## Usage Example

Below is an example demonstrating how to use the `LFUCache` class within the pypeline framework:

```python
from lfu_cache import LFUCache

# Initialize the LFUCache with a capacity of 3 items.
cache = LFUCache(capacity=3)

# Example of putting a value into the cache.
cache.put({"parameter_index": {"param": 42}, "globalcontext": {"df": "dataframe_placeholder"}})

# Retrieve a cached value using its key.
value = cache.get(0)
print("Cached value:", value)

# Store a checkpoint with dummy step index, parameter index, and global context.
dummy_step_index = {"step1": "dummy_step_object"}
dummy_parameter_index = {"param": 42}
dummy_global_context = {"df": "dataframe_placeholder"}
cache.store(dummy_step_index, dummy_parameter_index, dummy_global_context, "step1")

# Load the checkpoint back.
param_index, global_context = cache.load("step1")
print("Loaded Parameter Index:", param_index)
print("Loaded Global Context:", global_context)

# Reset the cache (optionally, delete cache directory).
cache.reset(delete_directory=True)