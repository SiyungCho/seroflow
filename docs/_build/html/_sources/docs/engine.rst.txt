Engine
=======================
The modules documented here define the interface and concrete implementations for ``Seroflow`` ``Pipeline`` compatible ``Engines``.
They provide a common interface to handle common ``Engine`` connection setup, context‑management, and resource cleanup within a ``Pipeline`` Object.

**It is important to note** that all ``Seroflow`` ``Extractors`` and ``Loaders`` that require an ``Engine`` can use the native ``SQLAlchemy`` or ``Pyodbc`` connection without implementing any of the defined ``Engine`` Classes offered with ``Seroflow``, unless specified otherwise. 
``Seroflow`` offers an interface and concrete example of a compatible ``Engine`` for abstraction and validity however it is **not** mandatory to use these unless specified. 

Overview
-----------------------------------

This documentation covers three modules:

- **AbstractEngine**: Defines the ``AbstractEngine`` abstract class, which specifies the interface for creating ``Seroflow`` compatible engines.

- **Engine**: Implements the ``Engine`` class, a concrete subclass of ``AbstractEngine`` that encapsulates a single type of database connection engine. 
The ``Engine`` class manages connection initialization, default values, error handling, and other connection components.

- **SQLAlchemyEngine**: A concrete subclass of ``Engine`` that defines the connection parameters and components for a ``SQLAlchemy`` based engine. 
``SQLAlchemy`` can be widely used in many database settings and is the recommended method of creating an ``Engine``.

AbstractEngine
-----------------------------

``AbstractEngine`` is an abstract base class that defines the interface for creating ``Seroflow`` compatible engines. 
It extends Python’s ``ABC`` (Abstract Base Class) and enforces the implementation of the needed abstract methods.

.. autoclass:: seroflow.engine.engine.AbstractEngine
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example:
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete engine implementation might inherit from ``AbstractEngine`` and implement its methods: ::

   from seroflow.engine import AbstractEngine

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


Although the ``AbstractEngine`` class can be used to create Custom ``Engine`` Objects, it is not recommended due to the fact that the user will need to implement the full `Engine` logic.
It is instead recommended to use the ``Engine`` Class documented below.

Engine
-----------------------------

The ``Engine`` class provides a concrete base implementation of ``AbstractEngine``. 
It handles common functionality such as unpacking a dictionary of connection settings into individual attributes, automatically creating and testing the underlying connection upon initialization, and cleaning up resources when used within a ``with`` block.

After unpacking settings and creating the ``Engine`` object via its subclass’s ``create_engine()`` implementation, the base class calls ``test_engine()`` if requested.
When exiting a ``with`` block, the ``Engine`` automatically closes or disposes of the underlying connection in a safe manner.

.. autoclass:: seroflow.engine.engine.Engine
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example:
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete engine implementation might inherit from ``Engine`` and implement its methods: ::

   from seroflow.engine import Engine

   class DummyEngine(Engine):
      def create_engine(self):
         # Implement connection logic here.
         return 

      def test_engine(self):
         # Implement engine testing logic here.
         pass

SQLAlchemyEngine
-----------------------------------------

The ``SQLAlchemyEngine`` class extends ``Engine`` to provide a fully functional connection using ``SQLAlchemy’s`` ``create_engine()`` under the hood.
It builds a connection ``URL`` from parameters such as server, database, driver, username, password, and trusted authentication settings, then instantiates a ``SQLAlchemy`` Engine with ``fast_executemany`` enabled for high‑speed bulk inserts.

On initialization, ``SQLAlchemyEngine`` constructs its ``URL``, creates the engine, and tests connectivity by executing a simple query against ``INFORMATION_SCHEMA.TABLES``.
If any step fails, it raises a descriptive ``RuntimeError``.

.. autoclass:: seroflow.engine.sqlalchemy_engine.SQLAlchemyEngine
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example:
^^^^^^^^^^^^^^^^^
Below is an example demonstrating how ``SQLAlchemyEngine`` may be used: ::

  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from seroflow.engine import SQLAlchemyEngine # Select preferred Engine

  engine = SQLAlchemyEngine(...)

  pipeline = Pipeline(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()

Instantiating Non Seroflow provided Engines
-----------------------------------------

As mentioned previously, it is entirely possible to bypass ``Pipeline’s`` classes entirely if you prefer a native approach:

Native SQLAlchemy Example
^^^^^^^^^^^^^^^^^

In the example below we create a native ``sqlalchemy`` based engine and use it in conjunction with a ``Loader`` ``Step`` in the ``Pipeline``. ::

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

Native Pyodbc Example
^^^^^^^^^^^^^^^^^
In the example below we create a native ``pyodbc`` based engine and use it in conjunction with a ``Loader`` ``Step`` in the ``Pipeline``. ::

  from seroflow import Pipeline
  from seroflow.extract import SQLServerExtractor
  from pyodbc 

  engine = pyodbc.connect(...)

  pipeline = Pipeline(...)
  sqlserver_extractor = SQLServerExtractor(source="Table Name", engine=engine)
  pipeline.target_extractor = sqlserver_extractor # Or add it using the add_step(s) methods
  pipeline.execute()
