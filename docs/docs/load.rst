.. _loaders:

Loaders
=====================
The modules documented here define the base structure and concrete implementations for ``Loader`` steps.
These loaders are responsible for outputting data to target destinations such as files or DB tables.
The loaders handle necessary configurations such as target path determination, file mode management based on an existence parameter, and file-format-specific behavior.

Overview
---------------------------------

This documentation covers:

- **Loader**: An abstract base class that specifies the interface for writing a DataFrame to a target destination.
- **FileLoader**: An abstract loader for file-based outputs. It extends the Loader class to determine the target file path (or directory), manage file modes (e.g., append, fail, replace), and define the file extension used for output.
- **CSVLoader**: A concrete loader for writing a single DataFrame to a CSV file. It maps the existence parameter to the proper file mode for CSV writing and determines the appropriate target file path.
- **MultiCSVLoader**: A concrete loader for writing multiple DataFrames to separate CSV files within a target directory. It reuses CSVLoader functionality to handle each DataFrame individually.
- **ExcelLoader**: A concrete loader for writing a single DataFrame to an Excel file. It implements Excel-specific logic including target file path determination, selection of Excel writing engines, and mapping of the existence parameter.
- **MultiExcelLoader**: A concrete loader for writing multiple DataFrames to separate Excel files within a target directory. It reuses ExcelLoader functionality to handle each DataFrame individually.
- **SQLServerLoader**: A concrete loader for writing a DataFrame to a SQL Server table using pandas’ to_sql() functionality. It supports writing data into an SQL table while handling schema information and file mode mapping.
- **ODBCLoader**: A concrete loader for writing a DataFrame to a ODBC‑accessible target. Inserts a pandas DataFrame into a database table via ODBC.

Loader
---------------------------

The ``Loader`` class is an abstract base class for writing a ``pandas`` DataFrame (or multiple DataFrames) to a target destination.
It extends a base ``Step`` class and defines a common interface for output operations.

**The class manages:**

- A list of DataFrames (ensuring even single DataFrame inputs are converted to a list).
- The file mode (or table existence behavior) through an exists parameter that must be one of ``"append", "fail", or "replace"``.

.. autoclass:: seroflow.load.loader.Loader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete load implementation might inherit from ``Loader`` and implement its methods: ::

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

FileLoader
---------------------------------

The ``FileLoader`` class is an abstract loader for file-based outputs.
It extends the ``Loader`` class and adds functionality to validate and determine the target file path.
The loader checks if the provided target is a file or a directory.
When a directory is provided, the file extension is used to form the complete target file name.
Subclasses are expected to implement file-format-specific logic in the ``func()`` method.

.. autoclass:: seroflow.load.file_loader.FileLoader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete load implementation might inherit from ``FileLoader`` and implement its methods: ::

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

CSVLoader
--------------------------------

The ``CSVLoader`` class is a concrete loader for writing a single DataFrame to a CSV file.
It extends ``FileLoader`` and implements CSV-specific logic by mapping the existence parameter to CSV file modes (``'a'`` for append, ``'x'`` for fail, ``'w'`` for replace).
It determines the target file path dynamically if only a directory is provided.

.. autoclass:: seroflow.load.csv_loader.CSVLoader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``CSVLoader``: ::

    from seroflow import Pipeline
    from seroflow.load import CSVLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    csv_loader = CSVLoader(target="path_to_csv_destination", dataframe="...")
    pipeline.target_loader = csv_loader # Or add it using the add_step(s) methods
    pipeline.execute()

MultiCSVLoader
--------------------------------

The ``MultiCSVLoader`` class extends ``CSVLoader`` to handle writing multiple DataFrames to separate CSV files. 
It expects a list of DataFrames Names stored in the ``Pipeline`` Object and writes each DataFrame to its own file within the specified target directory.

.. autoclass:: seroflow.load.csv_loader.MultiCSVLoader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``MultiCSVLoader``: ::

    from seroflow import Pipeline
    from seroflow.load import MultiCSVLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    multi_csv_loader = MultiCSVLoader(target="path_to_directory_destination", dataframes=["...", "..."])
    pipeline.target_loader = multi_csv_loader # Or add it using the add_step(s) methods
    pipeline.execute()

