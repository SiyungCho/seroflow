"""
This module implements transformation classes for manipulating scalar variables within a ``Pipeline``.
Each class extends the base ``Transformation`` and performs a simple arithmetic or assignment operation on a named variable.
The result of each transformation is returned and can be stored back into the ``Pipeline`` context.

- **CopyVariable**: Copies the value of an existing variable under a new name.
- **DivideVariable**: Divides a variable’s value by a specified divisor.
- **MultiplyVariable**: Multiplies a variable’s value by a specified factor.
- **IncrementVariable**: Increments a variable’s value by a specified amount.
- **DecrementVariable**: Decrements a variable’s value by a specified amount.
- **CreateVariable**: Creates a new variable with a constant value.
- **UpdateVariable**: Updates an existing variable with a new value.
"""

# class DeleteVariable(Transformation):
# class RenameVariable(Transformation): # do a copy then delete

from .transformation import Transformation

class CopyVariable(Transformation):
    """
    Copies the value of an existing variable.
    This transformation retrieves the value of a specified variable from the input parameters
    and returns it, effectively creating a duplicate value under the same variable name
    in the ``Pipeline`` context.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``CopyVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import CopyVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        cp_var = CopyVariable(variable="x", new_variable="x_copy")
        pipeline.add_steps([cp_var])
        pipeline.execute()

    Attributes:
        variable (str): The name of the variable to copy.
        new_variable (str): The new variable name (unused in the current implementation).
    """
    def __init__(self,
                 variable,
                 new_variable,
                 step_name="CopyVariable",
                 on_error=None):
        """
        Initializes the ``CopyVariable`` transformation.

        Arguments:
            variable (str): The name of the variable to copy.
            new_variable (str): The new variable name for the copied value.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "CopyVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.new_variable = new_variable
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        """
        Executes the ``CopyVariable`` transformation.

        Retrieves the value of the specified variable from the input keyword arguments
        and returns it.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The value of the specified variable.
        """
        return kwargs[self.variable]


class DivideVariable(Transformation):
    """
    Divides the value of a specified variable by a given divisor.
    The result of the division is returned as the updated variable value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DivideVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DivideVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        div_var = DivideVariable(variable="x", divide_by=2)
        pipeline.add_steps([div_var])
        pipeline.execute()
    
    Attributes:
        variable (str): The name of the variable to be divided.
        divide_by (numeric): The divisor value.
    """
    def __init__(self,
                 variable,
                 divide_by=1,
                 step_name="DivideVariable",
                 on_error=None):
        """
        Initializes the ``DivideVariable`` transformation.

        Arguments:
            variable (str): The name of the variable whose value will be divided.
            divide_by (numeric, optional): The divisor to use in the division.
                                           Defaults to 1.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DivideVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.divide_by = divide_by
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        """
        Executes the ``DivideVariable`` transformation.

        Retrieves the value of the specified variable from the input keyword arguments,
        divides it by the divisor, and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The result of dividing the variable's value by the divisor.
        """
        return kwargs[self.variable] / self.divide_by


class MultiplyVariable(Transformation):
    """
    Multiplies the value of a specified variable by a given factor.
    The resulting product is returned as the updated variable value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``MultiplyVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import MultiplyVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        mul_var = MultiplyVariable(variable="y", multiply_by=3)
        pipeline.add_steps([mul_var])
        pipeline.execute()

    
    Attributes:
        variable (str): The name of the variable to be multiplied.
        multiply_by (numeric): The factor by which to multiply the variable.
    """
    def __init__(self,
                 variable,
                 multiply_by=1,
                 step_name="MultiplyVariable",
                 on_error=None):
        """
        Initializes the ``MultiplyVariable`` transformation.

        Arguments:
            variable (str): The name of the variable whose value will be multiplied.
            multiply_by (numeric, optional): The factor to multiply by. Defaults to 1.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "MultiplyVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.multiply_by = multiply_by
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        """
        Executes the ``MultiplyVariable`` transformation.

        Retrieves the value of the specified variable from the input keyword arguments,
        multiplies it by the factor, and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The product of the variable's value and the multiplication factor.
        """
        return kwargs[self.variable] * self.multiply_by


class IncrementVariable(Transformation):
    """
    Increments the value of a specified variable by a given amount.
    The result of the increment operation is returned as the updated variable value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``IncrementVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import IncrementVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        inc_var = IncrementVariable(variable="x", increment_by=10)
        pipeline.add_steps([inc_var])
        pipeline.execute()

    Attributes:
        variable (str): The name of the variable to be incremented.
        increment_by (numeric): The value by which to increment the variable.
    """
    def __init__(self,
                 variable,
                 increment_by=1,
                 step_name="IncrementVariable",
                 on_error=None):
        """
        Initializes the ``IncrementVariable`` transformation.

        Arguments:
            variable (str): The name of the variable to increment.
            increment_by (numeric, optional): The amount to add to the variable.
                                              Defaults to 1.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "IncrementVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.increment_by = increment_by
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        """
        Executes the ``IncrementVariable`` transformation.

        Retrieves the value of the specified variable from the input keyword arguments,
        adds the increment value, and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The incremented value of the variable.
        """
        return kwargs[self.variable] + self.increment_by


