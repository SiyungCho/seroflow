"""
Module: variable.py

This module implements a series of transformation classes for manipulating variables within the ETL pypeline.
These transformations perform arithmetic or assignment operations on variables passed as parameters to pypeline steps.
The available transformations include:
    - CopyVariable: Creates a copy of an existing variable.
    - DivideVariable: Divides a variable by a specified divisor.
    - MultiplyVariable: Multiplies a variable by a specified factor.
    - IncrementVariable: Increments a variable by a specified amount.
    - DecrementVariable: Decrements a variable by a specified amount.
    - CreateVariable: Creates a new variable with a constant value.
    - UpdateVariable: Updates an existing variable with a new value.

Each class extends the base Transformation class and implements the func() method to perform its specific operation.
"""

# class DeleteVariable(Transformation):
# class RenameVariable(Transformation): # do a copy then delete

from .transformation import Transformation

class CopyVariable(Transformation):
    """
    CopyVariable

    Copies the value of an existing variable.
    This transformation retrieves the value of a specified variable from the input parameters and returns it,
    effectively creating a duplicate value under the same variable name in the pypeline context.

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
        Initializes the CopyVariable transformation.

        Arguments:
            variable (str): The name of the variable to copy.
            new_variable (str): The new variable name for the copied value.
            step_name (str, optional): The name of this transformation step. Defaults to "CopyVariable".
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
        Executes the CopyVariable transformation.

        Retrieves the value of the specified variable from the input keyword arguments and returns it.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The value of the specified variable.
        """
        return kwargs[self.variable]


class DivideVariable(Transformation):
    """
    DivideVariable

    Divides the value of a specified variable by a given divisor.
    The result of the division is returned as the updated variable value.
    
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
        Initializes the DivideVariable transformation.

        Arguments:
            variable (str): The name of the variable whose value will be divided.
            divide_by (numeric, optional): The divisor to use in the division. Defaults to 1.
            step_name (str, optional): The name of this transformation step. Defaults to "DivideVariable".
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
        Executes the DivideVariable transformation.

        Retrieves the value of the specified variable from the input keyword arguments, divides it by the divisor,
        and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The result of dividing the variable's value by the divisor.
        """
        return kwargs[self.variable] / self.divide_by


class MultiplyVariable(Transformation):
    """
    MultiplyVariable

    Multiplies the value of a specified variable by a given factor.
    The resulting product is returned as the updated variable value.
    
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
        Initializes the MultiplyVariable transformation.

        Arguments:
            variable (str): The name of the variable whose value will be multiplied.
            multiply_by (numeric, optional): The factor to multiply by. Defaults to 1.
            step_name (str, optional): The name of this transformation step. Defaults to "MultiplyVariable".
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
        Executes the MultiplyVariable transformation.

        Retrieves the value of the specified variable from the input keyword arguments, multiplies it by the factor,
        and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The product of the variable's value and the multiplication factor.
        """
        return kwargs[self.variable] * self.multiply_by


class IncrementVariable(Transformation):
    """
    IncrementVariable

    Increments the value of a specified variable by a given amount.
    The result of the increment operation is returned as the updated variable value.
    
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
        Initializes the IncrementVariable transformation.

        Arguments:
            variable (str): The name of the variable to increment.
            increment_by (numeric, optional): The amount to add to the variable. Defaults to 1.
            step_name (str, optional): The name of this transformation step. Defaults to "IncrementVariable".
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
        Executes the IncrementVariable transformation.

        Retrieves the value of the specified variable from the input keyword arguments, adds the increment value,
        and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The incremented value of the variable.
        """
        return kwargs[self.variable] + self.increment_by


class DecrementVariable(Transformation):
    """
    DecrementVariable

    Decrements the value of a specified variable by a given amount.
    The result of the decrement operation is returned as the updated variable value.
    
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
        Initializes the DecrementVariable transformation.

        Arguments:
            variable (str): The name of the variable to decrement.
            decrement_by (numeric, optional): The amount to subtract from the variable. Defaults to 1.
            step_name (str, optional): The name of this transformation step. Defaults to "DecrementVariable".
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
        Executes the DecrementVariable transformation.

        Retrieves the value of the specified variable from the input keyword arguments, subtracts the decrement value,
        and returns the result.

        Arguments:
            **kwargs: The keyword arguments containing variable values.

        Returns:
            The decremented value of the variable.
        """
        return kwargs[self.variable] + self.decrement_by

class CreateVariable(Transformation):
    """
    CreateVariable

    Creates a new variable with a specified constant value.
    
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
        Initializes the CreateVariable transformation.

        Arguments:
            variable (str): The name of the new variable.
            value: The constant value to assign to the new variable.
            step_name (str, optional): The name of this transformation step. Defaults to "CreateVariable".
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
        Executes the CreateVariable transformation.

        Returns the constant value specified for the variable.

        Returns:
            The constant value assigned to the variable.
        """
        return self.value


class UpdateVariable(Transformation):
    """
    UpdateVariable

    Updates an existing variable with a new value.
    
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
        Initializes the UpdateVariable transformation.

        Arguments:
            variable (str): The name of the variable to update.
            value: The new value for the variable.
            step_name (str, optional): The name of this transformation step. Defaults to "UpdateVariable".
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
        Executes the UpdateVariable transformation.

        Returns the new value that should update the variable.

        Returns:
            The new value for the variable.
        """
        return self.value
