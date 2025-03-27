"""
Module: wrappers

This module provides decorators which aid with enhanced logging capabilities.
It includes a timer decorator to measure and log the execution time of functions,
and a log_error decorator that catches exceptions during function execution,
logs error details (such as the function name and line number), and optionally
re-raises a new exception with a custom error message.
"""

from functools import wraps
import time
import traceback

def timer(func):
    """
    Decorator that logs the execution time of the decorated function.
    Execution time is computed by measuring time before and after the function call.
    * only compatible with class methods that have a logger attribute.
    
    Arguments:
        func (function): The function whose execution time will be measured.

    Returns:
        function: The wrapped function with execution time logging.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        args[0].logger.info("%s took: %s sec", func.__name__, end - start)
        return result
    return wrap

def log_error(err_msg, log_only=False):
    """
    Decorator factory that returns a decorator to log errors during function execution.

    This decorator wraps the target function in a try-except block.
    If an exception occurs, it extracts the location of the error and logs the error
    using the object's logger if it is set. 
    Depending on the 'log_only' flag, it either re-raises a new exception with a custom 
    error message or simply logs the error.

    Arguments:
        err_msg (string):
            Custom error message to be used when re-raising the exception.
        log_only (bool, optional):
            False (Default): re-raises the exception with a custom error message.
            True: only logs the error without re-raising the exception.

    Returns:
        function:
            Decorator that can be applied to a function to add error logging.
    """
    def log_error_inner(func):
        """
        Inner decorator that wraps target function with error logging.

        Arguments:
            func (function):
                The function to be wrapped.

        Returns:
            function:
                The wrapped function that logs errors if they occur.
        """
        @wraps(func)
        def wrap(*args, **kwargs):
            """
            Wraps the decorated function in a try-except block to catch and log exceptions.

            If an exception occurs, logs the function name and the code line of the error.
            If the logger is set on the first argument, logs the error details.
            Depending on the log_only flag, the function either re-raises a new 
            exception with a custom error message or suppresses the exception after logging.

            Returns:
                The result of the function:
                    If no exception occurs
                None:
                    If the exception is logged and suppressed.
            """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb_last_frame = traceback.extract_tb(e.__traceback__)[-1]
                _, _, function_name, code_line = tb_last_frame
                if args[0].logger_is_set():
                    raised_msg = f"Error Occurred at: {function_name}; On line: {code_line};"
                    args[0].logger.error(raised_msg)
                    if not log_only:
                        args[0].logger.error(f"Exception {e}")
                        raise RuntimeError(err_msg) from e
                else:
                    raise RuntimeError(err_msg) from e
                return None
        return wrap
    return log_error_inner
