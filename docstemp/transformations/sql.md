# SQL Transformations Documentation

This module implements a transformation class for executing SQL queries on DataFrames using the pandasql library. Each transformation class extends the base `Transformation` class and operates on DataFrames stored in the `Pipeline` context. The available transformation is:

- **SQLQuery**: Executes a SQL query against one or more DataFrames in the context and stores the result under a specified key.

## SQLQuery

- **Purpose**: Runs a SQL query on DataFrames in the `Pipeline` context using pandasql’s `sqldf`.
- **Parameters**:
  - `query` (str): The SQL query string. DataFrames may be referenced by their context keys.
  - `output_dataframe_name` (str): The context key under which to store the query result.
  - `step_name` (str, optional): Name of this transformation step. Defaults to `"SQLQuery"`.
  - `on_error` (str, optional): Error handling strategy.

## SQLQuery Example

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import SQLQuery

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Extractor extracts 'customers' and 'orders'
  # SQL query to join customers and orders and aggregate total spend
  query = """
  SELECT c.customer_id,
        c.name,
        SUM(o.amount) AS total_amount
  FROM customers AS c
  JOIN orders AS o
    ON c.customer_id = o.customer_id
  GROUP BY c.customer_id, c.name
  """

  sql_step = SQLQuery(
      query=query,
      output_dataframe_name="customer_summary"
  )

  pipeline.add_steps([sql_step])
  pipeline.execute()
```