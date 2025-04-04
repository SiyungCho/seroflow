# Extractor Documentation

The modules documented here define the base structure and concrete implementations for `Extractor` steps. These extractors are responsible for reading data from various sources—such as files (CSV, Excel) and SQL Server tables—and adding the resulting pandas DataFrames to the `Pipeline` context. The extractors support both full reads and chunked reads, as well as error handling and row count estimation.

## Overview

This documentation covers:

- **Extractor**: Abstract class, which specifies the interface for creating a single extractor.
- **MultiExtractor**: A concrete class that aggregates multiple extractor instances to handle multiple sources in a single step.
- **FileExtractor**: Abstract class, which specifies the interface for creating a single extractor, specifically for File data sources.
- **MultiFileExtractor**: A concrete class extending MultiExtractor that gathers file paths from a directory (based on extension) and creates extractor instances for each file.
- **CSVExtractor**: Single CSV File data extractor. Extracts data within a single CSV File.
- **MultiCSVExtractor**: Multi CSV File data extractor. Extracts data from multiple CSV Files given a directory path.
- **ExcelExtractor**: Single Excel File data extractor. Extracts data within a single Excel File.
- **MultiExcelExtractor**: Multi Excel File data extractor. Extracts data from multiple Excel Files given a directory path.
- **SQLServerExtractor**: Single SQL Server Table data extractor. Extracts data within a single SQL Server Table.
- **ODBCExtractor**: Single ODBC Source Table data extractor. Extracts data within a single ODBC Source Table.

## Class: Extractor

The `Extractor` class is an abstract base class that provides the common structure for all data extractors. It defines the general interface and common behaviors such as handling chunk sizes and managing the step lifecycle (e.g., start and stop).

**Subclasses must override:**
- `func(self, context)`: Implements the logic to read the data source and add the resulting DataFrame to the provided context.
- `get_max_row_count(self)`: Returns the total number of rows in the source, which is needed for determining the extent of data for full or chunked reads.

## Initialization

- **`__init__(step_name, func, on_error, chunk_size=None)`**  
  Initializes a new `Extractor` instance.
  
  **Parameters:**
  
  - `step_name` *(str)*: 
    - Name of the Extractor Step.
  - `func` *(function)*: 
    - The function that performs the extraction and adds the DataFrame to the context.
  - `on_error` *("raises", "ignore")*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `Extractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.

- **`func(self, context)`**  
  *Abstract Method*  
  Must be implemented by subclasses to read the data source and add the DataFrame to the `Pipeline` context.

  **Parameters:**
  context (Context): A blank context object to which the DataFrame will be added.
  
  **Returns:**
  Context: The updated context object containing the extracted DataFrame.

- **`get_max_row_count`**  
  *Abstract Method*  
  Must be implemented by subclasses to return the number of rows present in the data source.

  **Returns:**
  int: The total row count of the data source.

#### Usage Example

Below is an example demonstrating how a concrete extract implementation might inherit from `Extractor` and implement its methods:

```python
  from seroflow import Pipeline
  from seroflow.extract import Extractor

  class MyCustomExtractor(Extractor):
      def __init__(self, source, chunk_size=None, **kwargs):
          super().__init__(step_name="MyCustomExtractor", func=self.func, on_error="raises", chunk_size=chunk_size)
          self.source = source

      def func(self, context):
          df = ...  # Obtain a pandas DataFrame here
          context.add_dataframe("custom", df)
          return context

      def get_max_row_count(self):
          num_rows = ... # Custom logic to determine the number of rows
          return num_rows

  pipeline = Pipeline(...)
  custom_extractor = MyCustomExtractor(...)
  pipeline.target_extractor = custom_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Class: FileExtractor

The `FileExtractor` class extends `Extractor` and provides a template for file-based data sources. In addition to the standard `Extractor` functionality, it validates the file’s existence, extracts the file name without its extension, and stores additional keyword arguments for the file reading operation.

**Subclasses must override:**
- `func(self, context)`: Implements the logic to read the data source and add the resulting DataFrame to the provided context.
- `get_max_row_count(self)`: Returns the total number of rows in the source, which is useful for determining the extent of data for full or chunked reads.

## Initialization

- **`__init__(source, func, chunk_size, on_error, step_name="FileExtractor", **kwargs)`**  
  Initializes a new `FileExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - The path to the source file.
  - `step_name` *(str, optional)*: 
    - Name of the Extractor Step.
    - Default: `"FileExtractor"`
  - `func` *(function)*: 
    - The function that performs the extraction and adds the DataFrame to the context.
  - `on_error` *("raises", "ignore")*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `FileExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments for the file reading function (e.g., options for pd.read_csv()).

