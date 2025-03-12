# """
# Module for managing a database connection using pyodbc.

# This module defines the PyodbcEngine class, which provides methods for creating
# a connection to a database, executing queries, checking table existence, and
# closing the connection.
# """

# from typing import Optional, Any, List
# import pyodbc

# class PyodbcEngine:
#     """
#     A database engine wrapper that uses pyodbc for connecting and executing SQL queries.

#     This class encapsulates connection creation via DSN or provided connection parameters,
#     and provides helper methods for query execution and connection management.
#     """

#     def __init__(
#         self,
#         schema: str,
#         dsn: Optional[str] = None,
#         server: str = "",
#         database: str = "",
#         driver: str = "",
#         **kwargs: Any
#     ) -> None:
#         """
#         Initialize a PyodbcEngine instance.

#         Establishes a connection to the database using either a DSN or provided connection
#         parameters. If a DSN is provided, the connection's driver, database, and server
#         information are retrieved from the connection itself.

#         Args:
#             schema (str): 
#                 The schema name to be used for database operations.
#             dsn (Optional[str]): 
#                 The Data Source Name for the connection. Defaults to None.
#             server (str, optional):
#                 The server name if DSN is not provided. Defaults to an empty string.
#             database (str, optional): 
#                 The database name if DSN is not provided. Defaults to an empty string.
#             driver (str, optional): 
#                 The driver name if DSN is not provided. Defaults to an empty string.
#             **kwargs: 
#                 Additional keyword arguments (currently unused).
#         """
#         self.schema: str = schema
#         self.dsn: Optional[str] = dsn
#         if self.dsn is not None:
#             self.connection = self.create_pyodbc_connection()
#             self.driver: str = self.connection.getinfo(pyodbc.SQL_DRIVER_NAME)
#             self.database: str = self.connection.getinfo(pyodbc.SQL_DATABASE_NAME)
#             self.server: str = self.connection.getinfo(pyodbc.SQL_SERVER_NAME)
#         else:
#             self.driver = driver
#             self.database = database
#             self.server = server
#             self.connection = self.create_pyodbc_connection()
#         self.cursor = self.connection.cursor()

#     def create_pyodbc_connection(self) -> pyodbc.Connection:
#         """
#         Create and return a pyodbc connection based on the provided parameters.

#         Returns:
#             pyodbc.Connection: The established database connection.
#         """
#         try:
#             if self.dsn is not None:
#                 return pyodbc.connect(f"DSN={self.dsn};", autocommit=True)
#             connection_string = (
#                 f"DRIVER={self.driver};"
#                 f"SERVER={self.server};"
#                 f"DATABASE={self.database};"
#                 f"SCHEMA={self.schema}"
#             )
#             return pyodbc.connect(connection_string, autocommit=True)
#         except pyodbc.Error as e:
#             raise RuntimeError("Error establishing connection to the database") from e

#     def close_connection(self) -> None:
#         """
#         Close the current database connection.

#         This method should be called when the connection is no longer needed.
#         """
#         if self.connection:
#             self.connection.close()

#     def _execute_query(self, sql_query: str, return_response: bool = False) -> Any:
#         """
#         Execute a SQL query using the active connection's cursor.

#         Args:
#             sql_query (str): The SQL query to execute.
#             return_response (bool, optional): If True, fetch and return all results of the query.
#                 Defaults to False.

#         Returns:
#             List[Any] or bool: A list of fetched results if return_response is True;
#                                otherwise, True if the query executed successfully.
#         """
#         self.cursor.execute(sql_query)
#         if return_response:
#             return self.cursor.fetchall()
#         return True

#     def table_exists(self, table_name: str) -> bool:
#         """
#         Check if a table exists in the specified schema.

#         Args:
#             table_name (str): The name of the table to check.

#         Returns:
#             bool: True if the table exists in the schema; otherwise, False.
#         """
#         sql_query = (
#             "SELECT * FROM INFORMATION_SCHEMA.TABLES "
#             "WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?;"
#         )
#         self.cursor.execute(sql_query, (table_name, self.schema))
#         results: List[Any] = self.cursor.fetchall()
#         return bool(results)

#     def __str__(self) -> str:
#         """
#         Return a string representation of the PyodbcEngine instance.

#         Returns:
#             str: A formatted string containing the connection details.
#         """
#         return (
#             f"Driver: {self.driver}, Schema: {self.schema}, "
#             f"Database: {self.database}, Server: {self.server}"
#         )

#     def __enter__(self) -> "PyodbcEngine":
#         """Enable usage with the 'with' statement."""
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb) -> None:
#         """Ensure the connection is closed when exiting a 'with' block."""
#         self.close_connection()
