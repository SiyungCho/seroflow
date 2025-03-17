"""
Module: extract

This module implements the extractor functionalities. It provides a set of 
extractor classes that are designed to retrieve data from various sources. 
These include the base Extractor class and specialized extractors for 
handling file-based data, CSV files, Excel files, and SQL Server databases. 
The module also supports handling multiple extractors simultaneously through the MultiExtractor 
variants.
Any custom Extractor class should inherit from the base Extractor class and implement the
required extraction logic for the specific data source.

Key Components:
    - Extractor: Base class defining the common interface for data extraction.
    - MultiExtractor: Supports combining multiple extractor instances.
    - FileExtractor & MultiFileExtractor: Extractors for handling generic file-based data sources.
    - CSVExtractor & MultiCSVExtractor: Specialized extractors for retrieving data from CSV files.
    - ExcelExtractor & MultiExcelExtractor: Specialized extractors for retrieving data from Excel files.
    - SQLServerExtractor: Extractor for connecting to and extracting data from SQL Server databases.

These extractor classes facilitate robust and flexible data ingestion into the pipeline, ensuring seamless 
integration with various data sources.
"""

from .extractor import Extractor
from .extractor import MultiExtractor
from .file_extractor import FileExtractor
from .file_extractor import MultiFileExtractor
from .csv_extractor import CSVExtractor
from .csv_extractor import MultiCSVExtractor
from .excel_extractor import ExcelExtractor
from .excel_extractor import MultiExcelExtractor
from .sqlserver_extractor import SQLServerExtractor
