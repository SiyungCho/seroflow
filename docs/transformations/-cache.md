# Cache Transformations Documentation

This module implements transformation steps related to caching operations in the ETL pypeline framework. It provides three transformation classes that interact with a caching mechanism to store, reload, or reset states. These transformations allow the execution to branch and resume from a saved state, or clear cached data as needed.

- **CacheState**:  
  Caches the current state of execution (i.e., the parameter index and global context) by storing deep copies in the cache. This transformation is typically used to create a checkpoint, allowing execution to resume from that point later.
- **ReloadCacheState**:  
  Reloads a previously cached state from the cache using a specified cache key and updates the pypeline's parameter index and global context. This transformation enables execution to resume from a saved checkpoint.
- **ResetCache**:  
  Resets the cache by clearing all cached state. It also provides an option to delete the underlying cache directory, ensuring that all cached data is removed.

## Cache Transformation Classes

### CacheState

- **Purpose**:  
  - The `CacheState` transformation caches the current state of the pypeline execution. It creates deep copies of the parameter index and global context and stores them in the provided cache using the cache's `put()` method.

- **Parameters**:
  - `cache`: The cache object used for storing the pypeline state.
  - `parameter_index` (dict): The parameter index to be cached.
  - `globalcontext`: The global context (containing DataFrames) to be cached.
  - `step_name` (str, optional): The name of this transformation step. Defaults to `"cache_state"`.
  - `on_error` (str, optional): The error handling strategy.

**Key Methods**:
- `func()`:  
  Creates deep copies of the current parameter index and global context and stores them in the cache.

- `start_step()`:  
  Prepares the transformation for execution (no pre-execution action required).

- `stop_step()`:  
  Cleans up after execution (no cleanup is required).

- `__str__()`:  
  Returns a string representation of the cache used by this transformation.

## CacheState Example

Below is an example demonstrating how to use the Cache Transformation `CacheState`:

```python
```

---

### ReloadCacheState

**Description**:  
The `ReloadCacheState` transformation reloads a cached state from the cache using a specified cache key. It then updates the pypeline's parameter index and global context with the retrieved state, enabling execution to resume from a saved checkpoint.

**Constructor Arguments**:
- `cache_key`: The key corresponding to the cached state to reload.
- `cache`: The cache object from which the state is retrieved.
- `pypeline`: The pypeline object whose state (parameter index and global context) will be updated.
- `step_name` (str, optional): The name of this transformation step. Defaults to `"reload_cached_state"`.
- `on_error` (str, optional): The error handling strategy.

**Key Methods**:
- `func()`:  
  Retrieves the cached state using the cache key and updates the pypeline's parameter index and global context.

- `start_step()`:  
  Prepares the transformation for execution (no pre-execution action required).

- `stop_step()`:  
  Cleans up after execution (no cleanup is required).

- `__str__()`:  
  Returns a string representation of the cache used by this transformation.

---

### ResetCache

**Description**:  
The `ResetCache` transformation resets the cache by clearing all cached state. It optionally deletes the underlying cache directory if specified, ensuring that all cached data is removed.

**Constructor Arguments**:
- `cache`: The cache object to be reset.
- `step_name` (str, optional): The name of this transformation step. Defaults to `"reset_cache"`.
- `delete_directory` (bool, optional):  
  - If `True`, deletes the cache directory when the transformation is executed.
  - Defaults to `False`.
- `on_error` (str, optional): The error handling strategy.

**Key Methods**:
- `func()`:  
  Executes the cache reset by calling the cache object's `reset()` method with the appropriate flag for deleting the directory.

- `start_step()`:  
  Prepares the transformation for execution (no pre-execution action required).

- `stop_step()`:  
  Cleans up after execution (no cleanup is required).

- `__str__()`:  
  Returns a string representation of the cache used by this transformation.

---

## Usage Example

Below is an example demonstrating how these cache transformations might be used in a pypeline:

```python
from cache import CacheState, ReloadCacheState, ResetCache
from my_cache_implementation import MyCache  # Assume MyCache implements AbstractCache
from pypeline import Pypeline

# Initialize a cache object (MyCache should be a concrete implementation of AbstractCache)
cache = MyCache(capacity=5)

# Assume we have a pypeline object with current state
pypeline = Pypeline(cache=cache, logger=True, mode="DEV")
parameter_index = {"param1": 123}
global_context = {"df": "dataframe_placeholder"}

# Create a CacheState transformation to save the current state
cache_state_transform = CacheState(cache, parameter_index, global_context)
cache_state_transform.func()  # This stores a checkpoint in the cache

# Later, to reload the state:
reload_transform = ReloadCacheState(cache_key=0, cache=cache, pypeline=pypeline)
reload_transform.func()  # This updates the pypeline's parameter index and global context

# To reset the cache:
reset_transform = ResetCache(cache, delete_directory=True)
reset_transform.func()  # This clears all cached data and deletes the cache directory