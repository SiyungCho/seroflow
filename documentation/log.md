# Custom Logging Module Documentation

This module defines the `CustomLogger` class, which sets up a logging mechanism for an application. It creates log directories, configures logging to write to a file with a timestamp, and provides a logger instance.

---

## Overview

The `CustomLogger` class configures the Python logging module to write log messages to a file. If no log file path is provided, it creates a default log directory structure based on the current working directory and the process ID, and generates a log file name that includes the log name and a timestamp.

---

## Class: CustomLogger

### Description

The `CustomLogger` class is designed to manage application logs. It handles the following tasks:

- **Directory Initialization:**  
  Creates a `logs` directory in the current working directory, then creates a subdirectory for the current process ID, and finally constructs a log file name that includes a timestamp.

- **Logging Configuration:**  
  Configures the logging module to write log messages to the specified log file with a defined format and logging level (set to `INFO`).

### Methods

#### `__init__(self, log_name, log_file_path=None)`

Initializes a `CustomLogger` instance.

- **Arguments:**
  - `log_name` (*str*): The name to be used in the log file name.
  - `log_file_path` (*str*, optional): The full path to the log file. If `None`, a default directory structure is created. Defaults to `None`.

- **Behavior:**
  - Determines the current process ID and source directory.
  - If no `log_file_path` is provided, calls `init_directory()` to create a log directory and file.
  - Configures the logging module with:
    - File mode: append (`'a'`)
    - Filename: the log file path
    - Format: `'%(asctime)s - %(levelname)s - %(message)s'`
    - Logging level: `INFO`
  - Retrieves and stores a logger instance from the logging module.

---

#### `init_directory(self)`

Initializes and returns the log file path.

- **Behavior:**
  - Creates a `logs` directory in the current working directory.
  - Creates a subdirectory named after the current process ID.
  - Constructs a log file name using the provided `log_name` and the current date and time in the format `%Y_%m_%d_%H_%M_%S`.
  - Returns the full path to the generated log file.

- **Returns:**
  - *str*: The full path to the generated log file.

---

## Usage Example

Below is an example demonstrating how to use the `CustomLogger` class:

```python
from custom_logging import CustomLogger

# Initialize a CustomLogger instance with a custom log name.
logger_instance = CustomLogger(log_name="my_app")

# Use the provided logger to log messages.
logger_instance.logger.info("This is an informational message.")
logger_instance.logger.error("This is an error message.")