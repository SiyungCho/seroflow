# Type Validation Documentation

The `type_validation.py` module provides utility functions for type validation. It verifies whether a given object is an instance of a specific base class for various ETL components—such as Extractor, Loader, Step, and Context—or, in the case of context objects, whether a dictionary contains only valid Context instances.

## Overview

This module includes the following functions:

- **`is_extractor(extractor, _raise=False)`**  
  Validates that an object is an instance of the base Extractor class.

- **`is_multiextractor(multiextractor, _raise=False)`**  
  Validates that an object is an instance of the base MultiExtractor class.

- **`is_loader(loader, _raise=False)`**  
  Validates that an object is an instance of the base Loader class.

- **`is_step(step, _raise=False)`**  
  Validates that an object is an instance of the base Step class.

- **`is_context(context, _raise=False)`**  
  Validates that an object is an instance of the base Context class.

- **`is_context_object(context, _raise=False)`**  
  Validates that the provided object is a dictionary where every value is a valid base Context instance.

Each function takes an optional `_raise` parameter. When `_raise` is set to `True`, a `TypeError` is raised if the validation fails.

## Functions

### `is_extractor(extractor, _raise=False)`

Checks if the provided object is an instance of the base Extractor class.

- **Arguments:**
  - `extractor` (*object*): The object to validate.
  - `_raise` (*bool*, optional): If `True`, a `TypeError` is raised on failure. Defaults to `False`.
- **Returns:**
  - *bool*: `True` if `extractor` is an instance of the base Extractor, otherwise `False`.
- **Raises:**
  - `TypeError`: If `_raise` is `True` and the object is not a valid Extractor.

---

### `is_multiextractor(multiextractor, _raise=False)`

Checks if the provided object is an instance of the base MultiExtractor class.

- **Arguments:**
  - `multiextractor` (*object*): The object to validate.
  - `_raise` (*bool*, optional): If `True`, a `TypeError` is raised on failure. Defaults to `False`.
- **Returns:**
  - *bool*: `True` if `multiextractor` is an instance of the base MultiExtractor, otherwise `False`.
- **Raises:**
  - `TypeError`: If `_raise` is `True` and the object is not a valid MultiExtractor.

---

### `is_loader(loader, _raise=False)`

Checks if the provided object is an instance of the base Loader class.

- **Arguments:**
  - `loader` (*object*): The object to validate.
  - `_raise` (*bool*, optional): If `True`, a `TypeError` is raised on failure. Defaults to `False`.
- **Returns:**
  - *bool*: `True` if `loader` is an instance of the base Loader, otherwise `False`.
- **Raises:**
  - `TypeError`: If `_raise` is `True` and the object is not a valid Loader.

---

### `is_step(step, _raise=False)`

Checks if the provided object is an instance of the base Step class.

- **Arguments:**
  - `step` (*object*): The object to validate.
  - `_raise` (*bool*, optional): If `True`, a `TypeError` is raised on failure. Defaults to `False`.
- **Returns:**
  - *bool*: `True` if `step` is an instance of the base Step, otherwise `False`.
- **Raises:**
  - `TypeError`: If `_raise` is `True` and the object is not a valid Step.

---

### `is_context(context, _raise=False)`

Checks if the provided object is an instance of the base Context class.

- **Arguments:**
  - `context` (*object*): The object to validate.
  - `_raise` (*bool*, optional): If `True`, a `TypeError` is raised on failure. Defaults to `False`.
- **Returns:**
  - *bool*: `True` if `context` is an instance of the base Context, otherwise `False`.
- **Raises:**
  - `TypeError`: If `_raise` is `True` and the object is not a valid Context.

---

### `is_context_object(context, _raise=False)`

Checks if the provided object is a valid context object, defined as a dictionary where each value is an instance of the base Context class.

- **Arguments:**
  - `context` (*object*): The object to validate. Should be a dictionary.
  - `_raise` (*bool*, optional): If `True`, a `TypeError` is raised on failure. Defaults to `False`.
- **Returns:**
  - *bool*: `True` if `context` is a dictionary containing only valid Context instances, otherwise `False`.
- **Raises:**
  - `TypeError`: If `_raise` is `True` and the object is not a dictionary or if any of its values are not valid Context instances.

## Usage Example

Below is an example demonstrating how to use these type validation functions:

```python
from type_validation import (
    is_extractor,
    is_multiextractor,
    is_loader,
    is_step,
    is_context,
    is_context_object,
)

from pypeline.context import Context
from pypeline.extract import ExcelExtractor

my_extractor = ExcelExtractor(...)
my_context = Context(...)

# Validate an extractor instance:
if is_extractor(my_extractor, _raise=True):
    print("Valid extractor")

# Validate a context object (dictionary of contexts):
context_obj = {"main": my_context}
if is_context_object(context_obj, _raise=True):
    print("Valid context object")
```