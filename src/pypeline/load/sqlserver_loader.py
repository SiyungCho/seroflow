"""
Module: sqlserver_loader.py

This module provides concrete implementations for writing DataFrames to SQL server tables.
It defines two loader classes:
    - SQLServerLoader: A loader that writes a single DataFrame to a SQL server table.
    - MultiSQLServerLoader: A loader that handles writing multiple DataFrames to SQL server tables.
These classes extend the base Loader class and implement SQL server-specific functionality.
"""

from ..load.loader import Loader


class SQLServerLoader(Loader):
    """
    SQLServerLoader

    A concrete loader for writing a DataFrame to a SQL server table. This class extends Loader and provides methods
    to convert DataFrames into SQL server tables with the use of a predefined engine.
    """

    def __init__(self,
                 target,
                 engine,
                 dataframe,
                 schema=None,
                 step_name="SQLServerLoader",
                 exists="append",
                 on_error=None,
                 **kwargs):
        """
        CSVLoader Class Constructor
        Initializes the CSVLoader object.

        Arguments:
            target (str): 
                The target SQL server table names
            engine (Engine subclass): 
                An object containing the database engine and schema attributes.
            dataframe (DataFrame): 
                The DataFrame to be written to the SQL server table
            exists (str): 
                The file mode to use when writing the SQL server table
            step_name (str): 
                The name of the step
            on_error (str): 
                The error handling strategy
            **kwargs: 
                Additional keyword arguments for the to_sql() method
        """
        super().__init__(step_name=step_name,
                         dataframes=dataframe,
                         exists=exists,
                         func=self.func,
                         on_error=on_error)
        self.target = [target] if not isinstance(target, list) else target
        self.engine = engine
        self.kwargs = kwargs
        self.schema = schema if not hasattr(engine, "schema") else engine.schema

    def func(self, context):
        """
        Public method: func()
        Reads the DataFrame from the context and writes it to an SQL server table

        Arguments:
            context (Context): 
                The context object containing the dataframes to be written to the target 
        """
        for target, (_, df) in zip(self.target, context.dataframes.items()):
            full_schema = f"{self.engine.database}.{self.schema}"
            self.__to_sql(df, target, full_schema, self.engine.engine, self.kwargs)


    def __to_sql(self, df, target, schema, engine, kwargs):
        """
        Private method: __to_sql()
        Writes the DataFrame to a SQL server table

        Arguments:
            df (DataFrame): 
                The DataFrame to be written to the target 
            target (str): 
                The Table name of target
            schema (str):
                The schema location of the target formatted as: "db.schema"
            engine (Engine subclass):
                An object containing the database engine and schema attributes.
            kwargs (dict): 
                Additional keyword arguments for the to_sql() method
        """
        df.to_sql(target,
                  con=engine,
                  if_exists=self.map_exists_parameter(),
                  schema=schema,
                  **kwargs)

    def map_exists_parameter(self):
        """
        Public method: map_exists_parameter()
        Maps the exists parameter, No mapping required for this instance

        Returns:
            str (['error', 'replace', 'append'], None): 
        """
        return self.exists
