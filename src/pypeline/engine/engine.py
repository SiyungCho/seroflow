from abc import ABC, abstractmethod

class AbstractEngine(ABC):

    @abstractmethod
    def __enter__(self):
        """Enable usage with the 'with' statement."""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the connection is closed when exiting a 'with' block."""

    @abstractmethod
    def __str__(self):
        """
        Return a string representation of the PyodbcEngine instance.

        Returns:
            str: A formatted string containing the connection details.
        """

    @abstractmethod
    def __create_engine(self):
        """
        Create a connection engine based on the connection settings.
        """

    @abstractmethod
    def __test_engine(self, engine):
        """
        Test the connection engine by executing a simple query.
        """

class Engine(AbstractEngine):
    """
    BaseEngine implements the common functionality for engine connection handling,
    including context management and unpacking connection settings.
    """
    def __init__(self, schema, connection_settings, engine_type, test_engine=True, **kwargs):
        self.schema = schema
        self.connection_settings = connection_settings
        self.engine_type = engine_type
        self.kwargs = kwargs
        self.unpack_connection_settings(connection_settings)
        self.engine = self.__create_engine()
        if test_engine:
            self.__test_engine(self.engine)

    def unpack_connection_settings(self, connection_settings):
        """Unpack connection settings into instance attributes."""
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
        """Enable usage with the 'with' statement."""
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close or dispose of the engine when exiting the context."""
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
        Return a string representation of the PyodbcEngine instance.

        Returns:
            str: A formatted string containing the connection details.
        """
        return (
            f"Driver: {self.driver}, Schema: {self.schema}, "
            f"Database: {self.database}, Server: {self.server}"
        )
    
    @abstractmethod
    def __create_engine(self):
        """Abstract method to create the connection engine."""

    @abstractmethod
    def __test_engine(self, engine):
        """Abstract method to test the connection engine."""
