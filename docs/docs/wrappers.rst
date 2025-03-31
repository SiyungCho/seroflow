Wrappers
=========================

This module provides ``decorators`` that enhance logging capabilities. 
It includes a ``timer`` decorator to measure and log the execution time of functions and a ``log_error`` decorator that catches and logs errors during function execution.

Overview
---------------------------------

This module implements two main decorators:

- **timer**: Measures the execution time of the decorated function. 
It is designed for class methods that have a ``logger`` attribute.

- **log_error**: A decorator factory that returns a decorator for error logging. 
It wraps the target function in a try-except block, logs error details (including function name and code line), and optionally re-raises an exception with a custom error message based on the ``log_only`` flag.


wrappers
---------------------------------

.. automodule:: seroflow.wrappers.wrappers
   :members:
   :show-inheritance:
   :undoc-members:
