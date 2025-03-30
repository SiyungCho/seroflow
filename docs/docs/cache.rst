Cache
======================

The modules documented here define the base structure and a concrete implementation for ``Pipeline`` caching.
They provide a common interface to inserting, retrieving, storing, loading, and resetting cache items.
This ensures consistent cache behavior across different caching strategies.

Overview
-----------------------------------
This documentation covers two modules:

- **abstract_cache**:  
  Defines the ``AbstractCache`` abstract class, which specifies the interface for creating caches.

- **lfu_cache**:  
  The Least Frequently Used (LFU), ``LFUCache`` class implements the ``AbstractCache`` interface to store, retrieve, and manage states within the ``Pipeline`` execution.
  It supports caching of ``Pipeline`` parameters and global context, along with mechanisms to evict the least frequently used items when the cache capacity is exceeded, persist cache state to disk, and restore the state from saved checkpoints.

Cache
---------------------------

``AbstractCache`` is an abstract base class (inheriting from ``ABC``) for implementing caching mechanisms within the ``Pipeline`` framework.
Derived classes must implement all the abstract methods below to handle caching operations.
This design enforces a standardized interface and behavior across different caching strategies.

**Note**: It is important to consider how a custom cache will interact with the internal systems in the ``Pipeline`` Object.
Please Review the [Cache Transformations](transformations/cache.md) documentation for further information on ``CacheState``, ``ReloadCacheState`` and ``ResetCache``.

**Subclasses must override:**

- ``put(self, value)``
- ``get(self, key)``
- ``store(self, step_index, parameter_index, global_context, step_key)``
- ``load(self, step_key)``
- ``reset(self, delete_directory=False)``

.. autoclass:: seroflow.cache.cache.AbstractCache
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^
Below is an example demonstrating how a concrete cache implementation might inherit from ``AbstractCache`` and implement its methods: ::

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

LFUCache
--------------------------------

.. autoclass:: seroflow.cache.lfu_cache.LFUCache
   :members:
   :show-inheritance:
   :undoc-members:
