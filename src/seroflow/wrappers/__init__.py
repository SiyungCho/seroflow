"""
Module: wrappers

This module aggregates decorator wrappers used throughout the package
for performance monitoring and error handling.
It provides easy-to-use wrappers that can be applied to functions to:
    - Measure and log execution time (via the timer decorator).
    - Catch, log, and handle exceptions gracefully (via the log_error decorator).
"""

from .wrappers import timer
from .wrappers import log_error
