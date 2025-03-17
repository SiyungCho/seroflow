"""
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

def log_error(err_msg, log_only=False):
    """
    """
    def log_error_inner(func):
        @wraps(func)
        def wrap(*args, **kwargs):
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
                        raise Exception(err_msg) from e
                else:
                    raise Exception(err_msg) from e
                return None
        return wrap
    return log_error_inner
