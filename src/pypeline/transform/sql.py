"""
Module: sql.py

This module provides a transformation class for executing SQL queries using the pandasql library on DataFrames.
The SQLQuery transformation enables users to run SQL commands against the dataframes by referencing them by their
keys within the context, and it stores the query result in the context under a specified name.
"""

#store result in variable

import pandasql as sqldf
from .transformation import Transformation

class SQLQuery(Transformation):
    """
    SQLQuery Transformation

    Executes a SQL query using the pandasql library on DataFrames contained in the pypeline context.
    The SQL query can reference any DataFrame in the context by its key. The result of the query is stored
    in the context under the provided output DataFrame name.
    """
    def __init__(self,
                 query,
                 output_dataframe_name,
                 step_name="SQLQuery",
                 on_error=None):
        """
        Initializes the SQLQuery transformation.

        Arguments:
            query (str): The SQL query to be executed. The query can reference DataFrames in the context by their keys.
            output_dataframe_name (str): The key under which the query result will be stored in the context.
            step_name (str, optional): The name of this transformation step. Defaults to "SQLQuery".
            on_error (str, optional): The error handling strategy.
        """
        self.query = query
        self.output_dataframe_name = output_dataframe_name
        super().__init__(step_name=step_name,
                         func=self.func,
                         on_error=on_error)

    def func(self, context):
        """
        Executes the SQL query on the DataFrames in the context.

        Uses the pandasql library to execute the provided SQL query, treating the context's dataframes as the namespace.
        The resulting DataFrame is then added to the context under the specified output name.

        Arguments:
            context (Context): The context object containing the DataFrames.

        Returns:
            Context: The updated context with the SQL query result added.
        """
        result = sqldf.sqldf(self.query, context.dataframes)
        context.set_dataframe(self.output_dataframe_name, result)
        return context
