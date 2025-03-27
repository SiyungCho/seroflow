"""
Module: load

This module provides the loader functionalities. It defines classes responsible
for loading data into target destinations from various sources. 
The module includes a base Loader class along with several specialized loaders 
for different file formats and database systems, such as CSV, Excel, and SQL Server.
Any custom Loader class should inherit from the base Loader class and implement the
required loading logic for the specific data source.

Key Components:
    - Loader: The base loader class that defines the common interface for all data loaders.
    - FileLoader: Implements loading functionality for generic file-based data sources.
    - CSVLoader & MultiCSVLoader: Specialized loaders for handling CSV files.
    - ExcelLoader & MultiExcelLoader: Specialized loaders for handling Excel files.
    - SQLServerLoader: Loader implementation for loading data into SQL Server databases.
"""
from .loader import Loader
from .file_loader import FileLoader
from .csv_loader import CSVLoader
from .csv_loader import MultiCSVLoader
from .excel_loader import ExcelLoader
from .excel_loader import MultiExcelLoader
from .sqlserver_loader import SQLServerLoader
from .odbc_loader import ODBCLoader