- **`func(self, context)`**  
  *Abstract Method*  
  Must be implemented by subclasses to read the file and add the resulting DataFrame to the context.

  **Parameters:**
  context (Context): A blank context object to which the DataFrame will be added.
  
  **Returns:**
  Context: The updated context object containing the extracted DataFrame.

- **`get_max_row_count(self)`**  
  *Abstract Method*  
  Must be implemented by subclasses to return the total number of rows in the file.

  **Returns:**
  int: The total row count of the data source.

#### Initialization Example

Below is an example demonstrating how a concrete extract implementation might inherit from `FileExtractor` and implement its methods:

```python
  from seroflow import Pipeline
  from seroflow.extract import FileExtractor

  class MyCustomFileExtractor(FileExtractor):
      def __init__(self, source, chunk_size=None, **kwargs):
          super().__init__(step_name="MyCustomFileExtractor", func=self.func, on_error="raises", chunk_size=chunk_size)
          self.source = source

      def func(self, context):
          df = ...  # Obtain a pandas DataFrame here
          context.add_dataframe("custom", df)
          return context

      def get_max_row_count(self):
          num_rows = ... # Custom logic to determine the number of rows
          return num_rows

  pipeline = Pipeline(...)
  custom_file_extractor = MyCustomFileExtractor(...)
  pipeline.target_extractor = custom_file_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Class: CSVExtractor

The `CSVExtractor` class is a concrete implementation for extracting data from a single CSV file. It leverages pandas’ read_csv() method to load the CSV file into a DataFrame and adds it to the `Pipeline` context under the file name. In addition, it provides a method for counting the total number of rows in the CSV file, which is useful for operations like chunked reading.

## Initialization

- **`source, step_name="CSVExtractor", chunk_size=None, on_error=None, **kwargs`**  
  Initializes a new `CSVExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - The path to the CSV file.
  - `step_name` *(str, optional)*: 
    - The name of the extraction step.
    - Default: `“CSVExtractor”`.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `CSVExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments for `pd.read_csv()`.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `CSVExtractor`:

```python
  from seroflow import Pipeline
  from seroflow.extract import CSVExtractor

  pipeline = Pipeline(...)
  csv_extractor = CSVExtractor(source="path_to_csv_file")
  pipeline.target_extractor = csv_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Class: MultiCSVExtractor

The `MultiCSVExtractor` class handles the extraction of data from multiple CSV files stored in a given directory. It extends the `MultiFileExtractor` and automatically gathers CSV file paths based on the specified directory. For each CSV file, it creates an instance of `CSVExtractor` to process and load the data into the `Pipeline` context.

## Initialization

- **`__init__(source, chunk_size=None, on_error=None, **kwargs)`**  
  Initializes a new `MultiCSVExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - The directory containing the CSV files.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `CSVExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments to pass to the `CSVExtractor` constructor.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `MultiCSVExtractor`:

```python
  from seroflow import Pipeline
  from seroflow.extract import MultiCSVExtractor

  pipeline = Pipeline(...)
  multi_csv_extractor = MultiCSVExtractor(source="path_to_directory", chunk_size=100)
  pipeline.target_extractor = multi_csv_extractor # Or add it using the add_step(s) methods
  pipeline.execute(chunker=...)
```

## Class: ExcelExtractor

The `ExcelExtractor` class is a concrete implementation for reading data from a single Excel file. It supports both .xls and .xlsx formats by selecting the appropriate engine (xlrd for .xls and openpyxl for .xlsx). The extractor loads the data into a DataFrame and adds it to the `Pipeline` context under the file name.

## Initialization

- **`__init__(source, step_name="ExcelExtractor", chunk_size=None, on_error=None, **kwargs)`**  
  Initializes a new `ExcelExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - The path to the Excel file.
  - `step_name` *(str, optional)*: 
    - The name of the extraction step.
    - Default: `ExcelExtractor`.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ExcelExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments for `pd.read_excel()`.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `ExcelExtractor`:

```python
  from seroflow import Pipeline
  from seroflow.extract import ExcelExtractor

  pipeline = Pipeline(...)
  excel_extractor = ExcelExtractor(source="path_to_excel_file")
  pipeline.target_extractor = excel_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Class: MultiExcelExtractor

