import pyodbc

from ..Utils.utils import *
from ..Wrappers.wrappers import log_error
 
class pyodbc_engine():
    def __init__(self, SCHEMA, DSN=None, SERVER="", DATABASE="", DRIVER="", **kwargs): #somehow get kwargs
 
        self.schema = SCHEMA
        self.dsn = DSN
        if self.dsn != None:
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
        # self.__test_engine()
 
    def create_pyodbc_connection(self):
        if self.dsn != None:
            return pyodbc.connect(f"DSN={self.dsn};", autocommit=True)
        return pyodbc.connect(f"""DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};SCHEMA={self.schema}""", autocommit=True)
 
    def close_connection(self):
        self.connection.close()
 
    def _execute_query(self, sql_query, return_response = False):
        self.cursor.execute(sql_query)
        if return_response:
            return self.cursor.fetchall()
        return True
 
    # def __test_engine(self):
    #     sql_query = f"""
    #     SELECT *
    #     FROM INFORMATION_SCHEMA.TABLES
    #     WHERE TABLE_SCHEMA = '{self.schema}'; """
    #     self._execute_query(sql_query)
 
    def table_exists(self, table_name):
        sql_query = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name}' and TABLE_SCHEMA = '{self.schema}';
        """
        return False if self._execute_query(sql_query, True) == [] else True
 
    def __str__(self):
        print(self.driver)
        print(self.schema)
        print(self.database)
        return self.server