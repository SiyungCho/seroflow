"""
This module implements transformation steps related to caching operations.
It provides three transformation classes that interact with a caching mechanism to store, reload, or reset states within the ``Pipeline`` Object.
These transformations allow the execution to branch and resume from a saved state, or clear cached data as needed.
It is important that custom caches are designed with these principles and classes in mind.
The available transformations include:

- **CacheState**: Caches the current state of execution (i.e., parameter index and global context) by storing a deep copy in the cache.
- **ReloadCacheState**: Reloads a cached state from the cache using a specified cache key and updates the ``Pipeline's`` parameter index and global context.
- **ResetCache**: Resets the cache by clearing all cached data, with an option to delete the underlying cache directory.

"""

from copy import deepcopy
from .transformation import Transformation

class CacheState(Transformation):
    """
    This transformation caches the current state of ``Pipeline`` execution by storing deep copies
    of the parameter index and global context in the provided cache. 
    It is typically used to create a checkpoint in the ``Pipeline``, allowing execution to resume
    from this point later if necessary.

    Attributes:
        cache: The cache object where the state is stored.
        parameter_index (dict): The current parameter index of the ``Pipeline``.
        globalcontext: The current global context of the ``Pipeline``.
    """
    def __init__(self,
                 cache,
                 parameter_index,
                 globalcontext,
                 step_name="cache_state",
                 on_error=None):
        """
        Initializes the ``CacheState`` transformation.

        Arguments:
            cache: The cache object used for storing the ``Pipeline`` state.
            parameter_index (dict): The parameter index to be cached.
            globalcontext: The global context (containing dataframes) to be cached.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "cache_state".
            on_error (str, optional): The error handling strategy.
        """
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.cache = cache
        self.parameter_index = parameter_index
        self.globalcontext = globalcontext

    def start_step(self):
        """
        Prepares the ``CacheState`` transformation for execution.
        This implementation does not require any pre-execution steps.
        """
        return

    def stop_step(self):
        """
        Cleans up after executing the ``CacheState`` transformation.
        No cleanup is required for this transformation.
        """
        return

    def func(self):
        """
        Executes the ``CacheState`` transformation.
        Creates deep copies of the current parameter index and global context, and stores them
        in the cache using the cache's ``put()`` method.
        """
        data = {
            "parameter_index": deepcopy(self.parameter_index),
            "globalcontext": deepcopy(self.globalcontext)
        }
        self.cache.put(data)

    def __str__(self):
        """
        Returns a string representation of the cache used by this transformation.

        Returns:
            str: A string representation of the cache object.
        """
        return f"{self.cache}"


class ReloadCacheState(Transformation):
    """
    This transformation reloads a previously cached state from the cache using a specified
    cache key. The reloaded state (parameter index and global context) is then applied to
    the ``Pipeline``, allowing execution to resume from a saved checkpoint.
    """
    def __init__(self,
                 cache_key,
                 cache,
                 pipeline,
                 step_name="reload_cached_state",
                 on_error=None):
        """
        Initializes the ``ReloadCacheState`` transformation.

        Arguments:
            cache_key: The key corresponding to the cached state to reload.
            cache: The cache object from which the state is retrieved.
            pipeline: The ``Pipeline`` object whose state will be updated.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "reload_cached_state".
            on_error (str, optional): The error handling strategy.
        """
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.cache_key = cache_key
        self.cache = cache
        self.pipeline = pipeline

    def start_step(self):
        """
        Prepares the ``ReloadCacheState`` transformation for execution.
        No pre-execution steps are required.
        """
        return

    def stop_step(self):
        """
        Cleans up after executing the ``ReloadCacheState`` transformation.
        No cleanup is required.
        """
        return

    def func(self):
        """
        Executes the ``ReloadCacheState`` transformation.
        Retrieves the cached state using the cache key and updates the ``Pipeline's``
        parameter index and global context accordingly.
        """
        parameter_index, globalcontext = self.cache.get(self.cache_key)
        self.pipeline.parameter_index = parameter_index
        self.pipeline.globalcontext = globalcontext

    def __str__(self):
        """
        Returns a string representation of the cache used by this transformation.

        Returns:
            str: A string representation of the cache object.
        """
        return f"{self.cache}"


class ResetCache(Transformation):
    """
    This transformation resets the cache by clearing all cached state. It can optionally
    delete the underlying cache directory, ensuring that all cached data is removed.
    """
    def __init__(self,
                 cache,
                 step_name="reset_cache",
                 delete_directory=False,
                 on_error=None):
        """
        Initializes the ``ResetCache`` transformation.

        Arguments:
            cache: The cache object to be reset.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "reset_cache".
            delete_directory (bool, optional): If True, deletes the cache directory.
                                       Defaults to False.
            on_error (str, optional): The error handling strategy.
        """
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.cache = cache
        self.delete_directory = delete_directory

    def start_step(self):
        """
        Prepares the ``ResetCache`` transformation for execution.
        No pre-execution initialization is needed.
        """
        return

    def stop_step(self):
        """
        Cleans up after executing the ``ResetCache`` transformation.
        No cleanup is required for this transformation.
        """
        return

    def func(self):
        """
        Executes the ``ResetCache`` transformation.
        Calls the ``reset()`` method on the cache object,
        optionally deleting the cache directory if specified.
        """
        self.cache.reset(delete_directory=self.delete_directory)

    def __str__(self):
        """
        Returns a string representation of the cache used by this transformation.

        Returns:
            str: A string representation of the cache object.
        """
        return f"{self.cache}"
