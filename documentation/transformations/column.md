# Column Transformations Module Documentation

This module implements a collection of transformation classes that perform various column operations on DataFrames. These transformations update the DataFrame stored in the pypeline context. Each transformation class extends the base `Transformation` class and provides a specific column operation.

---

## Overview

The available transformation classes include:

- **ConvertColumnType**: Converts a specified column of a DataFrame to a new data type.
- **RenameColumns**: Renames one or more columns based on a provided mapping.
- **DropColumn**: Drops a single specified column from a DataFrame.
- **DropColumns**: Drops multiple specified columns from a DataFrame.
- **AddColumn**: Adds a new column to a DataFrame computed from a function.
- **MergeColumns**: Merges multiple columns into a single column by concatenating their string representations.
- **SplitColumn**: Splits a single column into multiple new columns based on a delimiter.
- **ExplodeColumn**: Explodes a column containing list-like elements into multiple rows.
- **CreateColumnFromVariable**: Creates a new column in a DataFrame using a constant value provided via a variable.

Each transformation retrieves the target DataFrame from the pypeline context, performs the operation, updates the DataFrame, and returns the modified context.

---

## Transformation Classes

### ConvertColumnType

**Description**:  
Converts a specified column to a new data type.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame in the context.
- `column` (str): The column to be converted.
- `new_type` (type): The target data type.
- `step_name` (str, optional): Defaults to `"ConvertColumnType"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame from `context`, converts the column type, updates the DataFrame, and returns the context.

---

### RenameColumns

**Description**:  
Renames one or more columns in a DataFrame using a provided mapping.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `columns_mapping` (dict): Mapping of current column names to new names.
- `step_name` (str, optional): Defaults to `"RenameColumns"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, renames columns, updates the DataFrame in the context, and returns the context.

---

### DropColumn

**Description**:  
Drops a specified column from a DataFrame.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `column` (str): The column to drop.
- `step_name` (str, optional): Defaults to `"DropColumn"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, drops the specified column, updates the DataFrame in the context, and returns the context.

---

### DropColumns

**Description**:  
Drops multiple specified columns from a DataFrame.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `columns` (list): List of columns to drop.
- `step_name` (str, optional): Defaults to `"DropColumns"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, drops the specified columns (ignoring errors for missing columns), updates the DataFrame in the context, and returns the context.

---

### AddColumn

**Description**:  
Adds a new column computed from a provided function.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `column` (str): Name of the new column.
- `compute_func` (function): Function that computes the column’s values from the DataFrame.
- `step_name` (str, optional): Defaults to `"AddColumn"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, computes the new column using `compute_func`, adds the new column, updates the context, and returns it.

---

### MergeColumns

**Description**:  
Merges multiple columns into a single column by concatenating their string representations.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `columns` (list): List of columns to merge.
- `new_column` (str): Name of the resulting merged column.
- `separator` (str, optional): Separator to use between values (default is a space).
- `step_name` (str, optional): Defaults to `"MergeColumns"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, concatenates the specified columns using the separator, adds the new merged column, updates the DataFrame, and returns the context.

---

### SplitColumn

**Description**:  
Splits a single column into multiple new columns based on a delimiter.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `column` (str): The column to split.
- `new_columns` (list): List of new column names.
- `delimiter` (str, optional): Delimiter to use for splitting (default is a space).
- `step_name` (str, optional): Defaults to `"SplitColumn"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, splits the column into multiple columns, concatenates them with the original DataFrame, updates the context, and returns it.

---

### ExplodeColumn

**Description**:  
Explodes a column containing list-like elements into multiple rows, duplicating the other column values.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `column` (str): The column to explode.
- `step_name` (str, optional): Defaults to `"ExplodeColumn"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, explodes the specified column, updates the context, and returns it.

---

### CreateColumnFromVariable

**Description**:  
Creates a new column in a DataFrame using a constant value provided via a variable.

**Constructor Arguments**:
- `dataframe` (str): Name of the DataFrame.
- `column` (str): Name of the new column.
- `variable`: The constant value to assign to the new column.
- `step_name` (str, optional): Defaults to `"CreateColumnFromVariable"`.
- `on_error` (str, optional): The error handling strategy.

**Method**:
- `func(context, **kwargs)`: Retrieves the DataFrame, creates a new column with the constant value (passed via keyword arguments), updates the context, and returns it.

---

## Usage Example

Below is an example demonstrating how to use one of these transformation classes (e.g., `ConvertColumnType`) within a pypeline context:

```python
import pandas as pd
from column import ConvertColumnType
from pypeline import Pypeline

# Create a sample DataFrame
df_sample = pd.DataFrame({
    'age': ['25', '30', '45'],
    'name': ['Alice', 'Bob', 'Charlie']
})

# Assume a pypeline context that holds dataframes
class DummyContext:
    def __init__(self):
        self.dataframes = {"people": df_sample}

    def set_dataframe(self, name, df):
        self.dataframes[name] = df

# Create a dummy context instance
context = DummyContext()

# Initialize the transformation to convert 'age' column to integer
convert_type = ConvertColumnType(dataframe="people", column="age", new_type=int)

# Execute the transformation
updated_context = convert_type.func(context)

# Verify the change
print(updated_context.dataframes["people"].dtypes)