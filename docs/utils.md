# Utils Documentation

The `utils.py` module provides a set of utility functions for various common operations. These include generating hash keys, retrieving and hashing function source code, dictionary filtering, AST node conversion, extracting function return elements, file gathering, file/directory checks and creation, and string manipulation functions.

## Overview

The module contains functions for:

- **Hashing & Source Code Operations:**  
  Generate unique keys from strings, retrieve function source code, and compute source code hashes.

- **Dictionary Utilities:**  
  Check for keyword presence in dictionaries and filter out specified keys.

- **AST & Return Value Extraction:**  
  Convert AST nodes to Python objects and extract return elements from function source code.

- **File Gathering & File System Operations:**  
  Collect files based on file extensions, check for the existence of directories/files, create directories/files, and perform basic file path manipulations.

## Functions

### Hashing & Source Code Functions

#### `generate_key(input_string)`
Generates a unique MD5 hash key from the provided input string.

- **Arguments:**
  - `input_string` (*str*): The string to be hashed.
- **Returns:**
  - *str*: The MD5 hash in hexadecimal format.

---

#### `get_function_source(func)`
Retrieves the source code of a given function.

- **Arguments:**
  - `func` (*function*): The function whose source code will be retrieved.
- **Returns:**
  - *str*: The source code of the function.

---

#### `hash_source(source)`
Generates a SHA-256 hash for the given source code string.

- **Arguments:**
  - `source` (*str*): The source code to hash.
- **Returns:**
  - *str*: The SHA-256 hash in hexadecimal format.

---

#### `get_function_hash(func)`
Retrieves the source code of a function and computes its SHA-256 hash.

- **Arguments:**
  - `func` (*function*): The function to hash.
- **Returns:**
  - *tuple*: A tuple containing:
    - The source code (*str*) of the function.
    - The SHA-256 hash (*str*) of the source code.

---

### Dictionary Utility Functions

#### `check_kw_in_kwargs(kw, kwargs)`
Checks if a given keyword is missing from a dictionary of keyword arguments.

- **Arguments:**
  - `kw` (*str*): The keyword to search for.
  - `kwargs` (*dict*): The dictionary of keyword arguments.
- **Returns:**
  - *bool*: `True` if the keyword is **not** present; otherwise, `False`.

---

#### `filter_kwargs(kwargs, keys_to_remove)`
Filters out specified keys from a dictionary of keyword arguments.

- **Arguments:**
  - `kwargs` (*dict*): The original dictionary.
  - `keys_to_remove` (*iterable*): An iterable of keys to be removed.
- **Returns:**
  - *dict*: A new dictionary with the specified keys removed.

---

### AST & Return Value Functions

#### `_convert_ast_node_to_python(node)`
Converts an AST node to its corresponding Python object representation (e.g., converts an `ast.Name` to its identifier or an `ast.Constant` to its value).  
*Note: This is an internal helper function.*

- **Arguments:**
  - `node` (*ast.AST*): The AST node to convert.
- **Returns:**
  - The Python representation of the node or `None` if unsupported.

---

#### `get_return_elements(func)`
Extracts the elements of the return statement from a function’s source code using AST parsing.

- **Arguments:**
  - `func` (*function*): The function from which to extract return elements.
- **Returns:**
  - *list*: A list of elements extracted from the return statement. Returns an empty list if no return statement or elements are found.

---

### File Gathering Functions

#### `gather_files(source, file_type)`
Gathers files from a specified directory that match given file extensions.

- **Arguments:**
  - `source` (*str*): The directory path to search.
  - `file_type` (*iterable*): An iterable of file extension strings (e.g., `['.csv', '.txt']`).
- **Returns:**
  - *tuple*: A tuple containing:
    - A list of full file paths for the matching files.
    - A list of file names for the matching files.
  
---

### File/Directory Checking Functions

#### `find_dir(path)`
Checks if the specified path is a directory.

- **Arguments:**
  - `path` (*str*): The path to check.
- **Returns:**
  - *bool*: `True` if the path is a directory; otherwise, `False`.

---

#### `find_file(path)`
Checks if the specified path is a file.

- **Arguments:**
  - `path` (*str*): The path to check.
- **Returns:**
  - *bool*: `True` if the path is a file; otherwise, `False`.

---

#### `check_directory(path)`
Verifies that the given path is a directory.

- **Arguments:**
  - `path` (*str*): The directory path to verify.
- **Returns:**
  - *bool*: `True` if the path is a directory; otherwise, `False`.

---

#### `check_file(path)`
Verifies that the given path is a file.

- **Arguments:**
  - `path` (*str*): The file path to verify.
- **Returns:**
  - *bool*: `True` if the path is a file; otherwise, `False`.

---

#### `check_str_is_file(path)`
Determines whether the given string represents a file.  
If the string contains a dot (`.`) or corresponds to an existing directory, it is treated as not being a file.

- **Arguments:**
  - `path` (*str*): The string to check.
- **Returns:**
  - *bool*: `True` if the string represents a file; otherwise, `False`.

### File/Directory Creation Functions

#### `create_directory(path)`
Creates a directory at the specified path if it does not already exist.

- **Arguments:**
  - `path` (*str*): The directory path to create.
- **Raises:**
  - *FileNotFoundError*: If an error occurs during directory creation.

---

#### `create_file(path)`
Creates an empty file at the specified path if it does not already exist.

- **Arguments:**
  - `path` (*str*): The file path to create.
- **Raises:**
  - *FileNotFoundError*: If an error occurs during file creation.

### String Processing Functions

#### `split_last_delimiter(value, delimiter='.')`
Splits a string by the last occurrence of the specified delimiter.

- **Arguments:**
  - `value` (*str*): The string to split.
  - `delimiter` (*str*, optional): The delimiter to use for splitting. Defaults to `'.'`.
- **Returns:**
  - *list*: A list of substrings. Typically, this returns a list with two elements, where the first element is the part before the last delimiter.

---

#### `remove_extension(filename)`
Removes the file extension from a filename.

- **Arguments:**
  - `filename` (*str*): The filename from which to remove the extension.
- **Returns:**
  - *str*: The filename without its extension.

## Usage Example

Below is a simple usage example that demonstrates some of the utilities provided by the module:

```python
from utils import (
    generate_key,
    get_function_source,
    get_function_hash,
    filter_kwargs,
    gather_files,
    create_directory,
    remove_extension,
)

# Generate a unique key for a string.
key = generate_key("example_string")
print("Generated key:", key)

# Retrieve function source and hash.
def sample_function():
    return 1, 2

source, code_hash = get_function_hash(sample_function)
print("Function source:\n", source)
print("Function hash:", code_hash)

# Filter dictionary keys.
original_kwargs = {'a': 1, 'b': 2, 'c': 3}
filtered = filter_kwargs(original_kwargs, keys_to_remove=['b'])
print("Filtered kwargs:", filtered)

# Gather .txt files from a directory.
file_paths, file_names = gather_files("./data", file_type=['.txt'])
print("File paths:", file_paths)
print("File names:", file_names)

# Create a new directory.
create_directory("./new_folder")

# Remove file extension.
name_without_ext = remove_extension("document.pdf")
print("Filename without extension:", name_without_ext)
```