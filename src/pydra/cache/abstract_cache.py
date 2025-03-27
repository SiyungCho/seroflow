"""
Module: abstract_cache

This module defines the AbstractCache class, an abstract base class that specifies the
required interface for caching mechanisms used within the Pipeline framework.
Any concrete cache implementation must inherit from AbstractCache and implement the
methods for inserting, retrieving, storing, loading, and resetting cache items.
This ensures consistent cache behavior across different caching strategies.
"""

from abc import ABC, abstractmethod

class AbstractCache(ABC):
    """
    AbstractCache

    An abstract base class for implementing caching mechanisms within the Pipeline framework.
    Derived classes must implement the following methods to handle caching operations:
      - put: Insert or update an item in the cache.
      - get: Retrieve an item from the cache using a key.
      - store: Cache the current state of the Pipeline.
      - load: Reload a cached state using a specific step key.
      - reset: Reset the cache, with the option to delete the underlying cache directory.
    """

    @abstractmethod
    def put(self, value):
        """
        Abstract Method: put()
        Ensures inherited class instantiates a put method.
        Used to Cache items in Execution.
        Put method inserts/updates a cached item.

        Arguments:
            value (Any):
                Value to cache.
        """

    @abstractmethod
    def get(self, key):
        """
        Abstract Method: get()
        Ensures inherited class instantiates a get method.
        Used to retrieve items in Execution.
        Get method retrieves a cached item using the corresponding key.

        Arguments:
            key (string):
                Key for cached state to retrieve.
        """

    @abstractmethod
    def store(self, step_index, parameter_index, global_context, step_key):
        """
        Abstract Method: store()
        Ensures inherited class instantiates a store method.
        Store method caches the current state including any properties or items desired.

        Arguments:
            step_index (OrderedDict):
                Index containing all steps instantiated in Pipeline object.
            parameter_index (dict):
                Current state of parameter index.
            global_context (Context):
                Current state of Pipeline global context.
            step_key (string):
                Step Key for step to cache.
        """

    @abstractmethod
    def load(self, step_key):
        """
        Abstract Method: load()
        Ensures inherited class instantiates a load method.
        Load method reloades a cached state using the provided step key.

        Arguments:
            step_key (string):
                Step Key for cached state to reload.
        """

    @abstractmethod
    def reset(self, delete_directory=False):
        """
        Abstract Method: reset()
        Ensures inherited class instantiates a reset method.
        Used to reset cache to desired state.

        Arguments:
            delete_directory (Bool):
                True: .cache directory is deleted on reset
                False: .cache directory is not deleted on reset
        """
