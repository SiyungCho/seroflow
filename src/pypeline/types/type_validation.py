"""
Module: type_validation.py

This module provides utility functions for type validation.

The functions in this module check whether a given object is an instance of a specific
base class for various ETL components (Extractor, Loader, Step, Context) or, in the case
of context objects, a dictionary of valid Context instances.
"""

from ..step.step import Step as base_step
from ..extract.extractor import Extractor as base_extractor
from ..extract.extractor import MultiExtractor as base_multiextractor
from ..load.loader import Loader as base_loader
from ..context.context import Context as base_context


def is_extractor(extractor, _raise=False):
    """
    Check if the provided object is an instance of the base_extractor class.

    Arguments:
        extractor (object): The object to check.
        _raise (bool, optional): If True, raise a TypeError when the check fails.
            Defaults to False.

    Returns:
        bool: True if the object is an instance of base_extractor, otherwise False.

    Raises:
        TypeError: If _raise is True and the object is not an instance of base_extractor.
    """
    if not isinstance(extractor, base_extractor):
        if _raise:
            raise TypeError("Not of type Extractor")
        return False
    return True

def is_multiextractor(multiextractor, _raise=False):
    """
    Check if the provided object is an instance of the base_multiextractor class.

    Arguments:
        multiextractor (object): The object to check.
        _raise (bool, optional): If True, raise a TypeError when the check fails.
            Defaults to False.

    Returns:
        bool: True if the object is an instance of base_multiextractor, otherwise False.

    Raises:
        TypeError: If _raise is True and the object is not an instance of base_multiextractor.
    """
    if not isinstance(multiextractor, base_multiextractor):
        if _raise:
            raise TypeError("Not of type multiextractor")
        return False
    return True

def is_loader(loader, _raise=False):
    """
    Check if the provided object is an instance of the base_loader class.

    Arguments:
        loader (object): The object to check.
        _raise (bool, optional): If True, raise a TypeError when the check fails.
            Defaults to False.

    Returns:
        bool: True if the object is an instance of base_loader, otherwise False.

    Raises:
        TypeError: If _raise is True and the object is not an instance of base_loader.
    """
    if not isinstance(loader, base_loader):
        if _raise:
            raise TypeError("Not of type Loader")
        return False
    return True


def is_step(step, _raise=False):
    """
    Check if the provided object is an instance of the base_step class.

    Arguments:
        step (object): The object to check.
        _raise (bool, optional): If True, raise a TypeError when the check fails.
            Defaults to False.

    Returns:
        bool: True if the object is an instance of base_step, otherwise False.

    Raises:
        TypeError: If _raise is True and the object is not an instance of base_step.
    """
    if not isinstance(step, base_step):
        if _raise:
            raise TypeError("Not of type Step")
        return False
    return True


def is_context(context, _raise=False):
    """
    Check if the provided object is an instance of the base_context class.

    Arguments:
        context (object): The object to check.
        _raise (bool, optional): If True, raise a TypeError when the check fails.
            Defaults to False.

    Returns:
        bool: True if the object is an instance of base_context, otherwise False.

    Raises:
        TypeError: If _raise is True and the object is not an instance of base_context.
    """
    if not isinstance(context, base_context):
        if _raise:
            raise TypeError("Not of type Context")
        return False
    return True


def is_context_object(context, _raise=False):
    """
    Check if the provided object is a valid context object.

    A valid context object is defined as a dictionary where each value is an instance
    of the base_context class.

    Arguments:
        context (object): The object to check. It should be a dictionary.
        _raise (bool, optional): If True, raise a TypeError when the check fails.
            Defaults to False.

    Returns:
        bool: True if the object is a dictionary containing only valid base_context instances,
        otherwise False.

    Raises:
        TypeError: If _raise is True and the object is not a dictionary, or if any value in the
        dictionary is not an instance of base_context.
    """
    if not isinstance(context, dict):
        if _raise:
            raise TypeError("Not of type Context")
        return False
    for _, item in context.items():
        if not is_context(item, _raise):
            return False
    return True
