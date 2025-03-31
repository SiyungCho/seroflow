Types
======================

This module provides utility functions for type validation.
It verifies whether a given object is an instance of a specific base class for various ``Seroflow`` components—such as ``Extractor``, ``Loader``, ``Step``, and ``Context``—or, in the case of context objects, whether a dictionary contains only valid ``Context`` instances.

Overview
---------------------------------

This module includes the following functions:

- **is_extractor(extractor, _raise=False)**: Validates that an object is an instance of the base ``Extractor`` class.

- **is_multiextractor(multiextractor, _raise=False)**: Validates that an object is an instance of the base ``MultiExtractor`` class.

- **is_loader(loader, _raise=False)**: Validates that an object is an instance of the base ``Loader`` class.

- **is_step(step, _raise=False)**: Validates that an object is an instance of the base ``Step`` class.

- **is_context(context, _raise=False)**: Validates that an object is an instance of the base ``Context`` class.

- **is_context_object(context, _raise=False)**: Validates that the provided object is a dictionary where every value is a valid base ``Context`` instance.

Each function takes an optional ``_raise`` parameter. When ``_raise`` is set to ``True``, a ``TypeError`` is raised if the validation fails.


type\_validation
--------------------------------------

.. automodule:: seroflow.types.type_validation
   :members:
   :show-inheritance:
   :undoc-members:
