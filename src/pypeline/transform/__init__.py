"""
Module: transform

This module implements a suite of predefined data transformation operations.
It defines a wide range of data transformation tasks including:

    - Base Transformation (Base class for creating predefined transformation steps):
        * Transformation
    - Cache Management (Classes to manage and revert cache states during transformations):
        * CacheState, ReloadCacheState, ResetCache
    - Column Operations (Functions to modify and manage dataframe columns):
        * DropColumn, DropColumns, ConvertColumnType,
          RenameColumns, AddColumn, MergeColumns,
          SplitColumn, ExplodeColumn, CreateColumnFromVariable
    - DataFrame Internal Operations (Functions to manage dataframes within a context):
        * AddDataFrame, DeleteDataFrame, RenameDataFrame, CopyDataFrame
    - Advanced DataFrame Manipulations (Functions for in-depth dataframe restructuring and cleaning):
        * TransposeDataFrame, PivotDataFrame, MeltDataFrame,
          GroupByAggregate, FilterRows, SortDataFrame,
          DropDuplicates, SelectColumns, FillNAValues, 
          ReplaceValues, MergeDataFrames, JoinDataFrames,
          ApplyFunction, ApplyMap, MapValues, OneHotEncode
    - Date and Time Conversions (Utility for converting columns to datetime objects):
        * ConvertToDateTime
    - Display Utilities (Functions for summarizing and visualizing dataframe contents):
        * DisplayInfo, DisplayColumns, DisplayHead,
          DisplayTail, DisplayColumnMean, DisplayColumnMedian,
          DisplayColumnMode, DisplayColumnVariance, DisplayColumnStdDev,
          DisplayColumnSum, DisplayColumnMin, DisplayColumnMax,
          DisplayColumnCount, DisplayColumnUnique, DisplayColumnNUnique,
          DisplayColumnDType, DisplayStringCount, DisplayMostFrequentString,
          DisplayAllCategories, DisplaySubstringOccurrence
    - Indexing Operations (Utilities to modify dataframe indices):
        * SetIndex, ResetIndex
    - SQL Integration (Class to execute SQL-based transformations on data):
        * SQLQuery
    - String Manipulations (Functions to handle text cleaning in columns):
        * RemoveCharacterFromColumn, RemoveCharactersFromColumn, ReplaceStringInColumn
    - Variable Operations (Functions to create and manipulate pypeline variables):
        * CreateVariable, UpdateVariable, DecrementVariable, 
          IncrementVariable, MultiplyVariable, DivideVariable, CopyVariable
    - Aggregation Functions (Statistical functions to aggregate and summarize data):
        * GetColMean, GetColMedian, GetColMode,
          GetColStd, GetColSum, GetColVariance,
          GetColQuantile, GetColCorrelation, GetColCovariance, GetColSkew

The module is designed to be extensible and integrative, allowing for flexible pypeline construction
and effective data manipulation.
"""
from .transformation import Transformation
from .cache import CacheState
from .cache import ReloadCacheState
from .cache import ResetCache
from .column import DropColumn
from .column import DropColumns
from .column import ConvertColumnType
from .column import RenameColumns
from .column import AddColumn
from .column import MergeColumns
from .column import SplitColumn
from .column import ExplodeColumn
from .column import CreateColumnFromVariable
from .internal import AddDataFrame
from .internal import DeleteDataFrame
from .internal import RenameDataFrame
from .internal import CopyDataFrame
from .dataframe import TransposeDataFrame
from .dataframe import PivotDataFrame
from .dataframe import MeltDataFrame
from .dataframe import GroupByAggregate
from .dataframe import FilterRows
from .dataframe import SortDataFrame
from .dataframe import DropDuplicates
from .dataframe import SelectColumns
from .dataframe import FillNAValues
from .dataframe import ReplaceValues
from .dataframe import MergeDataFrames
from .dataframe import JoinDataFrames
from .dataframe import ApplyFunction
from .dataframe import ApplyMap
from .dataframe import MapValues
from .dataframe import OneHotEncode
from .date import ConvertToDateTime
from .display import DisplayInfo
from .display import DisplayColumns
from .display import DisplayHead
from .display import DisplayTail
from .display import DisplayColumnMean
from .display import DisplayColumnMedian
from .display import DisplayColumnMode
from .display import DisplayColumnVariance
from .display import DisplayColumnStdDev
from .display import DisplayColumnSum
from .display import DisplayColumnMin
from .display import DisplayColumnMax
from .display import DisplayColumnCount
from .display import DisplayColumnUnique
from .display import DisplayColumnNUnique
from .display import DisplayColumnDType
from .display import DisplayStringCount
from .display import DisplayMostFrequentString
from .display import DisplayAllCategories
from .display import DisplaySubstringOccurrence
from .index import SetIndex
from .index import ResetIndex
from .sql import SQLQuery
from .string import RemoveCharacterFromColumn
from .string import RemoveCharactersFromColumn
from .string import ReplaceStringInColumn
from .variable import CreateVariable
from .variable import UpdateVariable
from .variable import DecrementVariable
from .variable import IncrementVariable
from .variable import MultiplyVariable
from .variable import DivideVariable
from .variable import CopyVariable
from .aggregation import GetColMean
from .aggregation import GetColMedian
from .aggregation import GetColMode
from .aggregation import GetColStd
from .aggregation import GetColSum
from .aggregation import GetColVariance
from .aggregation import GetColQuantile
from .aggregation import GetColCorrelation
from .aggregation import GetColCovariance
from .aggregation import GetColSkew
