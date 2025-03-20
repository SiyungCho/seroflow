# Cache Transformations Documentation

This module implements transformation steps related to caching operations. It provides three transformation classes that interact with a caching mechanism to store, reload, or reset states within the Pypeline Object. These transformations allow the execution to branch and resume from a saved state, or clear cached data as needed. It is important that custom caches are designed with these principles and classes in mind.

- **CacheState**:  
  Caches the current state of execution (i.e., the parameter index and global context or anything the caching states) by storing deep copies in the cache. This transformation is typically used to create a checkpoint, allowing execution to resume from that point later.
- **ReloadCacheState**:  
  Reloads a previously cached state from the cache using a specified cache key and updates the pypeline state. This transformation enables execution to resume from a saved checkpoint.
- **ResetCache**:  
  Resets the cache by clearing all cached state. It also provides an option to delete the underlying cache directory, ensuring that all cached data is removed.

## Cache Transformation Classes

### CacheState

- **Purpose**:  
  - The `CacheState` transformation caches the current state of the pypeline execution. It creates deep copies of the parameter index and global context and stores them in the provided cache using the cache's `put()` method.

- **Parameters**:
  - `cache` (Cache Object): 
    - The cache object used for storing the pypeline state.
  - `parameter_index` (dict): 
    - The parameter index to be cached.
  - `globalcontext` (Context Object): 
    - The global context (containing DataFrames) to be cached.
  - `step_name` (str, optional): 
    - The name of this transformation step. 
    - Defaults to `"cache_state"`.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `CacheState` without terminating the `Pypeline` execution.

**Key Methods**:
- `func()`:  
  Creates deep copies of the current parameter index and global context and stores them in the cache. Calls the cache's `put()` method to perform this action.

- `start_step()`:  
  Prepares the transformation for execution (no pre-execution action required).

- `stop_step()`:  
  Cleans up after execution (no cleanup is required).

**Note**: The `CacheState` Object is instantiated inside a method within the `Pypeline` Object. It is performed when the method `pypeline.cache_state()` is called. Any custom Caches' created must handle this appropriately by creating a compatible `put()` method.

### ReloadCacheState

**Description**:  
The `ReloadCacheState` transformation reloads a cached state from the cache using a specified cache key. It then updates the pypeline's parameter index and global context with the retrieved state, enabling execution to resume from a saved checkpoint. It uses the cache's `get()` method to perform this action.

**Constructor Arguments**:
- `cache_key` (int, Any type cache uses): 
  - The key corresponding to the cached state to reload.
- `cache` (Cache Object): 
  - The cache object from which the state is retrieved.
- `pypeline` (Pypeline Object): 
  - The pypeline object whose state (parameter index and global context) will be updated.
- `step_name` (str, optional): 
  - The name of this transformation step. 
  - Defaults to `"reload_cached_state"`.
- `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ReloadCacheState` without terminating the `Pypeline` execution.

**Key Methods**:
- `func()`:  
  Retrieves the cached state using the cache key and updates the pypeline's parameter index and global context. Calls the cache's `get()` method to perform this action.

- `start_step()`:  
  Prepares the transformation for execution (no pre-execution action required).

- `stop_step()`:  
  Cleans up after execution (no cleanup is required).

**Note**: The `ReloadCacheState` Object is instantiated inside a method within the `Pypeline` Object. It is performed when the method `pypeline.reload_cached_state()` is called. Any custom Caches' created must handle this appropriately by creating a compatible `get()` method.

### ResetCache

**Description**:  
The `ResetCache` transformation resets the cache by clearing all cached state. It optionally deletes the underlying cache directory if specified, ensuring that all cached data is removed. It uses the cache's `reset()` method to perform this action.

**Constructor Arguments**:
- `cache` (Cache Object): 
  - The cache object to reset
- `step_name` (str, optional): 
  - The name of this transformation step. 
  - Defaults to `"reset_cache"`.
- `delete_directory` (bool, optional):  
  - If `True`, deletes the cache directory when the transformation is executed.
  - Defaults to `False`.
- `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ResetCache` without terminating the `Pypeline` execution.

**Key Methods**:
- `func()`:  
  Executes the cache reset by calling the cache object's `reset()` method with the appropriate flag for deleting the directory.

- `start_step()`:  
  Prepares the transformation for execution (no pre-execution action required).

- `stop_step()`:  
  Cleans up after execution (no cleanup is required).

**Note**: The `ResetCache` Object is instantiated inside a method within the `Pypeline` Object. It is performed when the method `pypeline.reset_cache()` is called. Any custom Caches' created must handle this appropriately by creating a compatible `reset()` method.