import os
import sys

from functools import wraps
import time
from Exceptions import base_exception

def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        args[0].logger.info(f"""{func.__name__} took: {end-start} sec """)
        return result
    return wrap

def log_error(err_msg, logger, log_only = False):
    def log_error_inner(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb_last_frame = traceback.extract_tb(e.__traceback__)[-1]
                filename, linenum, functioname, codeline = tb_last_frame
                logger.error(f"""Error {err_msg} ; Occured at: {functioname} ; On line number: {codeline} ; Exception {e} """)
                if not log_only:
                    raise Exception(f"""{e}; {err_msg} """)
            return wrap
        return log_error_inner