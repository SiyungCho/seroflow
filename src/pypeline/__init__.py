"""
Package: Pypeline
Version: 1.0.0

This package provides a comprehensive toolkit for building and managing ETL (Extract, Transform, Load)
pypelines. It encompasses a wide range of modules and classes to support the various stages of data
processing, including caching, chunking, context management, data extraction, loading, transformation,
and logging. The design emphasizes modularity, flexibility, and robustness, enabling developers to
easily construct scalable data workflows.

Key Components:
    - Cache: Implements caching mechanisms to store intermediate pypeline states.
        AbstractCache, LFUCache
    - Chunker: Provides strategies for partitioning large tasks.
        Chunker, DirectChunker, DistributedChunker
    - Context: Manages shared data and dataframes across the pypeline through the Context class.
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
    - Step: Defines the structure for pypeline steps to encapsulate individual processing tasks.
        AbstractStep, Step
    - Transform: Includes a diverse set of transformation utilities to process and modify data.
        Many...
    - Types: Offers type-checking utilities.
    - Utils: Provides helper functions for common tasks and operations.
    - Wrappers: Contains decorators to facilitate performance monitoring and error handling.
      (timer, log_error)

This package is designed to enable robust, error-resilient, and scalable ETL processes, supporting
a variety of use cases from simple file processing to complex, database-driven workflows.
"""

from .cache import AbstractCache
from .cache import LFUCache
from .chunker import Chunker
from .chunker import DirectChunker
from .chunker import DistributedChunker
from .context import Context
# from .engine import PyodbcEngine
from .engine import SQLAlchemyEngine
from .exceptions import CustomException
from .extract import Extractor
from .extract import MultiExtractor
from .extract import FileExtractor
from .extract import MultiFileExtractor
from .extract import CSVExtractor
from .extract import MultiCSVExtractor
from .extract import ExcelExtractor
from .extract import MultiExcelExtractor
from .extract import SQLServerExtractor
from .load import Loader
from .load import FileLoader
from .load import CSVLoader
from .load import MultiCSVLoader
from .load import ExcelLoader
from .load import MultiExcelLoader
from .load import SQLServerLoader
from .log import CustomLogger
from .step import AbstractStep
from .step import Step
from .transform import Transformation
from .transform import CacheState
from .transform import ReloadCacheState
from .transform import ResetCache
from .transform import DropColumn
from .transform import DropColumns
from .transform import ConvertColumnType
from .transform import RenameColumns
from .transform import AddColumn
from .transform import MergeColumns
from .transform import SplitColumn
from .transform import ExplodeColumn
from .transform import CreateColumnFromVariable
from .transform import AddDataFrame
from .transform import DeleteDataFrame
from .transform import RenameDataFrame
from .transform import CopyDataFrame
from .transform import TransposeDataFrame
from .transform import PivotDataFrame
from .transform import MeltDataFrame
from .transform import GroupByAggregate
from .transform import FilterRows
from .transform import SortDataFrame
from .transform import DropDuplicates
from .transform import SelectColumns
from .transform import FillNAValues
from .transform import ReplaceValues
from .transform import MergeDataFrames
from .transform import JoinDataFrames
from .transform import ApplyFunction
from .transform import ApplyMap
from .transform import MapValues
from .transform import OneHotEncode
from .transform import ConvertToDateTime
from .transform import SetIndex
from .transform import ResetIndex
from .transform import SQLQuery
from .transform import RemoveCharacterFromColumn
from .transform import RemoveCharactersFromColumn
from .transform import ReplaceStringInColumn
from .transform import CreateVariable
from .transform import UpdateVariable
from .transform import DecrementVariable
from .transform import IncrementVariable
from .transform import MultiplyVariable
from .transform import DivideVariable
from .transform import CopyVariable
from .transform import GetColMean
from .transform import GetColMedian
from .transform import GetColMode
from .transform import GetColStd
from .transform import GetColSum
from .transform import GetColVariance
from .transform import GetColQuantile
from .transform import GetColCorrelation
from .transform import GetColCovariance
from .transform import GetColSkew
from .transform import DisplayInfo
from .transform import DisplayColumns
from .transform import DisplayHead
from .transform import DisplayTail
from .transform import DisplayColumnMean
from .transform import DisplayColumnMedian
from .transform import DisplayColumnMode
from .transform import DisplayColumnVariance
from .transform import DisplayColumnStdDev
from .transform import DisplayColumnSum
from .transform import DisplayColumnMin
from .transform import DisplayColumnMax
from .transform import DisplayColumnCount
from .transform import DisplayColumnUnique
from .transform import DisplayColumnNUnique
from .transform import DisplayColumnDType
from .transform import DisplayStringCount
from .transform import DisplayMostFrequentString
from .transform import DisplayAllCategories
from .transform import DisplaySubstringOccurrence
from .types import is_extractor
from .types import is_multiextractor
from .types import is_loader
from .types import is_step
from .types import is_context
from .types import is_context_object
from .utils import generate_key
from .utils import check_kw_in_kwargs
from .utils import filter_kwargs
from .utils import _convert_ast_node_to_python
from .utils import get_return_elements
from .utils import gather_files
from .utils import find_dir
from .utils import find_file
from .utils import check_directory
from .utils import check_file
from .utils import create_directory
from .utils import create_file
from .utils import split_last_delimiter
from .utils import remove_extension
from .utils import check_str_is_file
from .wrappers import timer
from .wrappers import log_error

__version__ = "1.0.0"
