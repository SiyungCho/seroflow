"""
Module: context

This module implements context management data classes.
It provides the Context class, which is used to store and manage dataframes
across different steps in a data pipeline process. The Context class enables
data access and manipulation throughout Pipeline, facilitating coordination and 
data integrity among various processing stages.
"""

from .context import Context
