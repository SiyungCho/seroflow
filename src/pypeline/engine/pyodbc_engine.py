"""
"""

import pyodbc
from .engine import Engine

class PyodbcEngine(Engine):
    """
    """

    def __init__(self, schema, dsn=None, server="", database="", driver="", **kwargs):
        """
        """
        connection_settings = {
            "server": server,
            "database": database,
            "driver": driver,
            "dsn": dsn
        }

        super().__init__(schema, connection_settings, "pyodbc", **kwargs)
        self.cursor = self.engine.cursor()

        if self.dsn is not None:
            try:
                self.driver = self.engine.getinfo(pyodbc.SQL_DRIVER_NAME)
                self.database = self.engine.getinfo(pyodbc.SQL_DATABASE_NAME)
                self.server = self.engine.getinfo(pyodbc.SQL_SERVER_NAME)
            except Exception as e:
                raise RuntimeError("Error retrieving connection details") from e

    def create_engine(self):
        """
        """
        try:
            if self.dsn:
                connection_str = f"DSN={self.dsn};"
            else:
                connection_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"SCHEMA={self.schema};"
                )
            return pyodbc.connect(connection_str, autocommit=True)
        except pyodbc.Error as e:
            raise RuntimeError("Error establishing connection to the database") from e
    
    def test_engine(self):
        """
        """
        try:
            self.engine.cursor().execute("SELECT 1")
        except pyodbc.Error as e:
            raise RuntimeError("Error testing the connection to the database") from e
