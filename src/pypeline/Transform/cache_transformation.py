from ..Utils.utils import *
from ..Transform.Transformation import transformation
from ..Wrappers.wrappers import log_error
from copy import deepcopy

class cache_state(transformation):
    def __init__(self, cache, parameter_index, globalcontext, step_name="cache_state"):
        super().__init__(step_name=step_name, func=self.func)
        self.cache = cache
        self.parameter_index = parameter_index
        self.globalcontext = globalcontext

    def start_step(self):
        return

    def stop_step(self):
        return

    def func(self):
        data = {
            "parameter_index": deepcopy(self.parameter_index),
            "globalcontext": deepcopy(self.globalcontext)
        }
        self.cache.put(data)
        return

    def __str__(self):
        return f"""{self.cache}"""
    
class reload_cached_state(transformation):
    def __init__(self, cache_key, cache, pypeline, step_name="reload_cached_state"):
        super().__init__(step_name=step_name, func=self.func)
        self.cache_key = cache_key
        self.cache = cache
        self.pypeline = pypeline

    def start_step(self):
        return

    def stop_step(self):
        return

    def func(self):
        parameter_index, globalcontext = self.cache.get(self.cache_key)
        self.pypeline.parameter_index = parameter_index
        self.pypeline.globalcontext = globalcontext
        return

    def __str__(self):
        return f"""{self.cache}"""