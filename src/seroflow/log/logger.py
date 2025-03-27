"""
Module for custom logging.

This module defines the CustomLogger class, which sets up a logging mechanism for an
application. It creates log directories, configures logging to write to a file with a timestamp.
Provides a logger instance.
"""

import os
import logging
import datetime
from ..utils.utils import create_directory

class CustomLogger():
    """
    Custom logger for managing application logs.

    The CustomLogger class configures the Python logging module to write log messages to a file.
    If no log file path is provided, it creates a log directory structure 
    based on the current working directory and the process ID, and generates 
    a log file name that includes the log name and a timestamp.
    """

    def __init__(self, log_name, log_file_path=None):
        """
        Initialize a CustomLogger instance.

        This method sets up the log file path and configures the logging module with the
        appropriate file mode, filename, log format, and logging level. 
        If log_file_path is not provided, a default log directory is created.

        Args:
            log_name (str): The name to be used in the log file name.
            log_file_path (str, optional): The full path to the log file. If None, 
                                           a default directory structure is created. 
                                           Defaults to None.
        """
        self.log_name = log_name
        self.__pid = os.getpid()
        self.__source_directory = os.path.abspath(os.getcwd())
        self.__log_file_path = self.init_directory() if log_file_path is None else log_file_path

        logging.basicConfig(
            filemode='a',
            filename=self.__log_file_path,
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger()

    def init_directory(self):
        """
        Initialize and return the log file path.

        Creates a "logs" directory in the current working directory
        and a subdirectory named after the current process ID.
        Constructs a log file name using the log name
        and the current date and time.

        Returns:
            str: The full path to the generated log file.
        """
        log_directory_path = os.path.join(self.__source_directory, "logs")
        create_directory(log_directory_path)
        active_directory_path = os.path.join(log_directory_path, str(self.__pid))
        create_directory(active_directory_path)
        log_file_path = os.path.join(
            active_directory_path,
            "{log_name}_{date:%Y_%m_%d_%H_%M_%S}.log".format(
                log_name=self.log_name, date=datetime.datetime.now()
            )
        )
        return log_file_path
