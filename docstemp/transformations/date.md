# Date Transformations Documentation

This module implements transformation classes for converting columns in a DataFrame to datetime format. Each transformation class extends the base `Transformation` class and operates on a specified DataFrame stored in the `Pipeline` context. The available transformations are:

- **ConvertToDateTime**: Converts a specified column to pandas datetime format, with optional format parsing.

## Date Transformation Classes

### ConvertToDateTime

- **Purpose**: Converts a specified column in a DataFrame to datetime dtype using pandas’ to_datetime.
- **Parameters**:
  - `dataframe` (*str*): Name of the DataFrame in the `Pipeline` context.
  - `column` (*str*): Column to convert to datetime.
  - `format` (*str*, optional): A datetime format string for parsing (e.g., "%Y-%m-%d"). Defaults to None.
  - `step_name` (*str*, optional): Name of the transformation step. Defaults to "ConvertToDateTime".
  - `on_error` (*str*, optional): Error handling strategy.

#### ConvertToDateTime Example

Below is an example demonstrating how to use the Transformation `ConvertToDateTime`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import ConvertToDateTime

  # Create a Pipeline and register the DataFrame under the name 'sales_data'
  pipeline = Pipeline()
  pipeline.target_extractor = ...

  # Initialize the ConvertToDateTime transformation to convert 'order_date' to datetime
  convert_dates = ConvertToDateTime(
      dataframe="sales_data",
      column="order_date",
      format="%Y-%m-%d"
  )

  pipeline.add_steps([convert_dates])
  pipeline.execute()
```

---
