"""
Module for managing SQL database connections using SQLAlchemy.

This module provides the SQLAlchemyEngine class, which encapsulates the creation of a
SQLAlchemy engine, execution of SQL queries, and helper functions for database operations
such as checking for table existence.
"""

from typing import Any, Dict, List, Optional, Union
from sqlalchemy import create_engine, text, URL
from sqlalchemy.engine import Engine, URL as SQLAlchemyURL, Result


class SQLAlchemyEngine:
    """
    A database engine wrapper using SQLAlchemy.

    This class creates a SQLAlchemy engine using the provided connection parameters,
    executes SQL queries, and provides helper methods such as checking if a table exists.
    """

    def __init__(
        self,
        server: str,
        schema: str,
        database: str,
        driver: str,
        fast_executemany: Union[bool, str] = "yes",
        dialect: str = "mssql+pyodbc",
        port: Optional[int] = None,
        username: str = "",
        password: str = "",
        trusted_connection: str = "yes",
        **kwargs: Any,
    ) -> None:
        """
        Initialize a SQLAlchemyEngine instance.

        Sets up connection parameters, creates the connection URL and SQLAlchemy engine,
        and tests the engine by executing a simple query.

        Args:
            server (str): The database server address.
            schema (str): The schema name to use.
            database (str): The name of the database.
            driver (str): The database driver to use.
            fast_executemany (Union[bool, str], optional): Option to enable fast executemany.
                Defaults to "yes".
            dialect (str, optional): SQLAlchemy dialect to use. Defaults to "mssql+pyodbc".
            port (Optional[int], optional): The port number for the server. Defaults to None.
            username (str, optional): The username for authentication. Defaults to "".
            password (str, optional): The password for authentication. Defaults to "".
            trusted_connection (str, optional): Whether to use a trusted connection.
                Defaults to "yes".
            **kwargs: Additional keyword arguments for URL query parameters.
        """
        self.driver: str = driver
        self.schema: str = schema
        self.database: str = database
        self.server: str = server
        self.dialect: str = dialect
        self.port: Optional[int] = port
        self._username: str = username
        self.__password: str = password
        self.trusted_connection: str = trusted_connection
        self.fast_executemany: Union[bool, str] = fast_executemany

        self.url: SQLAlchemyURL = self.create_url(kwargs)
        self.engine: Engine = self.create_alchemy_engine()
        self.__test_engine()

    def create_url(self, kwargs: Dict[str, Any]) -> SQLAlchemyURL:
        """
        Create and return a SQLAlchemy URL for the database connection.

        Constructs a URL using the provided connection parameters and additional query
        arguments.

        Args:
            kwargs (Dict[str, Any]): Additional query parameters to include in the URL.

        Returns:
            SQLAlchemyURL: A URL object representing the database connection.
        """
        connection_url = URL.create(
            self.dialect,
            username=self._username,
            password=self.__password,
            host=self.server,
            port=self.port,
            database=self.database,
            query={
                "driver": self.driver,
                "trusted_connection": self.trusted_connection,
                **kwargs,
            },
        )
        return connection_url

    def create_alchemy_engine(self) -> Engine:
        """
        Create and return a SQLAlchemy engine using the constructed URL.

        Returns:
            Engine: An instance of a SQLAlchemy engine.
        """
        return create_engine(self.url, fast_executemany=self.fast_executemany)

    def _execute_query(self,
                       sql_query: str,
                       return_response: bool = False) -> Union[List[Any], bool]:
        """
        Execute a SQL query using the SQLAlchemy engine.

        Args:
            sql_query (str): The SQL query to execute.
            return_response (bool, optional): If True, fetch and return all results from the query.
                Defaults to False.

        Returns:
            Union[List[Any], bool]: A list of query results if return_response is True,
            or True if the query executed successfully.
        """
        with self.engine.connect() as connection:
            result: Result = connection.execute(text(sql_query))
            if return_response:
                return result.fetchall()
            connection.commit()
            return True

    def __test_engine(self) -> None:
        """
        Test the SQLAlchemy engine by executing a simple query.

        Runs a query against the INFORMATION_SCHEMA.TABLES to verify that the connection
        and engine are functioning correctly.
        """
        test_query = text(
            "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :schema"
        )
        with self.engine.connect() as connection:
            # This will raise an error if the engine cannot execute the query.
            connection.execute(test_query, {"schema": self.schema}).fetchall()

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the specified schema.

        Executes a query against INFORMATION_SCHEMA.TABLES to determine if a table with the
        given name exists within the schema.

        Args:
            table_name (str): The name of the table to check for existence.

        Returns:
            bool: True if the table exists; otherwise, False.
        """
        query = text(
            "SELECT * FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_NAME = :table_name AND TABLE_SCHEMA = :schema"
        )
        with self.engine.connect() as connection:
            result = connection.execute(query, {"table_name": table_name, "schema": self.schema})
            return bool(result.fetchall())

    def __enter__(self) -> "SQLAlchemyEngine":
        """Enable use of the engine with the 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Dispose of the engine when exiting the 'with' block."""
        self.engine.dispose()
