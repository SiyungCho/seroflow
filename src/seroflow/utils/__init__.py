"""
Module: utils

This module provides a collection of utility functions for common tasks across the package. 
These functions simplify operations such as:
    - Generating unique keys (generate_key).
    - Validating and filtering keyword arguments (check_kw_in_kwargs, filter_kwargs).
    - Converting AST nodes to Python objects (_convert_ast_node_to_python).
    - Extracting return elements from function outputs (get_return_elements).
    - Managing files and directories, including:
        * Gathering files (gather_files).
        * Locating directories and files (find_dir, find_file).
        * Checking the existence and validity of directories and files
        (check_directory, check_file).
        * Creating directories and files (create_directory, create_file).
    - Manipulating strings: splitting by delimiters and removing file extensions 
      (split_last_delimiter, remove_extension, check_str_is_file).
"""
from .utils import generate_key
from .utils import check_kw_in_kwargs
from .utils import filter_kwargs
from .utils import _convert_ast_node_to_python
from .utils import get_return_elements
from .utils import gather_files
from .utils import find_dir
from .utils import find_file
from .utils import check_directory
from .utils import check_file
from .utils import create_directory
from .utils import create_file
from .utils import split_last_delimiter
from .utils import remove_extension
from .utils import check_str_is_file
