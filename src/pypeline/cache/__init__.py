"""
Module: cache

This module implements caching functionalities. It provides an abstract caching 
interface and a concrete implementation using the Least Frequently Used (LFU) strategy. 
These caching mechanisms allow for efficient storage and retrieval of 
global or intermediate pipeline states, facilitating execution resumption and branching.
Any custom caching implementation should derive from the AbstractCache class.

Key Components:
    - AbstractCache: An abstract base class that defines the interface and required methods for caching implementations.
    - LFUCache: A concrete caching implementation that employs the LFU algorithm to manage and evict cache entries 
      based on usage frequency.
"""
from .abstract_cache import AbstractCache
from .lfu_cache import LFUCache
