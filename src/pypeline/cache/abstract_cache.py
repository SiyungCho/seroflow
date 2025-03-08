"""Module that defines an abstract caching interface using the AbstractCache class.

This module provides an abstract base class for caching mechanisms. The
AbstractCache class outlines the necessary methods that concrete caching
implementations should provide.
"""

from abc import ABC, abstractmethod

class AbstractCache(ABC):
    """Abstract base class for caching mechanisms.

    This class defines the required methods for any caching implementation.
    Concrete implementations must override the abstract methods to provide 
    functionality for adding, retrieving, storing, loading, and resetting the cache.
    """

    @abstractmethod
    def put(self, value):
        """Insert an item into the cache.

        Implementations should provide the logic to add an item to the cache.
        """

    @abstractmethod
    def get(self, key):
        """Retrieve an item from the cache.

        Implementations should provide the logic to retrieve an item from the cache.
        """

    @abstractmethod
    def store(self, step_index, parameter_index, global_context, step_key):
        """Store the current state of the cache.

        Implementations should provide the logic to persist the cache state.
        """

    @abstractmethod
    def load(self, step_key):
        """Load a previously stored cache state.

        Implementations should provide the logic to restore the cache state.
        """

    @abstractmethod
    def reset(self, delete_directory=False):
        """Reset the cache to its initial state.

        Implementations should clear all items from the cache and restore any default settings.
        """
