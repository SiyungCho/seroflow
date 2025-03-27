# """Module: pyodbc_engine.py

# Provides a concrete Engine implementation using pyodbc for connecting to an
# ODBC data source. Defines PyodbcEngine, which manages connection creation,
# context management, and connection testing.
# """

# import pyodbc
# from .engine import Engine

# class PyodbcEngine(Engine):
#     """
#     Concrete Engine for pyodbc-based ODBC connections.

#     Extends the base Engine to create and test a pyodbc.Connection, expose a cursor,
#     and retrieve connection metadata when using a DSN.
#     """

#     def __init__(
#         self,
#         schema: str,
#         dsn: str = None,
#         server: str = "",
#         database: str = "",
#         driver: str = "",
#         **kwargs
#     ):
#         """
#         Initialize a PyodbcEngine.

#         Args:
#             schema (str): Database schema or owner.
#             dsn (str, optional): Data Source Name for ODBC. Defaults to None.
#             server (str): Server hostname or IP address.
#             database (str): Database name.
#             driver (str): ODBC driver name.
#             **kwargs: Additional keyword arguments passed to the base Engine.

#         Raises:
#             RuntimeError: If retrieving connection metadata via DSN fails.
#         """
#         connection_settings = {
#             "server": server,
#             "database": database,
#             "driver": driver,
#             "dsn": dsn
#         }

#         super().__init__(schema, connection_settings, engine_type="pyodbc", **kwargs)
#         self.cursor = self.engine.cursor()

#         if self.dsn is not None:
#             try:
#                 self.driver = self.engine.getinfo(pyodbc.SQL_DRIVER_NAME)
#                 self.database = self.engine.getinfo(pyodbc.SQL_DATABASE_NAME)
#                 self.server = self.engine.getinfo(pyodbc.SQL_SERVER_NAME)
#             except Exception as e:
#                 raise RuntimeError("Error retrieving connection details") from e

#     def create_engine(self):
#         """
#         Create and return a pyodbc.Connection using DSN or explicit connection settings.

#         Returns:
#             pyodbc.Connection: An active ODBC connection with autocommit enabled.

#         Raises:
#             RuntimeError: If establishing the connection fails.
#         """
#         try:
#             if self.dsn:
#                 connection_str = f"DSN={self.dsn};"
#             else:
#                 connection_str = (
#                     f"DRIVER={{{self.driver}}};"
#                     f"SERVER={self.server};"
#                     f"DATABASE={self.database};"
#                     f"SCHEMA={self.schema};"
#                 )
#             return pyodbc.connect(connection_str, autocommit=True)
#         except pyodbc.Error as e:
#             raise RuntimeError("Error establishing connection to the database") from e

#     def test_engine(self):
#         """
#         Validate the pyodbc connection by executing a simple query.

#         Raises:
#             RuntimeError: If the test query execution fails.
#         """
#         try:
#             self.engine.cursor().execute("SELECT 1")
#         except pyodbc.Error as e:
#             raise RuntimeError("Error testing the connection to the database") from e
