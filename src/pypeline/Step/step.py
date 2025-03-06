"""
Module that defines the Step class for processing pipeline steps.

This module implements the Step class which extends the AbstractStep base class.
The Step class manages the initialization, parameter handling, and execution of a processing step.
It supports decorating a function to be executed as part of the step and dynamically maps function
parameters with provided values.
"""

import inspect
from .base_step import AbstractStep
from ..utils.utils import get_return_elements


class Step(AbstractStep):
    """
    A concrete implementation of a processing step.

    The Step class allows a function to be decorated as a processing step. It handles
    parameter initialization, default values, and execution of the function with the provided parameters.
    """

    def __init__(self, step_name=None, params={}, dataframes=[], **kwargs):
        """
        Initialize a Step instance.

        Args:
            step_name (str, optional): The name of the step. If not provided, it will be set to the name
                of the function decorated later.
            params (dict, optional): A dictionary of initial parameters for the step.
            dataframes (list, optional): A list of dataframes associated with the step. Defaults to an empty list.
            **kwargs: Additional keyword arguments. If 'func' is provided, it will be used as the step function.
        """
        self.step_name = step_name
        self.input_params = params
        self.dataframes = None if dataframes == [] else dataframes

        if 'func' in kwargs:
            self.step_func = kwargs['func']
            self.init_step_func_params()
        else:
            self.step_func = None

    def __call__(self, *args, **kwargs):
        """
        Callable interface for the Step instance.

        On the first call, the method expects a decorated function as the sole argument,
        which is then set as the step function. On subsequent calls, the provided arguments and keyword
        arguments are used to update the function parameters and execute the step.

        Args:
            *args: Positional arguments to pass to the step function.
            **kwargs: Keyword arguments to pass to the step function.

        Returns:
            The output of the step function after execution.

        Raises:
            TypeError: If the first call does not provide a callable function as expected.
        """
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
        """
        Initialize the step function's parameters.

        Retrieves the function signature, extracts the list of parameter names,
        default parameter values, and the list of expected return elements.
        If the step name was not provided during initialization, it is set to the function's name.
        """
        self.step_signature = inspect.signature(self.step_func)
        self.params_list = list(self.step_signature.parameters.keys())
        self.default_params = self.get_default_params(self.step_signature)
        self.return_list = get_return_elements(self.step_func)

        if self.step_name is None:
            self.step_name = self.step_func.__name__
        return

    def get_default_params(self, sig):
        """
        Extract default parameters from the function signature.

        Args:
            sig (inspect.Signature): The signature of the step function.

        Returns:
            dict: A dictionary mapping parameter names to their default values for parameters that have defaults.
        """
        default_params = {
            param_name: default_value.default
            for param_name, default_value in sig.parameters.items()
            if default_value.default is not inspect.Parameter.empty
        }
        return default_params

    def check_params(self):
        """
        Check that all parameters have been assigned values.

        Raises:
            Exception: If any parameter in self.params has a value of None.
        """
        for param, value in self.params.items():
            if value is None:
                raise Exception(f"Error parameter {param} has value None, please either explicitly pass in a value or set a default")

    def add_params(self, params):
        """
        Add parameters to the current parameter dictionary.

        This method updates self.params with values from the given dictionary.
        If a parameter is not present in self.params and 'kwargs' is not a key, an Exception is raised.

        Args:
            params (dict): A dictionary of parameters to add.
        """
        for param, value in params.items():
            if param not in self.params:
                if 'kwargs' not in self.params:
                    raise Exception("Error parameter given not found in function signature")
                self.params[param] = value
            elif self.params[param] is None:
                self.params[param] = value

    def create_kwargs_params(self, args, kwargs):
        """
        Create and update the step function's parameters using provided arguments.

        Maps positional arguments to parameter names, then updates the parameters with keyword arguments,
        input parameters, and default parameters.

        Args:
            args (tuple): Positional arguments provided during the call.
            kwargs (dict): Keyword arguments provided during the call.
        """
        for index, value in enumerate(args):
            kwargs[list(self.params.keys())[index]] = value

        self.add_params(kwargs)
        self.add_params(self.input_params)
        self.add_params(self.default_params)

    def start_step(self):
        """
        Prepare the step for execution by checking parameter values.

        Raises:
            Exception: If any required parameter has not been assigned a value.
        """
        self.check_params()
        return

    def stop_step(self):
        """
        Finalize the step by clearing the parameters.
        """
        self.params.clear()
        return

    def execute(self):
        """
        Execute the step function with the current parameters.

        Calls start_step() to ensure parameters are valid, executes the function,
        then calls stop_step() to clear parameters.

        Returns:
            The output produced by the step function.
        """
        self.start_step()
        self.step_output = self.step_func(**self.params)
        self.stop_step()
        return self.step_output

    def __str__(self):
        """
        Return a string representation of the Step instance.

        Prints the description, mode, and input parameters, then returns the step name.

        Returns:
            str: The name of the step.
        """
        print(self.description)
        print(self.mode)
        print(self.input_params)
        return self.step_name
