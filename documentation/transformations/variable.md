# Variable Transformations Module Documentation

This module implements a series of transformation classes for manipulating variables within the ETL pypeline. These transformations perform arithmetic or assignment operations on variables passed as parameters to pypeline steps. The available transformations include:

- **CopyVariable**: Creates a copy of an existing variable.
- **DivideVariable**: Divides a variable by a specified divisor.
- **MultiplyVariable**: Multiplies a variable by a specified factor.
- **IncrementVariable**: Increments a variable by a specified amount.
- **DecrementVariable**: Decrements a variable by a specified amount.
- **CreateVariable**: Creates a new variable with a constant value.
- **UpdateVariable**: Updates an existing variable with a new value.

Each class extends the base `Transformation` class and implements the `func()` method to perform its specific operation. The transformation receives variable values as keyword arguments, processes them, and returns the updated value.

---

## Overview

The variable transformations are used to manipulate scalar values (variables) that are passed into the pypeline as part of the parameter index. These transformations allow arithmetic operations (e.g., division, multiplication, increment, decrement) and assignment operations (e.g., copy, create, update) on these variables. The results can then be stored back into the pypeline context.

---

## Transformation Classes

### CopyVariable

**Description:**  
Copies the value of an existing variable, effectively duplicating it under a new variable name.

**Constructor Arguments:**
- `variable` (*str*): Name of the variable to copy.
- `new_variable` (*str*): The new variable name for the copied value.
- `step_name` (*str*, optional): Defaults to `"CopyVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func(**kwargs)`: Retrieves the value of the specified variable from the input keyword arguments and returns it.

---

### DivideVariable

**Description:**  
Divides the value of a specified variable by a given divisor.

**Constructor Arguments:**
- `variable` (*str*): The name of the variable to be divided.
- `divide_by` (*numeric*, optional): The divisor (default is `1`).
- `step_name` (*str*, optional): Defaults to `"DivideVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func(**kwargs)`: Returns the result of dividing the variable's value by the divisor.

---

### MultiplyVariable

**Description:**  
Multiplies the value of a specified variable by a given factor.

**Constructor Arguments:**
- `variable` (*str*): The name of the variable to be multiplied.
- `multiply_by` (*numeric*, optional): The factor (default is `1`).
- `step_name` (*str*, optional): Defaults to `"MultiplyVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func(**kwargs)`: Returns the product of the variable's value and the multiplication factor.

---

### IncrementVariable

**Description:**  
Increments the value of a specified variable by a given amount.

**Constructor Arguments:**
- `variable` (*str*): The name of the variable to increment.
- `increment_by` (*numeric*, optional): The amount to add (default is `1`).
- `step_name` (*str*, optional): Defaults to `"IncrementVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func(**kwargs)`: Returns the variable's value incremented by the specified amount.

---

### DecrementVariable

**Description:**  
Decrements the value of a specified variable by a given amount.

**Constructor Arguments:**
- `variable` (*str*): The name of the variable to decrement.
- `decrement_by` (*numeric*, optional): The amount to subtract (default is `1`).
- `step_name` (*str*, optional): Defaults to `"DecrementVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func(**kwargs)`: Returns the variable's value decremented by the specified amount.

*Note: In the current implementation, the `DecrementVariable` transformation uses a `+` operator instead of subtraction. This may be a bug and should be verified.*

---

### CreateVariable

**Description:**  
Creates a new variable with a specified constant value.

**Constructor Arguments:**
- `variable` (*str*): The name of the new variable.
- `value`: The constant value to assign.
- `step_name` (*str*, optional): Defaults to `"CreateVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func()`: Returns the constant value to be assigned to the new variable.

---

### UpdateVariable

**Description:**  
Updates an existing variable with a new value.

**Constructor Arguments:**
- `variable` (*str*): The name of the variable to update.
- `value`: The new value for the variable.
- `step_name` (*str*, optional): Defaults to `"UpdateVariable"`.
- `on_error` (*str*, optional): Error handling strategy.

**Method:**
- `func()`: Returns the new value that should update the variable.

---

## Usage Example

Below is an example demonstrating how to use these variable transformation classes within a pypeline step:

```python
from variable import CopyVariable, DivideVariable, MultiplyVariable, IncrementVariable, DecrementVariable, CreateVariable, UpdateVariable

# Assume we have a pypeline step that receives variables as keyword arguments.
# For demonstration, we simulate the variable operations by passing a dictionary.

# Example input variable dictionary:
variables = {
    "x": 100,
    "y": 50
}

# Copy variable "x" to a new variable "x_copy"
copy_transform = CopyVariable(variable="x", new_variable="x_copy")
x_copy = copy_transform.func(**variables)
print("Copied Variable x:", x_copy)

# Divide variable "x" by 2
divide_transform = DivideVariable(variable="x", divide_by=2)
x_divided = divide_transform.func(**variables)
print("x divided by 2:", x_divided)

# Multiply variable "y" by 3
multiply_transform = MultiplyVariable(variable="y", multiply_by=3)
y_multiplied = multiply_transform.func(**variables)
print("y multiplied by 3:", y_multiplied)

# Increment variable "x" by 10
increment_transform = IncrementVariable(variable="x", increment_by=10)
x_incremented = increment_transform.func(**variables)
print("x incremented by 10:", x_incremented)

# Decrement variable "y" by 5
decrement_transform = DecrementVariable(variable="y", decrement_by=5)
y_decremented = decrement_transform.func(**variables)
print("y decremented by 5:", y_decremented)

# Create a new variable "z" with value 42
create_transform = CreateVariable(variable="z", value=42)
z_value = create_transform.func()
print("Created variable z:", z_value)

# Update variable "x" with a new value 200
update_transform = UpdateVariable(variable="x", value=200)
x_updated = update_transform.func()
print("Updated variable x:", x_updated)