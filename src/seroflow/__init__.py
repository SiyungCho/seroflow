"""
Package: Seroflow
Version: 1.0.0

This package provides a comprehensive toolkit for building and managing data pipelines
It encompasses a wide range of modules and classes to support the various stages of data processing,
including caching, chunking, context management, data extraction, loading, transforming and logging.
The design emphasizes modularity, flexibility, and robustness, enabling developers to easily
construct scalable data workflows.

Key Components:
    - Cache: Implements caching mechanisms to store intermediate Pipeline states.
        AbstractCache, LFUCache
    - Chunker: Provides strategies for partitioning large tasks.
        Chunker, DirectChunker, DistributedChunker
    - Context: Manages shared data and dataframes across the Pipeline through the Context class.
    - Engine: Supports database connectivity and operations using engines.
        SQLAlchemyEngine, PyodbcEngine, UniversalEngine(WIP)
    - Exceptions: Defines custom exceptions for improved error handling.
        CustomException(WIP)
    - Extract: Offers various extractor classes to facilitate data ingestion from multiple sources.
        Extractor, MultiExtractor, FileExtractor, CSVExtractor, ExcelExtractor, SQLServerExtractor
    - Load: Contains loader classes for loading data into target systems.
        (Loader, FileLoader, CSVLoader, ExcelLoader, SQLServerLoader, etc.)
    - Log: Provides a customizable logging solution.
        CustomLogger
    - Step: Defines the structure for Pipeline steps to encapsulate individual processing tasks.
        AbstractStep, Step
    - Transform: Includes a diverse set of transformation utilities to process and modify data.
        Many...
    - Types: Offers type-checking utilities.
    - Utils: Provides helper functions for common tasks and operations.
    - Wrappers: Contains decorators to facilitate performance monitoring and error handling.
      (timer, log_error)

This package is designed to enable robust, error-resilient, and scalable data pipeline processes,
supporting a variety of use cases from simple file processing to complex, database-driven workflows.
"""

from .seroflow import Pipeline
from .cache.cache import AbstractCache
from .cache.lfu_cache import LFUCache
from .chunker.chunker import Chunker
from .chunker.direct_chunker import DirectChunker
from .chunker.distributed_chunker import DistributedChunker
from .context.context import Context
from .engine.engine import AbstractEngine
from .engine.engine import Engine
from .engine.sqlalchemy_engine import SQLAlchemyEngine
from .exceptions.exception import CustomException
from .extract.extractor import Extractor
from .extract.extractor import MultiExtractor
from .extract.file_extractor import FileExtractor
from .extract.file_extractor import MultiFileExtractor
from .extract.csv_extractor import CSVExtractor
from .extract.csv_extractor import MultiCSVExtractor
from .extract.excel_extractor import ExcelExtractor
from .extract.excel_extractor import MultiExcelExtractor
from .extract.sqlserver_extractor import SQLServerExtractor
from .extract.odbc_extractor import ODBCExtractor
from .load.loader import Loader
from .load.file_loader import FileLoader
from .load.csv_loader import CSVLoader
from .load.csv_loader import MultiCSVLoader
from .load.excel_loader import ExcelLoader
from .load.excel_loader import MultiExcelLoader
from .load.sqlserver_loader import SQLServerLoader
from .load.odbc_loader import ODBCLoader
from .log.logger import CustomLogger
from .step.base_step import AbstractStep
from .step.step import Step
from .transform.transformation import Transformation
from .transform.cache import CacheState
from .transform.cache import ReloadCacheState
from .transform.cache import ResetCache
from .transform.column import DropColumn
from .transform.column import DropColumns
from .transform.column import ConvertColumnType
from .transform.column import RenameColumns
from .transform.column import AddColumn
from .transform.column import MergeColumns
from .transform.column import SplitColumn
from .transform.column import ExplodeColumn
from .transform.column import CreateColumnFromVariable
from .transform.internal import AddDataFrame
from .transform.internal import DeleteDataFrame
from .transform.internal import RenameDataFrame
from .transform.internal import CopyDataFrame
from .transform.dataframe import TransposeDataFrame
from .transform.dataframe import PivotDataFrame
from .transform.dataframe import MeltDataFrame
from .transform.dataframe import GroupByAggregate
from .transform.dataframe import FilterRows
from .transform.dataframe import SortDataFrame
from .transform.dataframe import DropDuplicates
from .transform.dataframe import SelectColumns
from .transform.dataframe import FillNAValues
from .transform.dataframe import ReplaceValues
from .transform.dataframe import MergeDataFrames
from .transform.dataframe import JoinDataFrames
from .transform.dataframe import ApplyFunction
from .transform.dataframe import ApplyMap
from .transform.dataframe import MapValues
from .transform.dataframe import OneHotEncode
from .transform.date import ConvertToDateTime
from .transform.index import SetIndex
from .transform.index import ResetIndex
from .transform.sql import SQLQuery
from .transform.string import RemoveCharacterFromColumn
from .transform.string import RemoveCharactersFromColumn
from .transform.string import ReplaceStringInColumn
from .transform.variable import CreateVariable
from .transform.variable import UpdateVariable
from .transform.variable import DecrementVariable
from .transform.variable import IncrementVariable
from .transform.variable import MultiplyVariable
from .transform.variable import DivideVariable
from .transform.variable import CopyVariable
from .transform.aggregation import GetColMean
from .transform.aggregation import GetColMedian
from .transform.aggregation import GetColMode
from .transform.aggregation import GetColStd
from .transform.aggregation import GetColSum
from .transform.aggregation import GetColVariance
from .transform.aggregation import GetColQuantile
from .transform.aggregation import GetColCorrelation
from .transform.aggregation import GetColCovariance
from .transform.aggregation import GetColSkew
from .transform.display import DisplayInfo
from .transform.display import DisplayColumns
from .transform.display import DisplayHead
from .transform.display import DisplayTail
from .transform.display import DisplayColumnMean
from .transform.display import DisplayColumnMedian
from .transform.display import DisplayColumnMode
from .transform.display import DisplayColumnVariance
from .transform.display import DisplayColumnStdDev
from .transform.display import DisplayColumnSum
from .transform.display import DisplayColumnMin
from .transform.display import DisplayColumnMax
from .transform.display import DisplayColumnCount
from .transform.display import DisplayColumnUnique
from .transform.display import DisplayColumnNUnique
from .transform.display import DisplayColumnDType
from .transform.display import DisplayStringCount
from .transform.display import DisplayMostFrequentString
from .transform.display import DisplayAllCategories
from .transform.display import DisplaySubstringOccurrence
from .types.type_validation import is_extractor
from .types.type_validation import is_multiextractor
from .types.type_validation import is_loader
from .types.type_validation import is_step
from .types.type_validation import is_context
from .types.type_validation import is_context_object
from .utils.utils import generate_key
from .utils.utils import check_kw_in_kwargs
from .utils.utils import filter_kwargs
from .utils.utils import _convert_ast_node_to_python
from .utils.utils import get_return_elements
from .utils.utils import gather_files
from .utils.utils import find_dir
from .utils.utils import find_file
from .utils.utils import check_directory
from .utils.utils import check_file
from .utils.utils import create_directory
from .utils.utils import create_file
from .utils.utils import split_last_delimiter
from .utils.utils import remove_extension
from .utils.utils import check_str_is_file
from .wrappers.wrappers import timer
from .wrappers.wrappers import log_error

__version__ = "1.0.0"