The `MultiExcelExtractor` class processes multiple Excel files from a specified directory. It extends the `MultiFileExtractor` and automatically identifies Excel files based on common extensions (.xlsx and .xls). For each Excel file, an `ExcelExtractor` instance is created and used to add the data to the `Pipeline` context.

## Initialization

- **`__init__(source, chunk_size=None, on_error=None, **kwargs)`**  
  Initializes a new `MultiExcelExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - The directory containing the Excel files.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ExcelExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments to pass to the `ExcelExtractor` constructor.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `MultiExcelExtractor`:

```python
  from seroflow import Pipeline
  from seroflow.extract import MultiExcelExtractor

  pipeline = Pipeline(...)
  multi_excel_extractor = MultiExcelExtractor(source="path_to_directory", on_error="ignore")
  pipeline.target_extractor = multi_excel_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Class: SQLServerExtractor

The `SQLServerExtractor` class is a concrete extractor for reading data from a `SQL Server` table. It uses `SQLAlchemy` to connect to the database and `pandas` to load the table data into a DataFrame. This extractor supports both full table reads and chunked reads by constructing `SQL` queries with `OFFSET/FETCH` clauses. It also provides a method to obtain the total number of rows in the table without reading the entire dataset.

**Note**: An `Engine` object must be created and passed to use with the `SQLServerExtractor` in the `engine` parameter.

Please Review the [Engine](engine.md) documentation for further information on `Engine` Objects.

## Initialization

- **`__init__(source, engine, schema=None, step_name="SQLServerExtractor", chunk_size=None, on_error=None, **kwargs)`**  
  Initializes a new `SQLServerExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - The name of the SQL Server table.
  - `engine` *(Engine Object)*: 
    - Any `Engine` Object. (Including `SQLAlchemy` Engine, `ODBCEngine`, `Pyodbc` Engine)
  - `schema` *(str, optional)*:
    - Database Schema Name.
    - If `Engine` object contains `.schema` attribute then `schema` is optional.
    - If `Engine` object does not contain `.schema` attribute then `schema` is mandatory.
  - `step_name` *(str, optional)*: 
    - The name of the extraction step.
    - Default: `SQLServerExtractor`.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `SQLServerExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments for `SQL` queries (e.g., for chunked extraction using skiprows and nrows).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `SQLServerExtractor`:

```python
  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from seroflow.engine import SQLAlchemyEngine # Select preferred Engine

  pipeline = Pipeline(...)
  engine = SQLAlchemyEngine(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Class: ODBCExtractor

The `ODBCExtractor` class is a concrete extractor for reading data from a `ODBC Data source` tables. Uses a `pyodbc.Connection` to execute SQL queries and returns pandas DataFrames. Supports full-table extraction or chunked extraction via OFFSET/FETCH for batching large tables.

**Note**: An `Engine` object must be created and passed to use with the `ODBCExtractor` in the `engine` parameter.

Please Review the [Engine](engine.md) documentation for further information on `Engine` Objects.

## Initialization

- **`__init__(source, engine, schema, step_name="ODBCExtractor", chunk_size=None, on_error=None, **kwargs)`**  
  Initializes a new `ODBCExtractor` instance.
  
  **Parameters:**
  
  - `source` *(str)*: 
    - Name of the table or view to read.
  - `engine` *(Engine Object)*: 
    - A `Pyodbc Engine` object.
  - `schema` *(str, optional)*:
    - Database Schema Name.
    - If `Engine` object contains `.schema` attribute then `schema` is optional.
    - If `Engine` object does not contain `.schema` attribute then `schema` is mandatory.
  - `step_name` *(str, optional)*: 
    - The name of the extraction step.
    - Default: `ODBCExtractor`.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ODBCExtractor` without terminating the `Pipeline` execution.
  - `chunk_size` *(int, optional)*: 
    - The number of rows to process at a time. If provided, enables chunked reading.
  - `**kwargs` *(Any)*: 
    - Additional keyword arguments for `SQL` queries 

#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `ODBCExtractor`:

```python
    from seroflow import Pipeline
    from seroflow.extract import ODBCExtractor
    import pyodbc

    pipeline = Pipeline(...)
    engine = pyodbc.connect(...)
    odbc_extractor = ODBCExtractor(source="Table Name", engine=engine, schema="Schema Name")
    pipeline.target_extractor = odbc_extractor # Or add it using the add_step(s) methods
    pipeline.execute()
```