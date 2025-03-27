# Loader Documentation

The modules documented here define the base structure and concrete implementations for `Loader` steps. These loaders are responsible for outputting data to target destinations such as files (such as CSV or Excel) or SQL Server tables. The loaders handle necessary configurations such as target path determination, file mode management based on an existence parameter, and file-format-specific behavior.

## Overview

This documentation covers:

- **Loader**: An abstract base class that specifies the interface for writing a DataFrame to a target destination.
- **FileLoader**: An abstract loader for file-based outputs. It extends the Loader class to determine the target file path (or directory), manage file modes (e.g., append, fail, replace), and define the file extension used for output.
- **CSVLoader**: A concrete loader for writing a single DataFrame to a CSV file. It maps the existence parameter to the proper file mode for CSV writing and determines the appropriate target file path.
- **MultiCSVLoader**: A concrete loader for writing multiple DataFrames to separate CSV files within a target directory. It reuses CSVLoader functionality to handle each DataFrame individually.
- **ExcelLoader**: A concrete loader for writing a single DataFrame to an Excel file. It implements Excel-specific logic including target file path determination, selection of Excel writing engines, and mapping of the existence parameter.
- **MultiExcelLoader**: A concrete loader for writing multiple DataFrames to separate Excel files within a target directory. It reuses ExcelLoader functionality to handle each DataFrame individually.
- **SQLServerLoader**: A concrete loader for writing a DataFrame to a SQL Server table using pandas’ to_sql() functionality. It supports writing data into an SQL table while handling schema information and file mode mapping.
- **ODBCLoader**: A concrete loader for writing a DataFrame to a ODBC‑accessible target. Inserts a pandas DataFrame into a database table via ODBC.
- 
## Class: Loader

The `Loader` class is an abstract base class for writing a `pandas` DataFrame (or multiple DataFrames) to a target destination. It extends a base `Step` class and defines a common interface for output operations.

**The class manages:**
- A list of DataFrames (ensuring even single DataFrame inputs are converted to a list).
- The file mode (or table existence behavior) through an exists parameter that must be one of `"append", "fail", or "replace"`.

**Abstract methods that subclasses must implement:**
- `func(self, context)`: Reads DataFrames from the provided `Pipeline` context and writes them to the target.
- `map_exists_parameter(self)`: Maps the provided `exists` parameter to the file-mode (or SQL table mode) that is appropriate for the output format.

## Initialization

- **`__init__(step_name, dataframes, exists, func, on_error)`**  
  Initializes a new `Loader` instance.
  
  **Parameters:**
  
  - `step_name` *(str)*: 
    - Name of the Loader Step.
  - `dataframes` (str, or list[str]):
    - The DataFrame(s) Name(s) to be written to the target.
  - `exists` ("append", "fail", or "replace"):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
  - `func` *(function)*: 
    - The function to execute for writing the DataFrame.
  - `on_error` *("raises", "ignore")*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `Loader` without terminating the `Pipeline` execution.

- **`func(self, context)`**  
  *Abstract Method*  
  Must be implemented by subclasses to write the DataFrame(s) to the target location.

  **Parameters:**
  context (Context): A context object to which the DataFrame will be loaded to the target.

- **`map_exists_parameter(self)`**  
  *Abstract Method*  
  Must be implemented by subclasses to map the exists parameter to the appropriate target destination's mode.

  **Returns:**
  str: exists parameter used in load function.

#### Usage Example

Below is an example demonstrating how a concrete load implementation might inherit from `Loader` and implement its methods:

```python
    from seroflow import Pipeline
    from seroflow.load import Loader

    class MyCustomLoader(Loader):
        def __init__(self, target, dataframe, exists="append", on_error="raise"):
            # Custom initialization logic can be added here
            super().__init__(step_name="MyCustomLoader", dataframes=dataframe, exists=exists, func=self.func, on_error=on_error)
            self.target = target

        def func(self, context):
            # Custom logic to write DataFrames to the target
            for key, df in context.dataframes.items():
                df ... # Implement load logic
            return 

        def map_exists_parameter(self):
            # Map the exists parameter; for custom loaders this might be trivial
            return self.exists

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    custom_loader = MyCustomLoader(...)
    pipeline.target_loader = custom_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: FileLoader

The `FileLoader` class is an abstract loader for file-based outputs. It extends the `Loader` class and adds functionality to validate and determine the target file path. The loader checks if the provided target is a file or a directory. When a directory is provided, the file extension is used to form the complete target file name. Subclasses are expected to implement file-format-specific logic in the `func()` method.

## Initialization

- **`__init__(target, dataframe, exists, func, file_extension, on_error, step_name="FileLoader", **kwargs)`**  
  Initializes a new `FileLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target directory or full file path where the output will be written.
  - `dataframe` (DataFrame):
    - The DataFrame to be written.
  - `exists` ("append", "fail", or "replace"):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
  - `func` (function):
    - The function that writes the DataFrame to the file.
  - `file_extension` (str):
    - The file extension to be used when writing the file.
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `FileLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `“FileLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the loader function.
  
