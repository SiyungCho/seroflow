"""
Module: utils.py

This module provides utility functions for various common operations such as:

    - Generating hash keys from strings.
    - Retrieving and hashing function source code.
    - Checking for keyword presence in dictionaries.
    - Filtering dictionaries.
    - Converting AST nodes to Python objects.
    - Extracting return elements from function source code.
    - Gathering files from a directory based on file extensions.
    - Checking and creating files and directories.
    - Splitting strings by the last delimiter and removing file extensions.
"""

import os
import inspect
import ast
import textwrap
import hashlib


def generate_key(input_string):
    """
    Generate a unique MD5 hash key from the given input string.

    Args:
        input_string (str): The input string to hash.

    Returns:
        str: The MD5 hash of the input string in hexadecimal format.
    """
    return hashlib.md5(input_string.encode('utf-8')).hexdigest()


def get_function_source(func):
    """
    Retrieve the source code of the given function.

    Args:
        func (function): The function whose source code is to be retrieved.

    Returns:
        str: The source code of the function.
    """
    return inspect.getsource(func)


def hash_source(source):
    """
    Generate a SHA-256 hash for the given source string.

    Args:
        source (str): The source code string to hash.

    Returns:
        str: The SHA-256 hash of the source in hexadecimal format.
    """
    return hashlib.sha256(source.encode('utf-8')).hexdigest()


def get_function_hash(func):
    """
    Retrieve the source code of a function and compute its SHA-256 hash.

    Args:
        func (function): The function for which to compute the hash.

    Returns:
        tuple: A tuple containing:
            - source_code (str): The source code of the function.
            - code_hash (str): The SHA-256 hash of the source code.
    """
    source_code = get_function_source(func)
    code_hash = hash_source(source_code)
    return source_code, code_hash


def check_kw_in_kwargs(kw, kwargs):
    """
    Check if a given keyword exists in the provided kwargs dictionary.

    Args:
        kw (str): The keyword to search for.
        kwargs (dict): The dictionary of keyword arguments.

    Returns:
        bool: True if the keyword is present, False otherwise.
    """
    return kw not in kwargs


def filter_kwargs(kwargs, keys_to_remove):
    """
    Filter out specified keys from a dictionary of keyword arguments.

    Args:
        kwargs (dict): The original dictionary of keyword arguments.
        keys_to_remove (iterable): An iterable of keys to be removed from kwargs.

    Returns:
        dict: A new dictionary with the specified keys removed.
    """
    return {key: value for key, value in kwargs.items() if key not in keys_to_remove}


def _convert_ast_node_to_python(node):
    """
    Convert an AST node to its corresponding Python object representation, if possible.

    This function handles AST nodes representing names and constants.

    Args:
        node (ast.AST): The AST node to convert.

    Returns:
        object: The Python representation of the node 
        (e.g., a string for ast.Name or a literal for ast.Constant),
                or None if the node type is unsupported.
    """
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return node.value
    return None


def get_return_elements(func):
    """
    Extract and return the elements of the return statement from a function's source code.

    This function uses AST parsing to inspect the function definition and extract the
    values returned by the function. If the return value is a tuple, each element is
    converted using `_convert_ast_node_to_python`.

    Args:
        func (function): The function from which to extract return elements.

    Returns:
        list: A list of elements extracted from the return statement. Returns an empty list
              if no return statement or elements are found.
    """
    source = inspect.getsource(func)
    source = textwrap.dedent(source)
    tree = ast.parse(source)
    func_def = next((node for node in tree.body if isinstance(node, ast.FunctionDef)), None)
    if not func_def:
        return []

    return_node = next((node for node in ast.walk(func_def) if isinstance(node, ast.Return)), None)
    if not return_node or not return_node.value:
        return []

    elements = []
    if isinstance(return_node.value, ast.Tuple):
        for elt in return_node.value.elts:
            elements.append(_convert_ast_node_to_python(elt))
    else:
        elements.append(_convert_ast_node_to_python(return_node.value))
    return elements


def gather_files(source, file_type):
    """
    Gather files from a specified directory that match the given file extensions.

    Args:
        source (str): The directory path to search for files.
        file_type (iterable): An iterable of file extension strings 
        (e.g., ['.csv', '.txt']) to match.

    Returns:
        tuple: A tuple containing:
            - file_paths (list): A list of full file paths for the matching files.
            - file_names (list): A list of file names for the matching files.
    """
    file_paths = []
    file_names = []
    for file_name in os.listdir(source):
        if any(file_name.endswith(ext) for ext in file_type):
            file_paths.append(os.path.join(source, file_name))
            file_names.append(file_name)
    return file_paths, file_names


def find_dir(path):
    """
    Check if the specified path is a directory.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a directory, False otherwise.
    """
    return os.path.isdir(path)


def find_file(path):
    """
    Check if the specified path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return os.path.isfile(path)


def check_directory(path):
    """
    Verify that the given path is a directory.

    Args:
        path (str): The path to verify.

    Returns:
        bool: True if the path is a directory, False otherwise.
    """
    return find_dir(path)


def check_file(path):
    """
    Verify that the given path is a file.

    Args:
        path (str): The path to verify.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return find_file(path)

def check_str_is_file(path):
    """
    """
    if check_file(path):
        return True
    if '.' in path or check_directory(path):
        return False
    return True


def create_directory(path):
    """
    Create a directory at the specified path if it does not already exist.

    Args:
        path (str): The directory path to create.

    Raises:
        Exception: If an error occurs during directory creation.
    """
    try:
        if not check_directory(path):
            os.mkdir(path)
        return
    except Exception as e:
        raise FileNotFoundError("Error creating directory: " + e) from e


def create_file(path):
    """
    Create an empty file at the specified path if it does not already exist.

    Args:
        path (str): The file path to create.

    Raises:
        Exception: If an error occurs during file creation.
    """
    try:
        if not check_file(path):
            with open(path, 'w', encoding="utf-8"):
                pass
        return
    except Exception as e:
        raise FileNotFoundError("Error creating file: " + e) from e


def split_last_delimiter(value, delimiter='.'):
    """
    Split a string by the last occurrence of the specified delimiter.

    Args:
        value (str): The string to split.
        delimiter (str, optional): The delimiter on which to split the string.
                                   Defaults to '.'.

    Returns:
        list: A list of substrings resulting from the split. 
              Typically, this will be a list with two elements,
              where the first element is the part of the string before the last delimiter.
    """
    return value.rsplit(delimiter, 1)


def remove_extension(filename):
    """
    Remove the file extension from a filename.

    Args:
        filename (str): The filename from which to remove the extension.

    Returns:
        str: The filename without its extension.
    """
    return split_last_delimiter(filename)[0]
