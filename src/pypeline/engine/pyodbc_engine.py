"""
Module for managing a database connection using pyodbc.

This module defines the PyodbcEngine class, which provides methods for creating
a connection to a database, executing queries, checking table existence, and
closing the connection.
"""

import pyodbc


class PyodbcEngine():
    """
    A database engine wrapper that uses pyodbc for connecting and executing SQL queries.

    This class encapsulates connection creation via DSN or individual connection parameters,
    and provides helper methods for query execution and connection management.
    """

    def __init__(self, SCHEMA, DSN=None, SERVER="", DATABASE="", DRIVER="", **kwargs):
        """
        Initialize a PyodbcEngine instance.

        Establishes a connection to the database using either a DSN or provided connection
        parameters. If a DSN is provided, the connection's driver, database, and server
        information are retrieved from the connection itself.

        Args:
            SCHEMA (str): The schema name to be used for database operations.
            DSN (str, optional): The Data Source Name for the connection. Defaults to None.
            SERVER (str, optional): The server name if DSN is not provided. Defaults to an empty string.
            DATABASE (str, optional): The database name if DSN is not provided. Defaults to an empty string.
            DRIVER (str, optional): The driver name if DSN is not provided. Defaults to an empty string.
            **kwargs: Additional keyword arguments (currently unused).
        """
        self.schema = SCHEMA
        self.dsn = DSN
        if self.dsn is not None:
            self.connection = self.create_pyodbc_connection()
            self.driver = self.connection.getinfo(pyodbc.SQL_DRIVER_NAME)
            self.database = self.connection.getinfo(pyodbc.SQL_DATABASE_NAME)
            self.server = self.connection.getinfo(pyodbc.SQL_SERVER_NAME)
        else:
            self.driver = DRIVER
            self.database = DATABASE
            self.server = SERVER
            self.connection = self.create_pyodbc_connection()
        self.cursor = self.connection.cursor()

    def create_pyodbc_connection(self):
        """
        Create and return a pyodbc connection based on the provided parameters.

        Returns:
            pyodbc.Connection: The established database connection.
        """
        if self.dsn is not None:
            return pyodbc.connect(f"DSN={self.dsn};", autocommit=True)
        return pyodbc.connect(
            f"""DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};SCHEMA={self.schema}""",
            autocommit=True
        )

    def close_connection(self):
        """
        Close the current database connection.

        This method should be called when the connection is no longer needed.
        """
        self.connection.close()

    def _execute_query(self, sql_query, return_response=False):
        """
        Execute a SQL query using the active connection's cursor.

        Args:
            sql_query (str): The SQL query to execute.
            return_response (bool, optional): If True, fetch and return all results of the query.
                Defaults to False.

        Returns:
            list or bool: A list of fetched results if return_response is True;
                          otherwise, True if the query executed successfully.
        """
        self.cursor.execute(sql_query)
        if return_response:
            return self.cursor.fetchall()
        return True

    def table_exists(self, table_name):
        """
        Check if a table exists in the specified schema.

        Args:
            table_name (str): The name of the table to check.

        Returns:
            bool: True if the table exists in the schema; otherwise, False.
        """
        sql_query = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name}' and TABLE_SCHEMA = '{self.schema}';
        """
        return False if self._execute_query(sql_query, True) == [] else True

    def __str__(self):
        """
        Return a string representation of the PyodbcEngine instance.

        This method prints the driver, schema, and database details, and returns the server name.

        Returns:
            str: The server name associated with the connection.
        """
        print(self.driver)
        print(self.schema)
        print(self.database)
        return self.server