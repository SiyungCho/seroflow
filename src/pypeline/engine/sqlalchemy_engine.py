"""
"""

from .engine import Engine
from sqlalchemy import create_engine, text, URL


class SQLAlchemyEngine(Engine):
    """
    """

    def __init__(
        self,
        schema,
        server,
        database,
        driver,
        fast_executemany="yes",
        dialect="mssql+pyodbc",
        port=None,
        username="",
        password="",
        trusted_connection="yes",
        **kwargs,
    ):
        """
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
            "trusted_connection": trusted_connection
        }
        super().__init__(schema, connection_settings, "sqlalchemy", **kwargs)

    def __create_engine(self):
        """
        """
        self.url = self.create_url()
        return self.create_alchemy_engine()
    
    def __test_engine(self):
        """
        """
        test_query = text(
            "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :schema"
        )
        with self.engine.connect() as connection:
            # This will raise an error if the engine cannot execute the query.
            connection.execute(test_query, {"schema": self.schema}).fetchall()
        
    def create_url(self):
        """
        """
        query = {
            "driver": self.driver,
            "trusted_connection": str(self.trusted_connection).lower()
        }
        query.update(**self.kwargs)
        connection_url = URL.create(
            self.dialect,
            username=self.username,
            password=self.password,
            host=self.server,
            port=self.port,
            database=self.database,
            query=query
        )
        return connection_url

    def create_alchemy_engine(self):
        """
        """
        return create_engine(self.url, fast_executemany=self.fast_executemany)
