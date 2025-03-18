# SQL Transformations Module Documentation

This module provides a transformation class for executing SQL queries on DataFrames using the pandasql library. The `SQLQuery` transformation enables users to run SQL commands against the DataFrames stored in the pypeline context by referencing them by their keys. The result of the SQL query is stored in the context under a specified output name.

---

## Overview

The `SQLQuery` transformation leverages the pandasql library to execute SQL queries on the DataFrames present in the pypeline context. It allows you to perform complex data manipulations using SQL syntax and then updates the context with the query result.

---

## Class: SQLQuery

### Description

The `SQLQuery` class executes a SQL query on the DataFrames in the context. The query can reference any DataFrame in the context by its key. The result of the query is stored in the context under a user-specified key.

### Attributes

- **query** (*str*):  
  The SQL query to execute. The query may reference DataFrames in the context by their keys.

- **output_dataframe_name** (*str*):  
  The key under which the query result will be stored in the context.

### Constructor

#### `__init__(self, query, output_dataframe_name, step_name="SQLQuery", on_error=None)`

- **Arguments:**
  - `query` (*str*): The SQL query to execute.
  - `output_dataframe_name` (*str*): The key for storing the query result in the context.
  - `step_name` (*str*, optional): The name of this transformation step. Defaults to `"SQLQuery"`.
  - `on_error` (*str*, optional): The error handling strategy.

- **Behavior:**
  - Initializes the transformation with the provided query and output name.
  - Sets up the transformation to execute the SQL query using the pandasql library.

### Methods

#### `func(self, context)`

- **Purpose:**  
  Executes the SQL query against the DataFrames in the pypeline context.

- **Arguments:**
  - `context` (*Context*): The context object that contains the DataFrames.

- **Behavior:**
  - Uses `pandasql.sqldf` to execute the SQL query, passing the context's DataFrames as the namespace.
  - Stores the resulting DataFrame in the context under the key specified by `output_dataframe_name`.
  - Returns the updated context.

- **Returns:**
  - The updated context with the SQL query result added.

---

## Usage Example

Below is an example demonstrating how to use the `SQLQuery` transformation within a pypeline context:

```python
import pandas as pd
from sql import SQLQuery
from pypeline import Pypeline

# Create sample DataFrames
df_customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})
df_orders = pd.DataFrame({
    'order_id': [101, 102, 103],
    'customer_id': [1, 2, 1],
    'amount': [250, 150, 300]
})

# Dummy context simulating a pypeline context
class DummyContext:
    def __init__(self):
        self.dataframes = {
            "customers": df_customers,
            "orders": df_orders
        }
    def set_dataframe(self, name, df):
        self.dataframes[name] = df

context = DummyContext()

# Define a SQL query to join customers and orders
query = """
SELECT c.customer_id, c.name, SUM(o.amount) as total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
"""

# Initialize the SQLQuery transformation
sql_transform = SQLQuery(query=query, output_dataframe_name="customer_summary")

# Execute the transformation
updated_context = sql_transform.func(context)

# Display the result stored in the context
print(updated_context.dataframes["customer_summary"])