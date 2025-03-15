"""
"""

from copy import deepcopy
from .transformation import Transformation

class CacheState(Transformation):
    """
    """

    def __init__(self, cache, parameter_index, globalcontext, step_name="cache_state", on_error=None):
        """
        """
        super().__init__(step_name=step_name, func=self.func, on_error=on_error)
        self.cache = cache
        self.parameter_index = parameter_index
        self.globalcontext = globalcontext

    def start_step(self):
        """
        """
        return

    def stop_step(self):
        """
        """
        return

    def func(self):
        """
        """
        data = {
            "parameter_index": deepcopy(self.parameter_index),
            "globalcontext": deepcopy(self.globalcontext)
        }
        self.cache.put(data)

    def __str__(self):
        """
        """
        return f"{self.cache}"


class ReloadCacheState(Transformation):
    """
    """

    def __init__(self, cache_key, cache, pypeline, step_name="reload_cached_state", on_error=None):
        """
        """
        super().__init__(step_name=step_name, func=self.func, on_error=on_error)
        self.cache_key = cache_key
        self.cache = cache
        self.pypeline = pypeline

    def start_step(self):
        """
        """
        return

    def stop_step(self):
        """
        """
        return

    def func(self):
        """
        """
        parameter_index, globalcontext = self.cache.get(self.cache_key)
        self.pypeline.parameter_index = parameter_index
        self.pypeline.globalcontext = globalcontext

    def __str__(self):
        """
        """
        return f"{self.cache}"


class ResetCache(Transformation):
    """
    """

    def __init__(self, cache, step_name="reset_cache", delete_directory=False, on_error=None):
        """
        """
        super().__init__(step_name=step_name, func=self.func, on_error=on_error)
        self.cache = cache
        self.delete_directory = delete_directory

    def start_step(self):
        """
        """
        return

    def stop_step(self):
        """
        """
        return

    def func(self):
        """
        """
        self.cache.reset(delete_directory=self.delete_directory)

    def __str__(self):
        """
        """
        return f"{self.cache}"
