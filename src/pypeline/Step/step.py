from .base_step import abstract_step
from ..Utils.utils import *

class step(abstract_step):
    def __init__(self, step_name=None, params={}, dataframes = [], **kwargs):
        self.step_name = step_name
        self.input_params = params
        self.dataframes = None if dataframes == [] else dataframes
        
        if 'func' in kwargs:
            self.step_func = kwargs['func']
            self.init_step_func_params()
        else:
            self.step_func = None

    def __call__(self, *args, **kwargs):
        if self.step_func is None:
            if not (len(args) == 1 and callable(args[0]) and not kwargs):
                raise TypeError("First call after init should be decorated function")
            self.step_func = args[0]
            self.init_step_func_params()
            return self
        else:
            self.params = {param: None for param in self.params_list}
            self.create_kwargs_params(args, kwargs)
            if 'kwargs' in self.params:
                self.params.pop('kwargs')
            return self.execute()
        
    def init_step_func_params(self):
        self.step_signature = inspect.signature(self.step_func)
        self.params_list = list(self.step_signature.parameters.keys())
        self.default_params = self.get_default_params(self.step_signature)
        self.return_list = get_return_elements(self.step_func)
        
        if self.step_name is None:
            self.step_name = self.step_func.__name__
        return
    
    def get_default_params(self, sig):
        default_params = {
            param_name: default_value.default
            for param_name, default_value in sig.parameters.items()
            if default_value.default is not inspect.Parameter.empty
        }
        return default_params
    
    def check_params(self):
        for param, value in self.params.items():
            if value is None:
                raise Exception(f"Error parameter {param} has value None, please either explicitly pass in a value or set a default")

    def add_params(self, params):
        for param, value in params.items():
            if param not in self.params:
                if 'kwargs' not in self.params:
                    raise Exception("Error parameter given not found in function signature")
                self.params[param] = value
            elif self.params[param] is None:
                self.params[param] = value

    def create_kwargs_params(self, args, kwargs):
        for index, value in enumerate(args):
            kwargs[list(self.params.keys())[index]] = value

        self.add_params(kwargs)
        self.add_params(self.input_params)
        self.add_params(self.default_params)

    def start_step(self):
        self.check_params()
        return

    def stop_step(self):
        self.params.clear()
        return

    def execute(self):
        self.start_step()
        self.step_output = self.step_func(**self.params)
        self.stop_step()
        return self.step_output

    def __str__(self):
        print(self.description)
        print(self.mode)
        print(self.input_params)
        return self.step_name