#### Initialization Example

Below is an example demonstrating how a concrete load implementation might inherit from `FileLoader` and implement its methods:

```python
    from seroflow import Pipeline
    from seroflow.load import FileLoader

    class MyCustomFileLoader(FileLoader):
        def __init__(self, target, dataframe, file_extension, exists="append", on_error="raise"):
            # Custom initialization logic can be added here
            super().__init__(step_name="MyCustomFileLoader", dataframes=dataframe, file_extension=file_extension, exists=exists, func=self.func, on_error=on_error)
            self.target = target

        def func(self, context):
            # Custom logic to write DataFrames to the target
            for key, df in context.dataframes.items():
                df ... # Implement load logic
            return 

        def map_exists_parameter(self):
            # Map the exists parameter; for custom loaders this might be trivial
            return self.exists

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    custom_file_loader = MyCustomFileLoader(...)
    pipeline.target_loader = custom_file_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: CSVLoader

The `CSVLoader` class is a concrete loader for writing a single DataFrame to a CSV file. It extends `FileLoader` and implements CSV-specific logic by mapping the existence parameter to CSV file modes ('a' for append, 'x' for fail, 'w' for replace). It determines the target file path dynamically if only a directory is provided.

## Initialization

- **`__init__(target, dataframe, exists="append", step_name="CSVLoader", on_error=None, **kwargs)`**  
  Initializes a new `CSVLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target directory or file path where the CSV file will be written.
  - `dataframe` (str):
    - The DataFrame Name to be written.
  - `exists` ("append", "fail", or "replace", optional):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `CSVLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `CSVLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the CSV writing function (passed to to_csv()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `CSVLoader`:

```python
    from seroflow import Pipeline
    from seroflow.load import CSVLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    csv_loader = CSVLoader(target="path_to_csv_destination", dataframe="...")
    pipeline.target_loader = csv_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: MultiCSVLoader

The `MultiCSVLoader` class extends `CSVLoader` to handle writing multiple DataFrames to separate CSV files. It expects a list of DataFrames Names stored in the `Pipeline` Object and writes each DataFrame to its own file within the specified target directory.

## Initialization

- **`__init__(target, dataframes=None, exists="append", step_name="MultiCSVLoader", on_error=None, **kwargs)`**  
  Initializes a new `MultiCSVLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target directory where the CSV files will be written.
  - `dataframes` (list[str]):
    - The List of DataFrame Names to be written.
  - `exists` ("append", "fail", or "replace", optional):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `MultiCSVLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `MultiCSVLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the CSV writing function (passed to to_csv()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `MultiCSVLoader`:

```python
    from seroflow import Pipeline
    from seroflow.load import MultiCSVLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    multi_csv_loader = MultiCSVLoader(target="path_to_directory_destination", dataframes=["...", "..."])
    pipeline.target_loader = multi_csv_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: ExcelLoader

The `ExcelLoader` class is a concrete loader for writing a single DataFrame to an Excel file. It extends `FileLoader` and implements Excel-specific logic, such as choosing the correct writing engine (e.g., openpyxl for .xlsx) and handling file modes based on the existence parameter. It also builds the target file path dynamically if a directory is provided.

## Initialization

- **`__init__(target, dataframe, file_extension=".xlsx", exists="append", step_name="ExcelLoader", on_error=None, **kwargs)`**  
  Initializes a new `ExcelLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target directory or file path where the Excel file will be written.
  - `dataframe` (str):
    - The DataFrame Name to be written.
  - `exists` ("append", "fail", or "replace", optional):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `file_extension` (str):
    - The file extension to use
    - Default: `.xlsx`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ExcelLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `ExcelLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the Excel writing function (passed to to_excel()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `ExcelLoader`:

```python
    from seroflow import Pipeline
    from v.load import ExcelLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    excel_loader = ExcelLoader(target="path_to_excel_destination", dataframe="...")
    pipeline.target_loader = excel_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: MultiExcelLoader

The `MultiExcelLoader` class extends `ExcelLoader` to handle multiple DataFrames. When provided with a list of DataFrame Names, it writes each one to a separate Excel file within the specified target directory. The loader constructs individual file paths based on the DataFrame key and the defined file extension.

## Initialization

- **`__init__(target, dataframes=None, file_extension=".xlsx", exists="append", step_name="MultiExcelLoader", on_error=None, **kwargs)`**  
  Initializes a new `MultiExcelLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target directory where the Excel files will be written.
  - `dataframes` (list[str]):
    - The List of DataFrame Names to be written.
  - `exists` ("append", "fail", or "replace", optional):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `file_extension` (str):
    - The file extension to use
    - Default: `.xlsx`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `MultiExcelLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `MultiExcelLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the Excel writing function (passed to to_excel()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `MultiExcelLoader`:

```python
    from seroflow import Pipeline
    from seroflow.load import MultiExcelLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    multi_excel_loader = MultiExcelLoader(target="path_to_directory_destination", dataframes=["...", "..."])
    pipeline.target_loader = multi_excel_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: SQLServerLoader

The `SQLServerLoader` class is a concrete loader for writing a DataFrame to SQL Server table(s). It extends the `Loader` class and leverages pandas’ `to_sql()` method. The loader accepts target table names (as a single string or list), an `Engine` object containing database connection details, and schema information. The existence parameter is passed directly to the `if_exists` argument of `to_sql()`, ensuring the appropriate behavior (append, fail, or replace).

**Note**: An `Engine` object must be created and passed to use with the `SQLServerLoader` in the `engine` parameter.

Please Review the [Engine](engine.md) documentation for further information on `Engine` Objects.

## Initialization

- **`__init__(target, engine, dataframe, schema=None, step_name="SQLServerLoader", exists="append", on_error=None, **kwargs)`**  
  Initializes a new `SQLServerLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target SQL Server table name(s) where the DataFrame will be written.
  - `engine` (Engine Object):
    - Any `Engine` Object. (Including `SQLAlchemy` Engine, `ODBCEngine`, `Pyodbc` Engine)
  - `dataframe` (str):
    - The DataFrame Name to be written.
  - `schema` *(str, optional)*:
    - Database Schema Name.
    - If `Engine` object contains `.schema` attribute then `schema` is optional.
    - If `Engine` object does not contain `.schema` attribute then `schema` is mandatory.
  - `exists` ("append", "fail", or "replace"):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `SQLServerLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `SQLServerLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the DataFrame writing function (passed to to_sql()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `SQLServerLoader`:

```python
    from seroflow import Pipeline
    from seroflow.load import SQLServerLoader
    from seroflow.engine import SQLAlchemyEngine # Select preferred Engine

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data
    engine = SQLAlchemyEngine(...)

    sqlserver_loader = SQLServerLoader(target="Table Name", dataframe="...", engine=engine)
    pipeline.target_loader = sqlserver_loader # Or add it using the add_step(s) methods
    pipeline.execute()
```

## Class: ODBCLoader

The `ODBCLoader` class is a concrete loader for writing a DataFrame to into an ODBC-accessible database (e.g., SQL Server) using raw SQL executed via a pyodbc.Connection. The loader accepts a single target table name, an `Engine` object containing database connection details, and schema information. The existence parameter is defined, ensuring the appropriate behavior (append, fail, or replace).

**Note**: An `Engine` object must be created and passed to use with the `ODBCLoader` in the `engine` parameter.

Please Review the [Engine](engine.md) documentation for further information on `Engine` Objects.

## Initialization

- **`__init__(target, engine, dataframe, schema, step_name="ODBCLoader", exists="append", on_error=None, **kwargs)`**  
  Initializes a new `ODBCLoader` instance.
  
  **Parameters:**

  - `target` (str):
    - Name of the destination table.
  - `engine` (Engine Object):
    - A `Pyodbc Engine` object.
  - `dataframe` (str):
    - The DataFrame Name to be written.
  - `schema` *(str)*:
    - Database Schema Name.
  - `exists` ("append", "fail", or "replace"):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pipeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ODBCLoader` without terminating the `Pipeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `ODBCLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the DataFrame writing function.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `ODBCLoader`:

```python
  from seroflow import Pipeline
  from seroflow.load import ODBCLoader
  import pyodbc

  pipeline = Pipeline(...)
  pipeline.target_extractor = ... # Set Extractor to gather data
  engine = pyodbc.connect(...)

  odbc_loader = ODBCLoader(target="Table Name", dataframe="...", engine=engine, schema="Schema Name")
  pipeline.target_loader = odbc_loader # Or add it using the add_step(s) methods
  pipeline.execute()
```