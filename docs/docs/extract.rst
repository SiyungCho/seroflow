Extractors
========================

The modules documented here define the base structure and concrete implementations for ``Extractor`` steps. 
These extractors are responsible for reading data from various sources—such as files or DB tables—and adding the resulting pandas DataFrames to the ``Pipeline`` context. 
The extractors support both full reads and chunked reads, as well as error handling and row count estimation.

Overview
---------------------------------

This documentation covers:

- **Extractor**: Abstract class, which specifies the interface for creating a single extractor.
- **MultiExtractor**: A concrete class that aggregates multiple extractor instances to handle multiple sources in a single step.
- **FileExtractor**: Abstract class, which specifies the interface for creating a single extractor, specifically for File data sources.
- **MultiFileExtractor**: A concrete class extending ``MultiExtractor`` that gathers file paths from a directory (based on extension) and creates extractor instances for each file.
- **CSVExtractor**: Single CSV File data extractor. Extracts data within a single CSV File.
- **MultiCSVExtractor**: Multi CSV File data extractor. Extracts data from multiple CSV Files given a directory path.
- **ExcelExtractor**: Single Excel File data extractor. Extracts data within a single Excel File.
- **MultiExcelExtractor**: Multi Excel File data extractor. Extracts data from multiple Excel Files given a directory path.
- **SQLServerExtractor**: Single SQL Server Table data extractor. Extracts data within a single SQL Server Table.
- **ODBCExtractor**: Single ODBC Source Table data extractor. Extracts data within a single ODBC Source Table.


Extractor 
---------------------------------

The ``Extractor`` class is an abstract base class that provides the common structure for all data extractors.
It defines the general interface and common behaviors such as handling chunk sizes and managing the step lifecycle (e.g., start and stop).

.. autoclass:: seroflow.extract.extractor.Extractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete extract implementation might inherit from ``Extractor`` and implement its methods: ::

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

MultiExtractor 
---------------------------------

.. autoclass:: seroflow.extract.extractor.MultiExtractor
   :members:
   :show-inheritance:
   :undoc-members:

FileExtractor
---------------------------------------

The ``FileExtractor`` class extends ``Extractor`` and provides a template for file-based data sources.
In addition to the standard ``Extractor`` functionality, it validates the file’s existence, extracts the file name without its extension, and stores additional keyword arguments for the file reading operation.

.. autoclass:: seroflow.extract.file_extractor.FileExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete extract implementation might inherit from ``FileExtractor`` and implement its methods: ::

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

MultiFileExtractor
---------------------------------------

.. autoclass:: seroflow.extract.file_extractor.MultiFileExtractor
   :members:
   :show-inheritance:
   :undoc-members:

CSVExtractor
--------------------------------------

The ``CSVExtractor`` class is a concrete implementation for extracting data from a single CSV file.
It leverages ``pandas’`` ``read_csv()`` method to load the CSV file into a DataFrame and adds it to the ``Pipeline`` context under the file name.
In addition, it provides a method for counting the total number of rows in the CSV file, which is useful for operations like chunked reading.

.. autoclass:: seroflow.extract.csv_extractor.CSVExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``CSVExtractor``: ::

  from seroflow import Pipeline
  from seroflow.extract import CSVExtractor

  pipeline = Pipeline(...)
  csv_extractor = CSVExtractor(source="path_to_csv_file")
  pipeline.target_extractor = csv_extractor # Or add it using the add_step(s) methods
  pipeline.execute()

MultiCSVExtractor
--------------------------------------

The ``MultiCSVExtractor`` class handles the extraction of data from multiple CSV files stored in a given directory.
It extends the ``MultiFileExtractor`` and automatically gathers CSV file paths based on the specified directory.
For each CSV file, it creates an instance of ``CSVExtractor`` to process and load the data into the ``Pipeline`` context.

