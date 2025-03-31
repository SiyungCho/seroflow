Logging
====================

This module defines the ``CustomLogger`` class, which sets up a logging mechanism for an application.
It creates log directories, configures logging to write to a file with a timestamp, and provides a logger instance.

**It is important to note** that ``Seroflow`` does not require the use of this ``CustomLogger`` class, any ``Python`` logging module can be used to log messages as long as it derives from ``Python`` ``logging.logger``.
``Seroflow`` offers an interface and concrete example of a compatible ``CustomLogger`` for abstraction and validity however it is **not** mandatory to use these unless specified. 

Overview
---------------------------------

The ``CustomLogger`` class configures the Python logging module to write log messages to a file.
If no log file path is provided, it creates a default log directory structure based on the current working directory and the process ID, and generates a log file name that includes the log name and a timestamp.

CustomLogger
--------------------------

The ``CustomLogger`` class is designed to manage application logs. It handles the following tasks:

- **Directory Initialization:**  
  Creates a ``logs`` directory in the current working directory, then creates a subdirectory for the current process ID, and finally constructs a log file name that includes a timestamp.

- **Logging Configuration:**  
  Configures the logging module to write log messages to the specified log file with a defined format and logging level (set to ``INFO``).

.. autoclass:: seroflow.log.logger.CustomLogger
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how to use the ``CustomLogger`` class: ::

   from seroflow.log import CustomLogger

   # Initialize a CustomLogger instance with a custom log name.
   logger_instance = CustomLogger(log_name="my_app")

   # Use the provided logger to log messages.
   logger_instance.logger.info("This is an informational message.")
   logger_instance.logger.error("This is an error message.")
