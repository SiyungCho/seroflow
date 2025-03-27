# """
# Module for managing SQL database connections using either SQLAlchemy or pyodbc.

# This module provides the UniversalEngine class, which encapsulates the creation of a
# database connection, execution of SQL queries, and helper functions for operations
# such as checking for table existence. The backend (SQLAlchemy or pyodbc) can be chosen
# via a parameter.
# """
# from typing import Any, Dict, List, Optional, Union
# import pyodbc
# from sqlalchemy import create_engine, text, URL
# from sqlalchemy.engine import Engine, URL as SQLAlchemyURL, Result

# class UniversalEngine:
#     """
#     A universal database engine wrapper that supports either SQLAlchemy or pyodbc.

#     This class creates a connection based on the provided parameters and backend choice.
#     It exposes a unified interface for executing queries and checking for table existence.
#     """

#     def __init__(
#         self,
#         backend: str = "sqlalchemy",
#         # Common parameters:
#         server: str = "",
#         schema: str = "",
#         database: str = "",
#         driver: str = "",
#         # For pyodbc:
#         dsn: Optional[str] = None,
#         # For SQLAlchemy:
#         fast_executemany: Union[bool, str] = "yes",
#         dialect: str = "mssql+pyodbc",
#         port: Optional[int] = None,
#         username: str = "",
#         password: str = "",
#         trusted_connection: str = "yes",
#         **kwargs: Any,
#     ) -> None:
#         """
#         Initialize a UniversalEngine instance.

#         Args:
#             backend (str): Choose the backend: either 'sqlalchemy' or 'pyodbc'.
#             server (str): The database server address.
#             schema (str): The schema name to use.
#             database (str): The name of the database.
#             driver (str): The database driver.
#             dsn (Optional[str]): DSN for pyodbc connections. If provided, it takes precedence.
#             fast_executemany (Union[bool, str], optional):
#               For SQLAlchemy, option to enable fast executemany. Defaults to "yes".
#             dialect (str, optional): SQLAlchemy dialect to use. Defaults to "mssql+pyodbc".
#             port (Optional[int], optional): The port number for the server.
#             username (str, optional): Username for authentication (SQLAlchemy).
#             password (str, optional): Password for authentication (SQLAlchemy).
#             trusted_connection (str, optional): Whether to use a trusted connection (SQLAlchemy).
#             **kwargs: Additional keyword arguments for connection configuration.
#         """
#         self.backend = backend.lower()
#         self.schema = schema

#         if self.backend == "sqlalchemy":
#             self.driver = driver
#             self.server = server
#             self.database = database
#             self.dialect = dialect
#             self.port = port
#             self._username = username
#             self.__password = password
#             self.trusted_connection = trusted_connection
#             self.fast_executemany = fast_executemany
#             self.url: SQLAlchemyURL = self._create_sqlalchemy_url(kwargs)
#             self.engine: Engine = create_engine(self.url, fast_executemany=self.fast_executemany)
#         elif self.backend == "pyodbc":
#             self.dsn = dsn
#             self.driver = driver
#             self.server = server
#             self.database = database
#             if self.dsn is not None:
#                 self.connection = pyodbc.connect(f"DSN={self.dsn};", autocommit=True)
#                 # Retrieve additional info from the connection
#                 self.driver = self.connection.getinfo(pyodbc.SQL_DRIVER_NAME)
#                 self.database = self.connection.getinfo(pyodbc.SQL_DATABASE_NAME)
#                 self.server = self.connection.getinfo(pyodbc.SQL_SERVER_NAME)
#             else:
#                 connection_str = (
#                     f"DRIVER={driver};"
#                     f"SERVER={server};"
#                     f"DATABASE={database};"
#                     f"SCHEMA={schema}"
#                 )
#                 self.connection = pyodbc.connect(connection_str, autocommit=True)
#             self.cursor = self.connection.cursor()
#         else:
#             raise ValueError("Invalid backend. Choose either 'sqlalchemy' or 'pyodbc'.")

#         # Optionally test the connection on initialization.
#         self._test_connection()

#     def _create_sqlalchemy_url(self, kwargs: Dict[str, Any]) -> SQLAlchemyURL:
#         """
#         Create a SQLAlchemy URL using the provided parameters.

#         Args:
#             kwargs (Dict[str, Any]): Additional query parameters for the URL.

#         Returns:
#             SQLAlchemyURL: A URL object representing the connection.
#         """
#         return URL.create(
#             self.dialect,
#             username=self._username,
#             password=self.__password,
#             host=self.server,
#             port=self.port,
#             database=self.database,
#             query={
#                 "driver": self.driver,
#                 "trusted_connection": self.trusted_connection,
#                 **kwargs,
#             },
#         )

#     def _test_connection(self) -> None:
#         """
#         Test the connection by executing a simple query.
#         """
#         self.execute_query("SELECT 1")

    # def execute_query(self,
    #                   sql_query: str,
    #                   return_response: bool = False) -> Union[List[Any], bool]:
#         """
#         Execute a SQL query.

#         Args:
#             sql_query (str): The SQL query to execute.
#             return_response (bool, optional):
#                   If True, return all fetched results. Defaults to False.

#         Returns:
#             Union[List[Any], bool]:
#               A list of results if return_response is True; otherwise, True on success.
#         """
#         if self.backend == "sqlalchemy":
#             with self.engine.connect() as connection:
#                 result: Result = connection.execute(text(sql_query))
#                 if return_response:
#                     return result.fetchall()
#                 else:
#                     connection.commit()
#                     return True
#         elif self.backend == "pyodbc":
#             self.cursor.execute(sql_query)
#             if return_response:
#                 return self.cursor.fetchall()
#             return True

#     def table_exists(self, table_name: str) -> bool:
#         """
#         Check if a table exists in the schema.

#         Args:
#             table_name (str): The table name to check.

#         Returns:
#             bool: True if the table exists; False otherwise.
#         """
#         if self.backend == "sqlalchemy":
#             query = text(
#                 "SELECT * FROM INFORMATION_SCHEMA.TABLES "
#                 "WHERE TABLE_NAME = :table_name AND TABLE_SCHEMA = :schema"
#             )
#             with self.engine.connect() as connection:
#                 result = connection.execute(query,
#                                             {"table_name": table_name,
#                                              "schema": self.schema})
#                 return bool(result.fetchall())
#         elif self.backend == "pyodbc":
#             query = (
#                 "SELECT * FROM INFORMATION_SCHEMA.TABLES "
#                 "WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?"
#             )
#             self.cursor.execute(query, (table_name, self.schema))
#             return bool(self.cursor.fetchall())

#     def close(self) -> None:
#         """
#         Close the connection/engine.
#         """
#         if self.backend == "sqlalchemy":
#             self.engine.dispose()
#         elif self.backend == "pyodbc":
#             self.connection.close()

#     def __enter__(self) -> "UniversalEngine":
#         """
#         Enter the runtime context related to this object.
#         """
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb) -> None:
#         """
#         Exit the runtime context and close the connection.
#         """
#         self.close()

#     def __str__(self) -> str:
#         """
#         Return a string representation of the UniversalEngine.
#         """
#         if self.backend == "sqlalchemy":
#             return (
#                 f"SQLAlchemyEngine(server={self.server}, schema={self.schema}, "
#                 f"database={self.database}, driver={self.driver})"
#             )
#         elif self.backend == "pyodbc":
#             return (
#                 f"PyodbcEngine(server={self.server}, schema={self.schema}, "
#                 f"database={self.database}, driver={self.driver})"
#             )
