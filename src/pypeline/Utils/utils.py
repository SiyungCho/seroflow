import os
import inspect
import ast
import textwrap
import uuid
import hashlib
import json

def generate_key(input_string):
    return hashlib.md5(input_string.encode('utf-8')).hexdigest()

def get_function_source(func):
    return inspect.getsource(func)

def hash_source(source):
    return hashlib.sha256(source.encode('utf-8')).hexdigest()

def get_function_hash(func):
    source_code = get_function_source(func)
    code_hash = hash_source(source_code)
    return source_code, code_hash

def check_kw_in_kwargs(kw, kwargs):
    return False if kw not in kwargs else True

def filter_kwargs(kwargs, keys_to_remove):
    return {key: value for key, value in kwargs.items() if key not in keys_to_remove}

def _convert_ast_node_to_python(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant):
        return node.value
    else:
        return None
    
def get_return_elements(func):
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
    file_paths = []
    file_names = []
    for file_name in os.listdir(source):
        if any(file_name.endswith(ext) for ext in file_type):
            file_paths.append(os.path.join(source, file_name))
            file_names.append(file_name)
    return file_paths, file_names

def find_dir(path):
    return os.path.isdir(path)

def find_file(path):
    return os.path.isfile(path)

def check_directory(path):
    return True if find_dir(path) else False

def check_file(path):
    return True if find_file(path) else False

def create_directory(path):
    try:
        if not check_directory(path):
            os.mkdir(path)
        return
    except Exception as e:
        raise Exception("Error creating directory")
    
def create_file(path):
    try:
        if not check_file(path):
            with open(path, 'w') as fp:
                pass
        return
    except Exception as e:
        raise Exception("Error creating file")
    
def split_last_delimiter(value, delimiter = '.'):
    return value.rsplit(delimiter, 1)

def remove_extension(filename):
    return split_last_delimiter(filename)[0]