"""Module: engine.py

This module defines an abstract base class for database connection engines (AbstractEngine)
and a concrete base implementation (Engine) that handles common connection setup,
context‑management, and resource cleanup. Specific engine types (e.g., PyODBC, SQLAlchemy)
should subclass AbstractEngine or Engine and implement the creation and testing of the connection.
"""

from abc import ABC, abstractmethod

class AbstractEngine(ABC):
    """
    Defines the interface for a database connection engine, enforcing context management
    and connection testing functionality.
    """

    @abstractmethod
    def __enter__(self):
        """
        Enter a runtime context related to the engine. Allows usage with the 'with' statement.

        Returns:
            AbstractEngine: The engine instance itself.
        """

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and ensure that the connection engine is properly closed or disposed.

        Args:
            exc_type (type): Exception type if raised in the context, otherwise None.
            exc_val (Exception): Exception value if raised in the context, otherwise None.
            exc_tb (traceback): Traceback if an exception occurred, otherwise None.
        """

    @abstractmethod
    def __str__(self):
        """
        Return a human-readable string representation of the engine, including key connection details.

        Returns:
            str: Connection details formatted as a string.
        """

    @abstractmethod
    def create_engine(self):
        """
        Instantiate and return the underlying database connection or engine object.

        Returns:
            Any: A connection or engine instance.
        """

    @abstractmethod
    def test_engine(self):
        """
        Validate the engine by executing a minimal query or connectivity check.

        Raises:
            RuntimeError: If the connection test fails.
        """

class Engine(AbstractEngine):
    """
    Base implementation of AbstractEngine that provides common functionality for unpacking
    connection settings, context management, and cleanup. Subclasses must implement create_engine()
    and test_engine() to provide engine-specific behavior.
    """

    def __init__(
        self,
        schema: str,
        connection_settings: dict,
        engine_type: str,
        test_engine: bool = True,
        **kwargs
    ):
        """
        Initialize the Engine with connection configuration and optionally test the connection.

        Args:
            schema (str): Database schema or owner name.
            connection_settings (dict): Dictionary containing connection parameters (server, database,
                                        driver, username, password, port, trusted_connection, dialect, dsn).
            engine_type (str): Identifier for the type of engine (e.g., 'pyodbc', 'sqlalchemy').
            test_engine (bool): Whether to perform an immediate connectivity test upon initialization.
            **kwargs: Additional engine-specific keyword arguments.
        """
        self.schema = schema
        self.connection_settings = connection_settings
        self.engine_type = engine_type
        self.kwargs = kwargs
        self.unpack_connection_settings(connection_settings)
        self.engine = self.create_engine()
        if test_engine:
            self.test_engine()

    def unpack_connection_settings(self, connection_settings: dict):
        """
        Extract known connection parameters from a settings dictionary into instance attributes.

        Args:
            connection_settings (dict): Connection parameters.
        """
        self.server = connection_settings.get("server")
        self.database = connection_settings.get("database")
        self.driver = connection_settings.get("driver")
        self.username = connection_settings.get("username")
        self.password = connection_settings.get("password")
        self.port = connection_settings.get("port")
        self.trusted_connection = connection_settings.get("trusted_connection")
        self.dialect = connection_settings.get("dialect")
        self.fast_executemany = connection_settings.get("fast_executemany")
        self.dsn = connection_settings.get("dsn")

    def __enter__(self):
        """
        Enter context management, returning the engine for use within a 'with' block.

        Returns:
            Engine: This engine instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context management, closing or disposing the engine based on its type.

        Args:
            exc_type (type): Exception type if raised.
            exc_val (Exception): Exception value if raised.
            exc_tb (traceback): Traceback if an exception occurred.

        Raises:
            RuntimeError: If closing or disposing fails.
        """
        try:
            if self.engine:
                if self.engine_type == "pyodbc":
                    if hasattr(self.engine, "close"):
                        self.engine.close()
                else:
                    if hasattr(self.engine, "dispose"):
                        self.engine.dispose()
        except Exception as e:
            raise RuntimeError("Error closing the connection engine") from e

    def __str__(self):
        """
        Format connection details into a readable string.

        Returns:
            str: Connection information.
        """
        return (
            f"Driver: {self.driver}, Schema: {self.schema}, "
            f"Database: {self.database}, Server: {self.server}"
        )

    @abstractmethod
    def create_engine(self):
        """
        Create and return the concrete engine/connection object. Must be implemented by subclasses.
        """

    @abstractmethod
    def test_engine(self):
        """
        Perform a connectivity check to verify that the engine can successfully connect to the database.

        Raises:
            RuntimeError: If the connection test fails.
        """
