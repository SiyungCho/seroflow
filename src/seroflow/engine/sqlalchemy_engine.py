"""Module: sqlalchemy_engine.py

Provides a concrete Engine implementation using SQLAlchemy for ODBC-accessible databases
(e.g., SQL Server). Defines SQLAlchemyEngine, which builds a connection URL,
creates an SQLAlchemy Engine, and validates connectivity.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from .engine import Engine
class SQLAlchemyEngine(Engine):
    """
    Concrete Engine for SQLAlchemy-based connections.

    Inherits from the base Engine to construct an SQLAlchemy connection URL,
    instantiate the engine, and perform basic connection tests.
    """

    def __init__(
        self,
        schema: str,
        server: str,
        database: str,
        driver: str,
        fast_executemany: str = "yes",
        dialect: str = "mssql+pyodbc",
        port: int = None,
        username: str = "",
        password: str = "",
        trusted_connection: str = "yes",
        **kwargs,
    ):
        """
        Initialize a SQLAlchemyEngine with connection parameters.

        Args:
            schema (str): Database schema or owner.
            server (str): Hostname or IP of the database server.
            database (str): Name of the target database.
            driver (str): ODBC driver name for the connection.
            fast_executemany (str): Whether to enable fast_executemany for bulk inserts.
            dialect (str): SQLAlchemy dialect+driver string (default 'mssql+pyodbc').
            port (int, optional): Port number for the database server.
            username (str): Username for authentication.
            password (str): Password for authentication.
            trusted_connection (str): Enable trusted connection (Windows authentication).
            **kwargs: Additional query parameters for the connection URL.
        """
        connection_settings = {
            "server": server,
            "database": database,
            "driver": driver,
            "fast_executemany": fast_executemany,
            "dialect": dialect,
            "port": port,
            "username": username,
            "password": password,
            "trusted_connection": trusted_connection,
        }
        super().__init__(schema, connection_settings, engine_type="sqlalchemy", **kwargs)

    def create_engine(self):
        """
        Construct the connection URL and create an SQLAlchemy Engine instance.

        Returns:
            sqlalchemy.engine.Engine: An active SQLAlchemy Engine.

        Raises:
            RuntimeError: If engine creation fails.
        """
        self.url = self.create_url()
        try:
            return self.create_alchemy_engine()
        except Exception as e:
            raise RuntimeError("Error creating SQLAlchemy engine") from e

    def test_engine(self):
        """
        Validate the SQLAlchemy Engine by executing a simple query against
        INFORMATION_SCHEMA.TABLES.

        Raises:
            RuntimeError: If the test query fails to execute.
        """
        test_query = text(
            "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :schema"
        )
        try:
            with self.engine.connect() as connection:
                connection.execute(test_query, {"schema": self.schema}).fetchall()
        except Exception as e:
            raise RuntimeError("Error testing the SQLAlchemy connection") from e

    def create_url(self):
        """
        Build and return a SQLAlchemy URL object from connection settings.

        Returns:
            sqlalchemy.engine.URL: Connection URL for the database.
        """
        query = {
            "driver": self.driver,
            "trusted_connection": str(self.trusted_connection).lower(),
        }
        query.update(self.kwargs)
        return URL.create(
            self.connection_settings.get("dialect"),
            username=self.username,
            password=self.password,
            host=self.server,
            port=self.port,
            database=self.database,
            query=query,
        )

    def create_alchemy_engine(self):
        """
        Instantiate and return the SQLAlchemy Engine using the constructed URL.

        Returns:
            sqlalchemy.engine.Engine: Configured SQLAlchemy Engine.
        """
        return create_engine(self.url, fast_executemany=self.fast_executemany)
