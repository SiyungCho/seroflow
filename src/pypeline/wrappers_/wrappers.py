"""
This module provides decorators for function instrumentation.

It includes:
    - timer:
    A decorator that measures and logs the execution time of a function.
    - log_error:
    A decorator generator that logs errors occurring in a function. 
    Optionally re-raises the exception.
"""

from functools import wraps
import time
import traceback

def timer(func):
    """
    Decorator that logs the execution time of the decorated function.

    The execution time is computed by measuring the time before and after the function call.
    It is assumed that the first positional argument of the decorated function is an object
    with a 'logger' attribute which is used for logging.

    Args:
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

def log_error(err_msg, logger, log_only=False):
    """
    Decorator generator that logs errors occurring in a function.
    Optionally re-raises the exception.

    When the decorated function raises an exception, 
    the decorator logs an error message that includes:
        - A custom error message (err_msg).
        - The function name and line number where the error occurred.
        - The exception details.
    If log_only is False, the exception is re-raised after logging.

    Args:
        err_msg (str): A custom error message to include in the log.
        logger (logging.Logger): 
            The logger instance used to log error messages.
        log_only (bool, optional): 
            If True, the error is logged without re-raising the exception.
            Defaults to False.

    Returns:
        function: A decorator that wraps the target function with error logging.
    """
    def log_error_inner(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb_last_frame = traceback.extract_tb(e.__traceback__)[-1]
                _, _, function_name, code_line = tb_last_frame
                logger.error("Error %s; Occurred at: %s; On line number: %s; Exception %s",
                             err_msg, function_name, code_line, e)
                if not log_only:
                    raise Exception("%s; %s" % (e, err_msg))
        return wrap
    return log_error_inner
