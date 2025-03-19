# Wrappers Documentation

The `wrappers` module provides decorators that enhance logging capabilities. It includes a *timer* decorator to measure and log the execution time of functions and a *log_error* decorator that catches and logs errors during function execution.

## Overview

This module implements two main decorators:

- **`timer`**:  
  Measures the execution time of the decorated function. It is designed for class methods that have a `logger` attribute.

- **`log_error`**:  
  A decorator factory that returns a decorator for error logging. It wraps the target function in a try-except block, logs error details (including function name and code line), and optionally re-raises an exception with a custom error message based on the `log_only` flag.

## Decorators

### `@timer`

The `timer` decorator logs the execution time of the decorated function by measuring the time before and after the function call.

- **Parameters:**
  - `func` (function): The function whose execution time is measured.

- **Returns:**
  - The wrapped function with execution time logging.

- **Usage Example:**

  ```python
  from wrappers import timer

  class Example:
      def __init__(self, logger):
          self.logger = logger

      @timer
      def process(self):
          # Function logic here
          pass
  ```
### `@log_error`

The `log_error` decorator is a factory that creates a decorator to log errors that occur during function execution.

- **Parameters:**
  - `err_msg` (str): A custom error message used when re-raising an exception.
  - `log_only` (bool, optional):
    - Default is False: the exception is logged and re-raised with the custom error message.
    - When set to True: the exception is only logged and not re-raised.
- **Behavior:**
  - Wraps the decorated function in a try-except block.
  - On exception, extracts error details (such as the function name and the code line where the error occurred) using the traceback.
  - Uses the object’s logger (if available) to log error details.
  - Depending on the log_only flag, either re-raises a new exception with the custom error message or suppresses the exception.

- **Usage Example:**

  ```python

  from wrappers import log_error

    class Example:
        def __init__(self, logger):
            self.logger = logger

        def logger_is_set(self):
            return self.logger is not None

        @log_error("An error occurred in process")
        def process(self):
            # Function logic that might raise an error
            raise ValueError("Example error")
  ```