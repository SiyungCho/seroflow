"""
Module: step

This module implements the core step functionality. It provides the base classes and structures
for representing individual steps in a data processing workflow. 
The abstract class, AbstractStep, defines the interface and properties for any Pipeline step
The concrete class, Step, implements the behaviors to enable custom processing logic.
Any custom Step created should derive from the Step class, however AbstractStep can be used.

Key Components:
    - AbstractStep: 
        Abstract Class for creating new steps, ensures all steps adhere to the same interface.
    - Step: 
        Implementation of a Pipeline step, encapsulating logic for executing a specific step and 
        managing its integration with Pipeline's global context and parameters.
"""

from .base_step import AbstractStep
from .step import Step

__all__ = [
    "AbstractStep",
    "Step",
]