ExcelLoader
----------------------------------

The ``ExcelLoader`` class is a concrete loader for writing a single DataFrame to an Excel file.
It extends ``FileLoader`` and implements Excel-specific logic, such as choosing the correct writing engine (e.g., openpyxl for .xlsx) and handling file modes based on the existence parameter.
It also builds the target file path dynamically if a directory is provided.

.. autoclass:: seroflow.load.excel_loader.ExcelLoader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``ExcelLoader``: ::

    from seroflow import Pipeline
    from v.load import ExcelLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    excel_loader = ExcelLoader(target="path_to_excel_destination", dataframe="...")
    pipeline.target_loader = excel_loader # Or add it using the add_step(s) methods
    pipeline.execute()


MultiExcelLoader
----------------------------------

The ``MultiExcelLoader`` class extends ``ExcelLoader`` to handle multiple DataFrames.
When provided with a list of DataFrame Names, it writes each one to a separate Excel file within the specified target directory.
The loader constructs individual file paths based on the DataFrame key and the defined file extension.

.. autoclass:: seroflow.load.excel_loader.MultiExcelLoader
   :members:
   :show-inheritance:
   :undoc-members:
  
Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``MultiExcelLoader``:

    from seroflow import Pipeline
    from seroflow.load import MultiExcelLoader

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data

    multi_excel_loader = MultiExcelLoader(target="path_to_directory_destination", dataframes=["...", "..."])
    pipeline.target_loader = multi_excel_loader # Or add it using the add_step(s) methods
    pipeline.execute()

ODBCLoader
---------------------------------

The ``ODBCLoader`` class is a concrete loader for writing a DataFrame to into an ODBC-accessible database using raw ``SQL`` executed via a ``pyodbc.Connection``.
The loader accepts a single target table name, an ``Engine`` object containing database connection details, and schema information.
The existence parameter is defined, ensuring the appropriate behavior (append, fail, or replace).

**Note**: An ``Engine`` object must be created and passed to use with the ``ODBCLoader`` in the ``engine`` parameter.

Please Review the :ref:`engine` documentation for further information on ``Engine`` Objects.

.. autoclass:: seroflow.load.odbc_loader.ODBCLoader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``ODBCLoader``:

  from seroflow import Pipeline
  from seroflow.load import ODBCLoader
  import pyodbc

  pipeline = Pipeline(...)
  pipeline.target_extractor = ... # Set Extractor to gather data
  engine = pyodbc.connect(...)

  odbc_loader = ODBCLoader(target="Table Name", dataframe="...", engine=engine, schema="Schema Name")
  pipeline.target_loader = odbc_loader # Or add it using the add_step(s) methods
  pipeline.execute()

SQLServerLoader
--------------------------------------

The ``SQLServerLoader`` class is a concrete loader for writing a DataFrame to SQL Server table(s).
It extends the ``Loader`` class and leverages pandas’ ``to_sql()`` method.
The loader accepts target table names (as a single string or list), an ``Engine`` object containing database connection details, and schema information.
The existence parameter is passed directly to the ``if_exists`` argument of ``to_sql()``, ensuring the appropriate behavior (append, fail, or replace).

**Note**: An ``Engine`` object must be created and passed to use with the ``SQLServerLoader`` in the ``engine`` parameter.

Please Review the :ref:`engine` documentation for further information on ``Engine`` Objects.

.. autoclass:: seroflow.load.sqlserver_loader.SQLServerLoader
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``SQLServerLoader``:

    from seroflow import Pipeline
    from seroflow.load import SQLServerLoader
    from seroflow.engine import SQLAlchemyEngine # Select preferred Engine

    pipeline = Pipeline(...)
    pipeline.target_extractor = ... # Set Extractor to gather data
    engine = SQLAlchemyEngine(...)

    sqlserver_loader = SQLServerLoader(target="Table Name", dataframe="...", engine=engine)
    pipeline.target_loader = sqlserver_loader # Or add it using the add_step(s) methods
    pipeline.execute()
