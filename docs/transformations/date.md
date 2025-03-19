# Date Transformations Module Documentation

This module implements transformation classes for converting columns in a DataFrame to datetime format. It provides functionality to convert a specified column to a datetime type using pandas' `to_datetime` method, allowing for an optional format parameter to guide the conversion.

---

## Overview

The module defines the `ConvertToDateTime` transformation class that extends the base `Transformation` class. This transformation retrieves a target DataFrame from the pypeline context, converts a designated column to datetime format (using an optional format if provided), updates the DataFrame in the context, and returns the updated context.

---

## Class: ConvertToDateTime

### Description

The `ConvertToDateTime` class converts a specified column in a DataFrame to datetime format. It leverages pandas' `to_datetime` to perform the conversion. If a format is provided, it is used for parsing; otherwise, pandas' default parser is used.

### Attributes

- **dataframe** (*str*):  
  The name of the DataFrame in the context.

- **column** (*str*):  
  The name of the column to convert.

- **format** (*str*, optional):  
  The datetime format to use for conversion (if provided).

### Methods

#### `__init__(self, dataframe, column, format=None, step_name="ConvertToDateTime", on_error=None)`

Initializes the `ConvertToDateTime` transformation.

- **Arguments:**
  - `dataframe` (*str*): The name of the DataFrame to update in the context.
  - `column` (*str*): The column in the DataFrame that will be converted to datetime.
  - `format` (*str*, optional): The datetime format to use for conversion. Defaults to `None`.
  - `step_name` (*str*, optional): The name of this transformation step. Defaults to `"ConvertToDateTime"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### `func(self, context)`

Executes the ConvertToDateTime transformation.

- **Behavior:**
  - Retrieves the specified DataFrame from the context.
  - Converts the designated column to datetime format using the provided format (if available) or default parsing.
  - Updates the DataFrame in the context.
  - Returns the updated context.

- **Arguments:**
  - `context` (*Context*): The pypeline context containing the DataFrame.

- **Returns:**
  - The updated context with the specified column converted to datetime.

#### `__convert_to_datetime(self, df)`

Converts the specified column of the DataFrame to datetime format.

- **Arguments:**
  - `df` (*DataFrame*): The DataFrame to process.
- **Returns:**
  - The DataFrame with the designated column converted to datetime format.

---

## Usage Example

Below is an example demonstrating how to use the `ConvertToDateTime` transformation within a pypeline context:

```python
import pandas as pd
from date import ConvertToDateTime

# Create a sample DataFrame with date strings
df_sample = pd.DataFrame({
    'date_str': ['2023-01-01', '2023-02-01', '2023-03-01']
})

# Dummy context to simulate a pypeline context
class DummyContext:
    def __init__(self):
        self.dataframes = {"sales": df_sample}
    def set_dataframe(self, name, df):
        self.dataframes[name] = df

context = DummyContext()

# Initialize the transformation to convert 'date_str' column to datetime
convert_datetime = ConvertToDateTime(dataframe="sales", column="date_str", format="%Y-%m-%d")

# Execute the transformation
updated_context = convert_datetime.func(context)

# Print the data types of the updated DataFrame to verify conversion
print(updated_context.dataframes["sales"].dtypes)