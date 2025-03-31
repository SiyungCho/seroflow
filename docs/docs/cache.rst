Cache
======================

The modules documented here define the interface and a concrete implementation for caching with the ``Seroflow`` ``Pipeline`` Object.
We provide a common interface to inserting, retrieving, storing, loading, and resetting cache items. 
This ensures consistent cache behavior across different caching strategies.

Overview
-----------------------------------

This documentation covers two modules:

- **abstract_cache**: Defines the ``AbstractCache`` abstract class, which specifies the interface for creating custom caches.

- **lfu_cache**: The Least Frequently Used (LFU), ``LFUCache`` class implements the ``AbstractCache`` interface to store, retrieve, and manage states within the ``Pipeline`` execution.
It supports caching of ``Pipeline`` parameters and global context, along with mechanisms to evict the least frequently used items when the cache capacity is exceeded, persist cache state to disk, and restore the state from saved checkpoints.

AbstractCache
---------------------------

``AbstractCache`` is an abstract base class (inheriting from ``ABC``) for implementing caching.
Derived classes must implement all the abstract methods below to handle caching operations.
This design enforces a standardized interface and behavior across different caching strategies.

**Note**: It is important to consider how a custom cache will interact with the internal systems in the ``Seroflow`` ``Pipeline`` Object.
Please Review the [Cache Transformations](transformations/cache.md) documentation for further information on ``CacheState``, ``ReloadCacheState`` and ``ResetCache``.

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

The ``LFUCache`` class uses the Least Frequently Used (LFU) strategy to manage a cache with limited capacity.
When the cache is full, the least frequently used item is evicted to make room for new items.
The cache state can be persisted to disk using gzip and dill and reloaded later.
In addition, the cache configuration is maintained in a ``JSON`` file to track cached steps and their corresponding function hashes and source code.

.. autoclass:: seroflow.cache.lfu_cache.LFUCache
   :members:
   :show-inheritance:
   :undoc-members:

  
Initialization Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``LFUCache``: ::

  from seroflow import Pipeline
  from seroflow.cache import LFUCache # Import LFUCache

  # Initialize a pipeline with caching 
  pipeline = Pipeline(cache=LFUCache)
