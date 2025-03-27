"""
Module: step

This module implements the Step class, an implementation of AbstractStep that encapsulates an
operation or transformation. The Step class provides functionality to initialize the step
function, manage input parameters and default values, execute the function, and handle errors.
It also supports dynamic updates to the list of return values and parameters.
"""


import inspect
from .base_step import AbstractStep
from ..utils.utils import get_return_elements

class Step(AbstractStep):
    """
    Step

    An implementation of a step that encapsulates the logic for executing a function with
    specified parameters and DataFrames. The Step class allows configuration of function
    parameters, extraction of default values, and error handling based on a defined strategy.
    """

    def __init__(self,
                 step_name=None,
                 params=None,
                 dataframes=None,
                 on_error='raise',
                 **kwargs):
        """
        Step Class Constructor
        Initializes the Step object.

        Arguments:
            step_name (str): 
                The name of the step
            params (dict): 
                The parameters to be passed to the function
            dataframes (List): 
                The DataFrames to be used in the step
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the function
        """
        self.step_name = step_name
        self.input_params = {} if params is None else params
        self.dataframes = dataframes if dataframes is not None else []
        self.params = None
        self.params_list = []
        self.default_params = {}
        self.return_list = [None]
        self.on_error = on_error
        self.needs_context = False

        if 'func' in kwargs:
            self.step_func = kwargs['func']
            self.__init_step_func_params()
        else:
            self.step_func = None

    def __call__(self, *args, **kwargs):
        """
        Call method for Step class
        This method is called when the Step object is called as a function.
        When creating a custom step, the first call should be the decorated function.
        This will initialize the step function and its parameters.
        Subsequent calls will execute the step function with the given parameters.
        Arguments and keyword arguments are passed to function and saved inside the Step object.
        The argument 'context' is reserved for the context object and should not be a parameter.

        Arguments:
            *args: 
                The arguments to be passed to the function
            **kwargs: 
                The keyword arguments to be passed to the function
        """
        if self.step_func is None:
            if not (len(args) == 1 and callable(args[0]) and not kwargs):
                raise TypeError("First call after init should be decorated function")
            self.step_func = args[0]
            self.__init_step_func_params()
            return self
        self.params = {param: None for param in self.params_list}
        if self.needs_context:
            self.params['context'] = None
        self.create_kwargs_params(args, kwargs)
        if 'kwargs' in self.params:
            self.params.pop('kwargs')
        return self.execute()

    def __init_step_func_params(self):
        """
        Private method: __init_step_func_params()
        Initializes the parameters of the step function.
        Gets the signature of the step function and extracts the parameter names.
        If the function has a 'context' parameter, it is removed from the list.
        The default parameters are extracted from the signature.
        The return elements of the function are extracted.
        The step name is set to the name of the function if not provided.
        """
        self.step_signature = inspect.signature(self.step_func)
        self.params_list = list(self.step_signature.parameters.keys())
        if 'context' in self.params_list:
            self.needs_context = True
            self.params_list.remove('context')
        self.default_params = self.get_default_params(self.step_signature)
        self.return_list = get_return_elements(self.step_func)

        if self.step_name is None:
            self.step_name = self.step_func.__name__

    def get_default_params(self, sig):
        """
        Public method: get_default_params()
        Gets the default parameters of the step function.

        Arguments:
            sig (Signature): 
                The signature of the step function

        Returns:
            dict: 
                The default parameters of the step function
        """
        default_params = {
            param_name: default_value.default
            for param_name, default_value in sig.parameters.items()
            if default_value.default is not inspect.Parameter.empty
        }
        return default_params

    def check_params(self):
        """
        Public method: check_params()
        Checks if any of the parameters are None.
        This method is called before executing the step function.
        If any parameter is None, a ValueError is raised

        Raises:
            ValueError: 
                If any parameter is None
        """
        for param, value in self.params.items():
            if value is None:
                raise ValueError(f"Error parameter {param} has value None")

    def add_params(self, params):
        """
        Public method: add_params()
        Adds parameters to the step function.
        If the parameter is not in the function signature, a ValueError is raised.
        If the parameter is already set, it is not overwritten.

        Arguments:
            params (dict): 
                The parameters to be added to the step function

        Raises:
            ValueError: 
                If the parameter is not in the function signature
        """
        for param, value in params.items():
            if param not in self.params:
                if 'kwargs' not in self.params:
                    raise ValueError("Error parameter given not found in function signature")
                self.params[param] = value
            elif self.params[param] is None:
                self.params[param] = value

    def create_kwargs_params(self, args, kwargs):
        """
        Public method: create_kwargs_params()
        Creates the parameters dictionary for the step function.
        Arguments are passed to the function based on their order.
        Keyword arguments are passed to the function based on their name.
        If the function has a 'context' parameter, it is added to the parameters dictionary.
        The input parameters are added to the parameters dictionary.
        The default parameters are added to the parameters dictionary.

        Arguments:
            args: 
                The arguments to be passed to the function
            kwargs: 
                The keyword arguments to be passed to the
        """
        for index, value in enumerate(args):
            kwargs[list(self.params.keys())[index]] = value

        self.add_params(kwargs)
        self.add_params(self.input_params)
        self.add_params(self.default_params)

    def start_step(self):
        """
        Public method: start_step()
        Validates that the inputted context is of the correct type
        """
        self.check_params()

    def stop_step(self):
        """
        Public method: stop_step()
        Clears the parameters dictionary so that the step can be executed again
        """
        self.params.clear()

    def execute(self):
        """
        Public method: execute()
        Executes the step function with the given parameters.
        If an error occurs during execution, the error is caught and handled
        based on the on_error parameter.
        If the on_error parameter is set to 'raise', the error is raised.
        If the on_error parameter is set to 'ignore', the error is printed
        and the step output is set to None.

        Returns:
            Any: 
                The output of the step function

        Raises:
            RuntimeError: 
                If the on_error parameter is set to 'raise' and an error occurs during
                the execution of the step function
        """
        self.start_step()
        try:
            step_output = self.step_func(**self.params)
        except Exception as e:
            if self.on_error == 'raise':
                raise RuntimeError("Error in step Execution") from e
            print(f"Error in {self.step_name} was ignored: {e}")
            step_output = None
        self.stop_step()
        return step_output

    def __str__(self):
        """
        Public method: __str__()
        Returns the name of the step and the input parameters.
        When the Step object is printed, this method is called.
        Or when the object is converted to a string, this method is called.

        Returns:
            str: 
                The name of the step and the input parameters
        """
        return self.step_name

    def update_return_list(self, variable):
        """
        Public method: update_return_list()
        Updates the return list with the given variable
        If the return list is empty, the variable is added to the list.
        Otherwise, the variable is appended to the list.
        Used externally to explicitly set the return list.

        Arguments:
            variable: 
                The variable to be added to the return list
        """
        if self.return_list == [None]:
            self.return_list = [variable]
        else:
            self.return_list.append(variable)

    def override_return_list(self, variable):
        """
        Public method: override_return_list()
        Overrides the return list with the given variable.
        Used externally to explicitly set the return list.

        Arguments:
            variable: 
                The variable to be added to the return list
        """
        self.return_list = [variable]

    def update_params_list(self, variable):
        """
        Public method: update_params_list()
        Updates the params list with the given variable.
        If the params list is empty, the variable is added to the list.
        Otherwise, the variable is appended to the list.
        Used externally to explicitly set the params list

        Arguments:
            variable: 
                The variable to be added to the params list
        """
        self.params_list.remove("kwargs")
        if self.params_list == [None]:
            self.params_list = [variable]
        else:
            self.params_list.append(variable)

    def override_params_list(self, variable):
        """
        Public method: override_params_list()
        Overrides the params list with the given variable.
        Used externally to explicitly set the params list.

        Arguments:
            variable: 
                The variable to be added to the params list
        """
        self.params_list.remove("kwargs")
        self.params_list = [variable]
