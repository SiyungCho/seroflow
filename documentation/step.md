# AbstractStep and Step Module Documentation

The modules documented here define the base structure and a concrete implementation for Pypeline steps. They provide a common interface to initialize, clean up, and execute operations (steps) within an ETL pipeline.

## Overview

This documentation covers two modules:

- **abstract_step**:  
  Defines the `AbstractStep` abstract class, which specifies the interface for creating steps. Subclasses must implement the abstract methods:
  - `start_step()`
  - `stop_step()`
  - `execute()`

- **step**:  
  Implements the `Step` class, a concrete subclass of `AbstractStep` that encapsulates a single operation or transformation. The `Step` class manages function initialization, parameter handling, default values, error handling, and dynamic updates to return and parameter lists.

---

## Module: abstract_step

### Class: AbstractStep

`AbstractStep` is an abstract base class that defines the structure of a Pypeline step. It extends Python’s `ABC` (Abstract Base Class) and enforces the implementation of the following methods:

- **`start_step()`**  
  *Abstract Method*  
  Should contain logic to initialize the step before execution.

- **`stop_step()`**  
  *Abstract Method*  
  Should contain logic to clean up the step after execution is complete.

- **`execute()`**  
  *Abstract Method*  
  Should contain the main functionality of the step.

**Example:**

```python
from abstract_step import AbstractStep

class MyStep(AbstractStep):
    def start_step(self):
        # Initialize resources or validate input
        pass

    def stop_step(self):
        # Perform cleanup after execution
        pass

    def execute(self):
        # Implement the step's main logic
        return "Step executed"
```
# Module: step

## Class: Step

The `Step` class is a concrete implementation of `AbstractStep` that encapsulates the logic for executing a function with given parameters and DataFrames. It also serves as a convenient wrapper, allowing you to easily create custom steps by simply decorating your function with `Step`.

---

## Key Features

- **Initialization and Function Wrapping:**
  - The `Step` class can be used as a decorator to easily create custom steps.
  - The first call after instantiation sets the step function and extracts its signature, default parameters, and return elements.
  - Subsequent calls execute the step function with updated parameters.

- **Parameter Management:**
  - Automatically constructs a parameters dictionary from:
    - The function signature.
    - Provided input parameters.
    - Default parameter values.
  - Supports methods to update or override the list of return values and parameters.

- **Error Handling:**
  - The `on_error` attribute controls error handling.
  - When set to `'raise'`, errors during execution raise an exception.
  - When set to `'ignore'`, errors are printed and execution returns `None`.

- **Context Support:**
  - If the step function has a parameter named `context`, the class marks that the step needs a context and handles it appropriately.

---

## Main Methods

- **`__init__(...)`**  
  Initializes the `Step` object with a step name, input parameters, DataFrames, error handling strategy, and optionally the step function (via a keyword argument).

- **`__call__(...)`**  
  Serves two purposes:
  - **Function Setup:**  
    On the first call (when the step function is not yet set), it initializes the step function and its parameters.
  - **Execution:**  
    On subsequent calls, it constructs the parameters dictionary and executes the step function.

- **`__init_step_func_params()`**  
  A private method that:
  - Extracts the step function’s signature.
  - Constructs a list of parameter names (excluding `context` if present).
  - Retrieves default parameter values.
  - Extracts the function’s return elements.
  - Sets the step name if not provided.

- **`get_default_params(sig)`**  
  Returns a dictionary of default parameters extracted from the function’s signature.

- **`check_params()`**  
  Validates that no parameter required for execution is left unset (`None`).

- **`add_params(params)` and `create_kwargs_params(args, kwargs)`**  
  Methods to add and update parameters from various sources (positional arguments, keyword arguments, and input defaults).

- **`start_step()` and `stop_step()`**  
  Methods to initialize and clean up the step before and after execution.

- **`execute()`**  
  Executes the step function with the assembled parameters. Handles errors based on the `on_error` strategy.

- **Helper Methods:**  
  Additional methods such as `update_return_list`, `override_return_list`, `update_params_list`, and `override_params_list` allow for dynamic modification of the return and parameters lists.

---

## Usage Example

Below is an example demonstrating how to create and use a `Step` to easily create a custom step by wrapping a function:

```python
from step import Step

# Define a sample function to be used as a step
def sample_step(a, b, context=None):
    # Example processing logic
    return a + b

# Initialize a Step with parameters and a custom function using it as a decorator/wrapper
step_instance = Step(params={'a': 1, 'b': 2}, on_error='raise', func=sample_step)

# Execute the step by calling the instance
result = step_instance()
print("Step result:", result)
```