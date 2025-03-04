import os
import logging
import datetime
from Utils.utils import *

class custom_logger():
    def __init__(self, log_name, log_file_path = None):
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
        log_directory_path = os.path.join(self.__source_directory, "logs")
        create_directory(log_directory_path)
        active_directory_path = os.path.join(log_directory_path, str(self.__pid))
        create_directory(active_directory_path)
        log_file_path = os.path.join(active_directory_path, "{log_name}_{date:%Y_%m_%d_%H_%M_%S}.log".format(log_name = self.log_name, date = datetime.datetime.now()))
        return log_file_path