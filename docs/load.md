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

## Class: Loader

The `Loader` class is an abstract base class for writing a `pandas` DataFrame (or multiple DataFrames) to a target destination. It extends a base `Step` class and defines a common interface for output operations.

**The class manages:**
- A list of DataFrames (ensuring even single DataFrame inputs are converted to a list).
- The file mode (or table existence behavior) through an exists parameter that must be one of `"append", "fail", or "replace"`.

**Abstract methods that subclasses must implement:**
- `func(self, context)`: Reads DataFrames from the provided `Pypeline` context and writes them to the target.
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
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `Loader` without terminating the `Pypeline` execution.

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
    from pypeline import Pypeline
    from pypeline.load import Loader

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

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data

    custom_loader = MyCustomLoader(...)
    pypeline.target_loader = custom_loader # Or add it using the add_step(s) methods
    pypeline.execute()
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
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `FileLoader` without terminating the `Pypeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `“FileLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the loader function.
  
#### Initialization Example

Below is an example demonstrating how a concrete load implementation might inherit from `FileLoader` and implement its methods:

```python
    from pypeline import Pypeline
    from pypeline.load import FileLoader

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

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data

    custom_file_loader = MyCustomFileLoader(...)
    pypeline.target_loader = custom_file_loader # Or add it using the add_step(s) methods
    pypeline.execute()
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
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `CSVLoader` without terminating the `Pypeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `CSVLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the CSV writing function (passed to to_csv()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pypeline` object with an `CSVLoader`:

```python
    from pypeline import Pypeline
    from pypeline.load import CSVLoader

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data

    csv_loader = CSVLoader(target="path_to_csv_destination", dataframe="...")
    pypeline.target_loader = csv_loader # Or add it using the add_step(s) methods
    pypeline.execute()
```

## Class: MultiCSVLoader

The `MultiCSVLoader` class extends `CSVLoader` to handle writing multiple DataFrames to separate CSV files. It expects a list of DataFrames Names stored in the Pypeline Object and writes each DataFrame to its own file within the specified target directory.

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
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `MultiCSVLoader` without terminating the `Pypeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `MultiCSVLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the CSV writing function (passed to to_csv()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pypeline` object with an `MultiCSVLoader`:

```python
    from pypeline import Pypeline
    from pypeline.load import MultiCSVLoader

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data

    multi_csv_loader = MultiCSVLoader(target="path_to_directory_destination", dataframes=["...", "..."])
    pypeline.target_loader = multi_csv_loader # Or add it using the add_step(s) methods
    pypeline.execute()
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
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `ExcelLoader` without terminating the `Pypeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `ExcelLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the Excel writing function (passed to to_excel()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pypeline` object with an `ExcelLoader`:

```python
    from pypeline import Pypeline
    from pypeline.load import ExcelLoader

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data

    excel_loader = ExcelLoader(target="path_to_excel_destination", dataframe="...")
    pypeline.target_loader = excel_loader # Or add it using the add_step(s) methods
    pypeline.execute()
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
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `MultiExcelLoader` without terminating the `Pypeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `MultiExcelLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the Excel writing function (passed to to_excel()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pypeline` object with an `MultiExcelLoader`:

```python
    from pypeline import Pypeline
    from pypeline.load import MultiExcelLoader

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data

    multi_excel_loader = MultiExcelLoader(target="path_to_directory_destination", dataframes=["...", "..."])
    pypeline.target_loader = multi_excel_loader # Or add it using the add_step(s) methods
    pypeline.execute()
```

## Class: SQLServerLoader

The `SQLServerLoader` class is a concrete loader for writing a DataFrame to SQL Server table(s). It extends the `Loader` class and leverages pandas’ `to_sql()` method. The loader accepts target table names (as a single string or list), an `Engine` object containing database connection details, and schema information. The existence parameter is passed directly to the `if_exists` argument of `to_sql()`, ensuring the appropriate behavior (append, fail, or replace).

## Initialization

- **`__init__(target, engine, dataframe, step_name="SQLServerLoader", exists="append", on_error=None, **kwargs)`**  
  Initializes a new `SQLServerLoader` instance.
  
  **Parameters:**
  
  - `target` (str):
    - The target SQL Server table name(s) where the DataFrame will be written.
  - `engine` (Engine Object):
    - An object containing the `SQLAlchemy` engine, database, and schema attributes.
  - `dataframe` (str):
    - The DataFrame Name to be written.
  - `exists` ("append", "fail", or "replace"):
    - `"append"`: File exists data will be appended to end of File.
    - `"fail"`: File exists `Step` execution will end, raising `Exception`.
    - `"replace"`: File exists, File will be overwritten with new data.
    - Default: `append`
  - `on_error` *("raises", "ignore", optional)*: 
    - `"raises"`: Raises Exceptions terminating `Pypeline` execution.
    - `"ignore"`: Ignores Exceptions terminating the `SQLServerLoader` without terminating the `Pypeline` execution.
  - `step_name` (str, optional):
    - The name of the loader step 
    - Default: `SQLServerLoader`"
  - `**kwargs`:
    - Additional keyword arguments for the DataFrame writing function (passed to to_sql()).
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pypeline` object with an `SQLServerLoader`:

```python
    from pypeline import Pypeline
    from pypeline.load import SQLServerLoader
    from pypeline.engine import SQLAlchemyEngine # Select preferred Engine

    pypeline = Pypeline(...)
    pypeline.target_extractor = ... # Set Extractor to gather data
    engine = SQLAlchemyEngine(...)

    sqlserver_loader = SQLServerLoader(target="Table Name", dataframe="...", engine=engine)
    pypeline.target_loader = sqlserver_loader # Or add it using the add_step(s) methods
    pypeline.execute()
```