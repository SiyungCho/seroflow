import sqlalchemy
from sqlalchemy import create_engine, text, URL
 
from ..Utils.utils import *
from ..Wrappers.wrappers import log_error
 
class sqlalchemy_engine():
    def __init__(self, SERVER, SCHEMA, DATABASE, DRIVER, fast_executemany = "yes", dialect = "mssql+pyodbc", port = None, username = "", password = "", trusted_connection = "yes", **kwargs):       
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
        connection_url = URL.create(
            self.dialect,
            username = self._username,
            password = self.__password,
            host = self.server,
            port = self.port,
            database = self.database,
            query = {
                'driver' : self.driver,
                'trusted_connection' : self.trusted_connection,
                **kwargs
            }
        )
        return connection_url
 
    def create_alchemy_engine(self):
        return create_engine(self.url, fast_executemany = self.fast_executemany)
 
    def _execute_query(self, sql_query, return_response = False):
        with self.engine.connect() as connection:
            result = connection.execute(text(sql_query))
            if return_response:
                response = result.fetchall()
                return response
            else:
                connection.commit()
                return True
 
    def __test_engine(self):
        sql_query = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{self.schema}'; """
        self._execute_query(sql_query)
 
    def table_exists(self, table_name):
        sql_query = f"""
        SELECT *
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name}' and TABLE_SCHEMA = '{self.schema}';
        """
        return False if self._execute_query(sql_query, True) == [] else True