"""
Module: cache

Defines the ``AbstractCache`` class, an abstract base class that specifies the interface
required for caching mechanisms within the ``Seroflow`` ``Pipeline`` Object. Concrete implementations
must inherit from ``AbstractCache`` and implement the methods defined below, ensuring
consistent behavior across different caching strategies.
"""

from abc import ABC, abstractmethod


class AbstractCache(ABC):
    """Abstract base class for creating a cache mechanism in the ``Seroflow`` ``Pipeline``.
    """

    @abstractmethod
    def put(self, value):
        """Inserts or updates an item in the cache.
        This method should be implemented to handle the insertion of
        a value into the cache during ``Seroflow's`` ``Pipeline`` execution.
        This method is used with the ``CacheState`` transformation which creates a ``Step`` object.
        The ``CacheState`` object is then subsequently used in the ``cache_state()`` method in the ``Pipeline`` Object.
        This allows the state of the ``Pipeline`` to be cached and restored later within ``Pipeline`` execution.

        Args:
            value (Any): The value to be cached.
        """
        pass

    @abstractmethod
    def get(self, key):
        """Retrieves an item from the cache using the provided key.
        This method should be implemented to handle the retrieval of
        a cached value based on its key during ``Seroflow's`` ``Pipeline`` execution.
        This method is used with the ``ReloadCacheState`` transformation which creates a ``Step`` object.
        The ``ReloadCacheState`` object is then subsequently used in the ``reload_cached_state()`` method in the ``Pipeline`` Object.
        This allows a cached state to be restored within ``Pipeline`` execution.

        Args:
            key (str): The key identifying the cached item.

        Returns:
            Any: The cached value associated with the key, or None if not found.
        """
        pass

    @abstractmethod
    def store(self, step_index, parameter_index, global_context, step_key):
        """Caches the current state of the Pipeline.
        This method should be implemented to handle the storage of
        the current state of the Pipeline, including the parameter index
        and global context, using the provided step key.
        Unlike the ``put()`` method, this method is used to store the state of the
        ``Pipeline`` during global development.
        This means that the state of the ``Pipeline`` is stored in a cache directory
        after each successful ``Step`` in the ``Pipeline`` execution.
        Cached States should be non-volatile.
        This method is used in the ``__store_in_cache()`` method in the ``Pipeline`` Object.

        Args: 
            step_index (OrderedDict): Index of all instantiated steps in the Pipeline.
            parameter_index (dict): The current state of the parameter index.
            global_context (Context): The current global context of the Pipeline.
            step_key (str): The key identifying the step whose state is being cached.
        """
        pass

    @abstractmethod
    def load(self, step_key):
        """Reloads a cached state using the specified step key.
        This method should be implemented to handle the retrieval of
        a cached state based on the step key.
        Unlike the ``get()`` method, this method is used to load the state of the
        ``Pipeline`` during global development.
        This means that the state of the ``Pipeline`` is loaded from a cache directory
        whenever the ``Pipeline`` is initially executed, to essentially 'resume' from the last completed ``Step``.
        This method is used in the ``__load_from_cache()`` method in the ``Pipeline`` Object.

        Args:
            step_key (str): The key identifying the cached state to reload.

        Returns:
            tuple: A tuple containing the parameter index and global context.
        """
        pass

    @abstractmethod
    def reset(self, delete_directory=False):
        """Resets the cache to its initial state.
        This method should be implemented to handle the clearing of
        all cached data, including the cache directory if specified.
        ``reset()`` can be used either in global development or in ``Pipeline`` execution.
        This method is used with the ``ResetCache`` transformation which creates a ``Step`` object.
        The ``ResetCache`` object is then subsequently used in the ``reset_cache()`` method in the ``Pipeline`` Object.
        This allows a cached state to be restored within ``Pipeline`` execution.
        For global development, the ``ResetCache`` object is simply appended as the last step in the ``Pipeline``.

        Args:
            delete_directory (bool, optional): If True, deletes the cache directory.
                Defaults to False.
        """
        pass