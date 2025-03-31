# Engine Documentation

The modules documented here define the base structure and a concrete implementation for `Pipeline` compatible Engines. They provide a common interface to handle common connection setup, context‑management, and resource cleanup within a `Pipeline`.

**It is important to note** that all `Pipeline` `Extractors` and `Loaders` that require an `Engine` can use the native `SQLAlchemy` or `Pyodbc` connection without implementing any of the defined `Engine` Classes offered with `Pipeline`. `Pipeline` offers an interface and concrete example of a compatible engine for abstraction and validity however it is **not** mandatory to use these unless specified. 

## Overview

This documentation covers three modules:

- **AbstractEngine**:  
  Defines the `AbstractEngine` abstract class, which specifies the interface for creating `Pipeline` compatible engines.

- **Engine**:  
  Implements the `Engine` class, a concrete subclass of `AbstractEngine` that encapsulates a single type of database connection engine. The `Engine` class manages connection initialization, default values, error handling, and other connection components.

- **SQLAlchemyEngine**:  
  A concrete subclass of `Engine` that defines the connection parameters and components for a SQLAlchemy based engine. SQLAlchemy can be widely used in many database settings and is the recommended method of creating an Engine.

## Class: AbstractEngine

`AbstractEngine` is an abstract base class that defines the interface for creating `Pipeline` compatible engines. It extends Python’s `ABC` (Abstract Base Class) and enforces the implementation of the following methods:

- **`create_engine()`**  
    *Abstract Method*  
    Instantiate and return the underlying database connection or engine object.

    **Returns**:
    Any: A connection or engine instance.

- **`test_engine()`**  
    *Abstract Method*  
    Validate the engine by executing a minimal query or connectivity check.

    **Raises**:
    RuntimeError: If the connection test fails.

- **`__enter__()`**  
    *Abstract Method*  
    Enter a runtime context related to the engine. Allows usage with the 'with' statement.

    **Returns**:
    AbstractEngine: The engine instance itself.

- **`__exit__()`**  
    *Abstract Method*  
    Exit the runtime context and ensure that the connection engine is properly closed or disposed.

    **Parameters**:
    - exc_type (type): Exception type if raised in the context, otherwise None.
    - exc_val (Exception): Exception value if raised in the context, otherwise None.
    - exc_tb (traceback): Traceback if an exception occurred, otherwise None.

- **`__str__()`**  
    *Abstract Method*  
    Return a human-readable string representation of the engine, including key connection details.

    **Returns**:
    str: Connection details formatted as a string.

**AbstractEngine Example:**

```python
from abstract_step import AbstractEngine

class MyEngine(AbstractEngine):
    def create_engine(self):
        # Initialize engine connection.
        pass

    def test_engine(self):
        # Implement engine connection test.
        pass

    def __enter__(self):
        # Implement engine 'with' logic.
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Implement engine connection deletion logic.
        return

    def __str__(self):
        return (
            f"Driver: {self.driver}, "
            f"Database: {self.database}"
        )
```

Although the `AbstractEngine` class can be used to create Custom Engine Objects, it is not recommended due to the fact that the user will need to implement the full engine logic. It is instead recommended to use the `Engine` Class documented below.

## Class: Engine

The `Engine` class provides a concrete base implementation of `AbstractEngine`. It handles common functionality such as unpacking a dictionary of connection settings into individual attributes, automatically creating and testing the underlying connection upon initialization, and cleaning up resources when used within a `with` block.

After unpacking settings and creating the `Engine` object via its subclass’s `create_engine()` implementation, the base class calls `test_engine()` if requested. When exiting a `with` block, the `Engine` automatically closes or disposes of the underlying connection in a safe manner.

**Subclasses must override:**
- `create_engine()`: Creates and returns the engine with a the specific connection parameters.
- `test_engine()`: Tests the created engine to ensure that connection is successful.
  
## Initialization

- **`__init__(schema, connection_settings, engine_type, test_engine=True, **kwargs)`**  
  Initializes a new `Engine` instance.
  
  **Parameters:**
  - **schema** (str): 
    - Database schema or owner name.
  - **connection_settings** (dict): 
    - Dictionary containing connection parameters:
      - server, database, driver, username, password, port, trusted_connection, dialect, dsn
  - **engine_type** (str): 
    - Identifier for the type of engine (e.g., 'pyodbc', 'sqlalchemy').
  - **test_engine** (bool): 
    - Perform an immediate connectivity test upon initialization.
  - ****kwargs**: 
    - Additional engine-specific keyword arguments.

#### Example

```python
from seroflow.engine import Engine

class DummyEngine(Engine):
    def create_engine(self):
        # Implement connection logic here.
        return 

    def test_engine(self):
        # Implement engine testing logic here.
        pass

```

## Class: SQLAlchemyEngine

The `SQLAlchemyEngine` class extends `Engine` to provide a fully functional connection using `SQLAlchemy’s` `create_engine()` under the hood. It builds a connection URL from parameters such as server, database, driver, username, password, and trusted authentication settings, then instantiates an `SQLAlchemy` Engine with `fast_executemany` enabled for high‑speed bulk inserts.

On initialization, `SQLAlchemyEngine` constructs its URL, creates the engine, and tests connectivity by executing a simple query against `INFORMATION_SCHEMA.TABLES`. If any step fails, it raises a descriptive `RuntimeError`.
  
## Initialization

- **`__init__(schema, server, database, driver, fast_executemany="yes", dialect="mssql+pyodbc", port=None, username="", password="",trusted_connection= "yes", **kwargs,)`**  
  Initializes a new `SQLAlchemyEngine` instance.
  
  **Parameters:**
  - **schema** (str): 
    - Database schema or owner.
  - **server** (str): 
    - Hostname or IP of the database server.
  - **database** (str): 
    - Name of the target database.
  - **driver** (str): 
    - ODBC driver name for the connection.
  - **fast_executemany** (str, optional): 
    - Whether to enable fast_executemany for bulk inserts.
    - Default: "yes"
  - **dialect** (str, optional): 
    - SQLAlchemy dialect+driver string (default 'mssql+pyodbc').
    - Default: "mssql+pyodbc"
  - **port** (int, optional): 
    - Port number for the database server.
    - Default: None
  - **username** (str, optional): 
    - Username for authentication.
    - Default: ""
  - **password** (str, optional): 
    - Password for authentication.
    - Default: ""
  - **trusted_connection** (str, optional): 
    - Enable trusted connection (Windows authentication).
    - Default: "yes"
  - ****kwargs**: 
    - Additional query parameters for the connection URL.

#### Example

```python
  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from seroflow.engine import SQLAlchemyEngine # Select preferred Engine

  engine = SQLAlchemyEngine(...)

  pipeline = Pipeline(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

## Instantiating Non Seroflow provided Engines
As mentioned previously, it is entirely possible to bypass `Pipeline’s` classes entirely if you prefer a native approach:

#### Example
In the example below we create a native `sqlalchemy` based engine and use it in conjunction with a Loader Step in the `Pipeline`.

```python
  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from sqlalchemy import create_engine
  from sqlalchemy.engine import URL

  connection_url = URL.create(...)
  engine = create_engine(connection_url, ...)

  pipeline = Pipeline(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```

#### Example
In the example below we create a native `pyodbc` based engine and use it in conjunction with a Loader Step in the `Pipeline`.

```python
  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from pyodbc 

  engine = pyodbc.connect(...)

  pipeline = Pipeline(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
```