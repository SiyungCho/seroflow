"""
Module: cache

Defines the AbstractCache class, an abstract base class that specifies the interface
required for caching mechanisms within the Pipeline framework. Concrete implementations
must inherit from AbstractCache and implement the methods defined below, ensuring
consistent behavior across different caching strategies.
"""

from abc import ABC, abstractmethod


class AbstractCache(ABC):
    """Abstract base class for caching mechanisms in the Pipeline framework.

    Concrete subclasses must implement methods for inserting, retrieving,
    storing, loading, and resetting cache items.
    """

    @abstractmethod
    def put(self, value):
        """Inserts or updates an item in the cache.

        Args:
            value (Any): The value to be cached.
        """
        pass

    @abstractmethod
    def get(self, key):
        """Retrieves an item from the cache using the provided key.

        Args:
            key (str): The key identifying the cached item.

        Returns:
            Any: The cached value associated with the key, or None if not found.
        """
        pass

    @abstractmethod
    def store(self, step_index, parameter_index, global_context, step_key):
        """Caches the current state of the Pipeline.

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

        Args:
            step_key (str): The key identifying the cached state to reload.

        Returns:
            tuple: A tuple containing the parameter index and global context.
        """
        pass

    @abstractmethod
    def reset(self, delete_directory=False):
        """Resets the cache to its initial state.

        Args:
            delete_directory (bool, optional): If True, deletes the cache directory.
                Defaults to False.
        """
        pass