class DecrementVariable(Transformation):
    """
    Decrements the value of a specified variable by a given amount.
    The result of the decrement operation is returned as the updated variable value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``DecrementVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import DecrementVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        dec_var = DecrementVariable(variable="y", decrement_by=5)
        pipeline.add_steps([dec_var])
        pipeline.execute()

    Attributes:
        variable (str): The name of the variable to be decremented.
        decrement_by (numeric): The value by which to decrement the variable.
    """
    def __init__(self,
                 variable,
                 decrement_by=1,
                 step_name="DecrementVariable",
                 on_error=None):
        """
        Initializes the ``DecrementVariable`` transformation.

        Arguments:
            variable (str): The name of the variable to decrement.
            decrement_by (numeric, optional): The amount to subtract from the variable.
                                              Defaults to 1.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "DecrementVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.decrement_by = decrement_by
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        """
        Executes the ``DecrementVariable`` transformation.

        Retrieves the value of the specified variable from the input keyword arguments,
        subtracts the decrement value, and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The decremented value of the variable.
        """
        return kwargs[self.variable] + self.decrement_by

class CreateVariable(Transformation):
    """
    Creates a new variable with a specified constant value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``CreateVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import CreateVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        create_var = CreateVariable(variable="z", value=42)
        pipeline.add_steps([create_var])
        pipeline.execute()

    Attributes:
        variable (str): The name of the variable to create.
        value: The constant value to assign to the variable.
    """
    def __init__(self,
                 variable,
                 value,
                 step_name="CreateVariable",
                 on_error=None):
        """
        Initializes the ``CreateVariable`` transformation.

        Arguments:
            variable (str): The name of the new variable.
            value: The constant value to assign to the new variable.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "CreateVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.value = value
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)

    def func(self):
        """
        Executes the ``CreateVariable`` transformation.

        Returns the constant value specified for the variable.

        Returns:
            The constant value assigned to the variable.
        """
        return self.value


class UpdateVariable(Transformation):
    """
    Updates an existing variable with a new value.

    Usage Example
    ^^^^^^^^^^^^^^^^^

    Below is an example demonstrating how to use the Transformation ``UpdateVariable``: ::

        import pandas as pd
        from seroflow import Pipeline
        from seroflow.transform import UpdateVariable

        pipeline = Pipeline()
        pipeline.target_extractor = ... 

        update_var = UpdateVariable(variable="x", value=200)
        pipeline.add_steps([update_var])
        pipeline.execute()

    Attributes:
        variable (str): The name of the variable to update.
        value: The new value to assign to the variable.
    """
    def __init__(self,
                 variable,
                 value,
                 step_name="UpdateVariable",
                 on_error=None):
        """
        Initializes the ``UpdateVariable`` transformation.

        Arguments:
            variable (str): The name of the variable to update.
            value: The new value for the variable.
            step_name (str, optional): The name of this transformation step.
                                       Defaults to "UpdateVariable".
            on_error (str, optional): The error handling strategy.
        """
        self.variable = variable
        self.value = value
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)
        self.update_return_list(self.variable)

    def func(self):
        """
        Executes the ``UpdateVariable`` transformation.

        Returns the new value that should update the variable.

        Returns:
            The new value for the variable.
        """
        return self.value
