"""
Module for managing SQL database connections using SQLAlchemy.

This module provides the SQLAlchemyEngine class, which encapsulates the creation of a
SQLAlchemy engine, execution of SQL queries, and helper functions for database operations
such as checking for table existence.
"""

from sqlalchemy import create_engine, text, URL


class SQLAlchemyEngine():
    """
    A database engine wrapper using SQLAlchemy.

    This class creates a SQLAlchemy engine using the provided connection parameters,
    executes SQL queries, and provides helper methods such as checking if a table exists.
    """

    def __init__(self, SERVER, SCHEMA, DATABASE, DRIVER, fast_executemany="yes",
                 dialect="mssql+pyodbc", port=None, username="", password="",
                 trusted_connection="yes", **kwargs):
        """
        Initialize a SQLAlchemyEngine instance.

        Sets up connection parameters, creates the connection URL and SQLAlchemy engine,
        and tests the engine by executing a simple query.

        Args:
            SERVER (str): The database server address.
            SCHEMA (str): The schema name to use.
            DATABASE (str): The name of the database.
            DRIVER (str): The database driver to use.
            fast_executemany (str, optional): Option to enable fast executemany. Defaults to "yes".
            dialect (str, optional): SQLAlchemy dialect to use. Defaults to "mssql+pyodbc".
            port (int, optional): The port number for the server. Defaults to None.
            username (str, optional): The username for authentication. Defaults to "".
            password (str, optional): The password for authentication. Defaults to "".
            trusted_connection (str, optional): Whether to use a trusted connection. Defaults to "yes".
            **kwargs: Additional keyword arguments for URL query parameters.
        """
        self.driver = DRIVER
        self.schema = SCHEMA
        self.database = DATABASE
        self.server = SERVER
        self.dialect = dialect
        self.port = port
        self._username = username
        self.__password = password
        self.trusted_connection = trusted_connection
        self.fast_executemany = fast_executemany

        self.url = self.create_url(kwargs)
        self.engine = self.create_alchemy_engine()
        self.__test_engine()

    def create_url(self, kwargs):
        """
        Create and return a SQLAlchemy URL for the database connection.

        Constructs a URL using the provided connection parameters and additional query
        arguments.

        Args:
            kwargs (dict): Additional query parameters to include in the URL.

        Returns:
            sqlalchemy.engine.URL: A URL object representing the database connection.
        """
        connection_url = URL.create(
            self.dialect,
            username=self._username,
            password=self.__password,
            host=self.server,
            port=self.port,
            database=self.database,
            query={
                'driver': self.driver,
                'trusted_connection': self.trusted_connection,
                **kwargs
            }
        )
        return connection_url

    def create_alchemy_engine(self):
        """
        Create and return a SQLAlchemy engine using the constructed URL.

        Returns:
            sqlalchemy.engine.Engine: An instance of a SQLAlchemy engine.
        """
        return create_engine(self.url, fast_executemany=self.fast_executemany)

    def _execute_query(self, sql_query, return_response=False):
        """
        Execute a SQL query using the SQLAlchemy engine.

        Args:
            sql_query (str): The SQL query to execute.
            return_response (bool, optional): If True, fetch and return all results from the query.
                Defaults to False.

        Returns:
            list or bool: A list of query results if return_response is True, or True if the
                          query executed successfully.
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(sql_query))
            if return_response:
                response = result.fetchall()
                return response
            else:
                connection.commit()
                return True

    def __test_engine(self):
        """
        Test the SQLAlchemy engine by executing a simple query.

        Runs a query against the INFORMATION_SCHEMA.TABLES to verify that the connection
        and engine are functioning correctly.
        """
        sql_query = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{self.schema}'; """
        self._execute_query(sql_query)

    def table_exists(self, table_name):
        """
        Check if a table exists in the specified schema.

        Executes a query against INFORMATION_SCHEMA.TABLES to determine if a table with the
        given name exists within the schema.

        Args:
            table_name (str): The name of the table to check for existence.

        Returns:
            bool: True if the table exists; otherwise, False.
        """
        sql_query = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name}' and TABLE_SCHEMA = '{self.schema}';
        """
        return False if self._execute_query(sql_query, True) == [] else True