.. autoclass:: seroflow.extract.csv_extractor.MultiCSVExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``MultiCSVExtractor``: ::

  from seroflow import Pipeline
  from seroflow.extract import MultiCSVExtractor

  pipeline = Pipeline(...)
  multi_csv_extractor = MultiCSVExtractor(source="path_to_directory", chunk_size=100)
  pipeline.target_extractor = multi_csv_extractor # Or add it using the add_step(s) methods
  pipeline.execute(chunker=...)

ExcelExtractor
----------------------------------------

The ``ExcelExtractor`` class is a concrete implementation for reading data from a single Excel file.
It supports both .xls and .xlsx formats by selecting the appropriate engine (xlrd for .xls and openpyxl for .xlsx).
The extractor loads the data into a DataFrame and adds it to the ``Pipeline`` context under the file name.

.. autoclass:: seroflow.extract.excel_extractor.ExcelExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``ExcelExtractor``: ::

  from seroflow import Pipeline
  from seroflow.extract import ExcelExtractor

  pipeline = Pipeline(...)
  excel_extractor = ExcelExtractor(source="path_to_excel_file")
  pipeline.target_extractor = excel_extractor # Or add it using the add_step(s) methods
  pipeline.execute()

MultiExcelExtractor
----------------------------------------

The ``MultiExcelExtractor`` class processes multiple Excel files from a specified directory.
It extends the ``MultiFileExtractor`` and automatically identifies Excel files based on common extensions (.xlsx and .xls).
For each Excel file, an ``ExcelExtractor`` instance is created and used to add the data to the ``Pipeline`` context.

.. autoclass:: seroflow.extract.excel_extractor.MultiExcelExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``MultiExcelExtractor``: ::

  from seroflow import Pipeline
  from seroflow.extract import MultiExcelExtractor

  pipeline = Pipeline(...)
  multi_excel_extractor = MultiExcelExtractor(source="path_to_directory", on_error="ignore")
  pipeline.target_extractor = multi_excel_extractor # Or add it using the add_step(s) methods
  pipeline.execute()

ODBCExtractor
---------------------------------------

The ``ODBCExtractor`` class is a concrete extractor for reading data from a ``ODBC Data source`` tables.
Uses a ``pyodbc.Connection`` to execute ``SQL`` queries and returns ``pandas`` DataFrames.
Supports full-table extraction or chunked extraction via ``OFFSET/FETCH`` for batching large tables.

**Note**: An ``Engine`` object must be created and passed to use with the ``ODBCExtractor`` in the ``engine`` parameter.

Please Review the [Engine](engine.md) documentation for further information on ``Engine`` Objects.

.. autoclass:: seroflow.extract.odbc_extractor.ODBCExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``ODBCExtractor``: ::

    from seroflow import Pipeline
    from seroflow.extract import ODBCExtractor
    import pyodbc

    pipeline = Pipeline(...)
    engine = pyodbc.connect(...)
    odbc_extractor = ODBCExtractor(source="Table Name", engine=engine, schema="Schema Name")
    pipeline.target_extractor = odbc_extractor # Or add it using the add_step(s) methods
    pipeline.execute()

SQLServerExtractor
--------------------------------------------

The ``SQLServerExtractor`` class is a concrete extractor for reading data from a ``SQL Server`` table.
It uses ``SQLAlchemy`` to connect to the database and ``pandas`` to load the table data into a DataFrame.
This extractor supports both full table reads and chunked reads by constructing ``SQL`` queries with ``OFFSET/FETCH`` clauses.
It also provides a method to obtain the total number of rows in the table without reading the entire dataset.

**Note**: An ``Engine`` object must be created and passed to use with the ``SQLServerExtractor`` in the ``engine`` parameter.

Please Review the [Engine](engine.md) documentation for further information on ``Engine`` Objects.


.. autoclass:: seroflow.extract.sqlserver_extractor.SQLServerExtractor
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``SQLServerExtractor``: ::

  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from seroflow.engine import SQLAlchemyEngine # Select preferred Engine

  pipeline = Pipeline(...)
  engine = SQLAlchemyEngine(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
