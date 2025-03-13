"""
This module provides transformation classes for managing cache operations in an ETL pipeline.

It defines three transformation steps:
    - cache_state: Caches the current pipeline state into a cache.
    - reload_cached_state: Reloads the cached state from the cache and updates the pipeline.
    - reset_cache: Resets the cache and optionally deletes the cache directory.

Each class is a subclass of the abstract transformation class and implements the required
transformation function.
"""

from copy import deepcopy
from .transformation import Transformation

class CacheState(Transformation):
    """
    A transformation step that caches the current state of the pipeline.

    This step deep-copies the pipeline's parameter index and global context and stores
    them in the cache.

    Attributes:
        cache: The cache object where the state will be stored.
        parameter_index: The current parameter index of the pipeline.
        globalcontext: The global context of the pipeline.
    """

    def __init__(self, cache, parameter_index, globalcontext, step_name="cache_state"):
        """
        Initialize a new cache_state instance.

        Args:
            cache: The cache object used to store the state.
            parameter_index: The current parameter index of the pipeline.
            globalcontext: The global context of the pipeline.
            step_name (str, optional): The name of the step. Defaults to "cache_state".
        """
        super().__init__(step_name=step_name, func=self.func)
        self.cache = cache
        self.parameter_index = parameter_index
        self.globalcontext = globalcontext

    def start_step(self):
        """
        Start the cache_state step.

        This method is a placeholder and does not perform any action.

        Returns:
            None
        """
        return

    def stop_step(self):
        """
        Stop the cache_state step.

        This method is a placeholder and does not perform any additional cleanup.

        Returns:
            None
        """
        return

    def func(self):
        """
        Execute the cache_state transformation.

        Deep copies the current parameter index and global context, packages them into a dictionary,
        and stores the dictionary in the cache.

        Returns:
            None
        """
        data = {
            "parameter_index": deepcopy(self.parameter_index),
            "globalcontext": deepcopy(self.globalcontext)
        }
        self.cache.put(data)

    def __str__(self):
        """
        Return a string representation of the cache_state instance.

        Returns:
            str: The string representation of the cache object.
        """
        return f"{self.cache}"


class ReloadCacheState(Transformation):
    """
    A transformation step that reloads the cached pipeline state.

    This step retrieves the cached state using a cache key and updates the pipeline's
    parameter index and global context accordingly.

    Attributes:
        cache_key: The key used to retrieve the cached state.
        cache: The cache object from which to load the state.
        pypeline: The pipeline instance that will be updated with the cached state.
    """

    def __init__(self, cache_key, cache, pypeline, step_name="reload_cached_state"):
        """
        Initialize a new reload_cached_state instance.

        Args:
            cache_key: The key corresponding to the cached state.
            cache: The cache object from which the state is retrieved.
            pypeline: The pipeline instance to be updated.
            step_name (str, optional): The name of the step. Defaults to "reload_cached_state".
        """
        super().__init__(step_name=step_name, func=self.func)
        self.cache_key = cache_key
        self.cache = cache
        self.pypeline = pypeline

    def start_step(self):
        """
        Start the reload_cached_state step.

        This method is a placeholder and does not perform any action.

        Returns:
            None
        """
        return

    def stop_step(self):
        """
        Stop the reload_cached_state step.

        This method is a placeholder and does not perform any additional cleanup.

        Returns:
            None
        """
        return

    def func(self):
        """
        Execute the reload_cached_state transformation.

        Retrieves the cached state using the cache key and updates the pipeline's
        parameter index and global context with the retrieved state.

        Returns:
            None
        """
        parameter_index, globalcontext = self.cache.get(self.cache_key)
        self.pypeline.parameter_index = parameter_index
        self.pypeline.globalcontext = globalcontext

    def __str__(self):
        """
        Return a string representation of the reload_cached_state instance.

        Returns:
            str: The string representation of the cache object.
        """
        return f"{self.cache}"


class ResetCache(Transformation):
    """
    A transformation step that resets the cache.

    This step resets the cache and, optionally, deletes the cache directory based on the
    provided configuration.

    Attributes:
        cache: The cache object to be reset.
        delete_directory (bool): Indicates whether to delete the cache directory.
    """

    def __init__(self, cache, step_name="reset_cache", delete_directory=False):
        """
        Initialize a new reset_cache instance.

        Args:
            cache: The cache object to be reset.
            step_name (str, optional): The name of the step. Defaults to "reset_cache".
            delete_directory (bool, optional): If True, the cache directory will be deleted.
                                               Defaults to False.
        """
        super().__init__(step_name=step_name, func=self.func)
        self.cache = cache
        self.delete_directory = delete_directory

    def start_step(self):
        """
        Start the reset_cache step.

        This method is a placeholder and does not perform any action.

        Returns:
            None
        """
        return

    def stop_step(self):
        """
        Stop the reset_cache step.

        This method is a placeholder and does not perform any additional cleanup.

        Returns:
            None
        """
        return

    def func(self):
        """
        Execute the reset_cache transformation.

        Resets the cache. If delete_directory is True, the cache directory is also deleted.

        Returns:
            None
        """
        self.cache.reset(delete_directory=self.delete_directory)

    def __str__(self):
        """
        Return a string representation of the reset_cache instance.

        Returns:
            str: A string representation of the reset_cache step.
        """
        return f"{self.cache}"
