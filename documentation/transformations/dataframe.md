# DataFrame Transformations Module Documentation

This module implements a collection of transformation classes that perform various operations on DataFrames. Each transformation class extends the base `Transformation` class and updates the DataFrame stored in the pypeline context accordingly.

---

## Overview

The following transformation classes are available in this module:

- **TransposeDataFrame**: Transposes the DataFrame.
- **PivotDataFrame**: Creates a pivot table from a DataFrame.
- **MeltDataFrame**: Unpivots a DataFrame from wide to long format.
- **GroupByAggregate**: Groups a DataFrame by specified columns and aggregates using provided functions.
- **FilterRows**: Filters rows based on a boolean function.
- **SortDataFrame**: Sorts a DataFrame by one or more columns.
- **DropDuplicates**: Removes duplicate rows from a DataFrame.
- **SelectColumns**: Selects a subset of columns from a DataFrame.
- **FillNAValues**: Fills missing (NA) values with a specified fill value.
- **ReplaceValues**: Replaces specified values in a DataFrame with a new value.
- **MergeDataFrames**: Merges two DataFrames based on specified keys and merge strategy.
- **JoinDataFrames**: Joins two DataFrames using the pandas join method.
- **ApplyFunction**: Applies a function to an entire DataFrame or a specified column.
- **ApplyMap**: Applies a function element-wise to a DataFrame.
- **MapValues**: Maps values in a specified column based on a provided dictionary.
- **OneHotEncode**: Performs one-hot encoding on a categorical column.

Each transformation retrieves the target DataFrame from the pypeline context, applies the desired operation, updates the DataFrame, and returns the modified context.

---

## Transformation Classes

### TransposeDataFrame

**Description**:  
Transposes the specified DataFrame using pandas' transpose method. The transposed DataFrame replaces the original in the context.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame in the context to be transposed.
- `step_name` (*str*, optional): Defaults to `"TransposeDataFrame"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, transposes it, updates the context, and returns the modified context.

---

### PivotDataFrame

**Description**:  
Creates a pivot table from a DataFrame using specified index, columns, values, and an aggregation function. The resulting pivot table is added to the context.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `index` (*str or list*): Column(s) to set as the pivot table index.
- `columns` (*str or list*): Column(s) to pivot.
- `values` (*str*): Column to aggregate.
- `aggfunc` (*str or function*, optional): Aggregation function to apply (default is `'mean'`).
- `step_name` (*str*, optional): Defaults to `"PivotDataFrame"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, creates a pivot table, updates the context, and returns it.

---

### MeltDataFrame

**Description**:  
Unpivots a DataFrame from wide to long format using pandas' `melt` function. The melted DataFrame is updated in the context.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `id_vars` (*str or list*): Identifier variable(s) that will remain unpivoted.
- `value_vars` (*str or list*): Column(s) to unpivot.
- `var_name` (*str*, optional): Name for the variable column (default is `"variable"`).
- `value_name` (*str*, optional): Name for the value column (default is `"value"`).
- `step_name` (*str*, optional): Defaults to `"MeltDataFrame"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, melts it, updates the context, and returns it.

---

### GroupByAggregate

**Description**:  
Groups a DataFrame by specified column(s) and aggregates other columns using provided functions. The resulting aggregated DataFrame is updated in the context.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `groupby_columns` (*str or list*): Column(s) to group by.
- `agg_dict` (*dict*): Dictionary specifying aggregation functions for columns.
- `step_name` (*str*, optional): Defaults to `"GroupByAggregate"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, applies groupby and aggregation, updates the context, and returns it.

---

### FilterRows

**Description**:  
Filters rows in a DataFrame based on a provided boolean function. The function should accept a DataFrame and return a boolean Series used for filtering.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `filter_func` (*function*): Function that returns a boolean Series for filtering rows.
- `step_name` (*str*, optional): Defaults to `"FilterRows"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, applies the filter, updates the context, and returns it.

---

### SortDataFrame

**Description**:  
Sorts a DataFrame by one or more specified columns.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `by` (*str or list*): Column(s) to sort by.
- `ascending` (*bool*, optional): Sort order (default is `True` for ascending).
- `step_name` (*str*, optional): Defaults to `"SortDataFrame"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, sorts it, updates the context, and returns it.

---

### DropDuplicates

**Description**:  
Removes duplicate rows from a DataFrame based on specified subset columns.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `subset` (*str or list*, optional): Columns to consider for identifying duplicates.
- `keep` (*str*, optional): Which duplicate to keep ('first', 'last', or `False`). Defaults to `'first'`.
- `step_name` (*str*, optional): Defaults to `"DropDuplicates"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, drops duplicates, updates the context, and returns it.

---

### SelectColumns

**Description**:  
Selects a subset of columns from a DataFrame.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `columns` (*list*): List of columns to retain.
- `step_name` (*str*, optional): Defaults to `"SelectColumns"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, selects the specified columns, updates the context, and returns it.

---

### FillNAValues

**Description**:  
Fills missing (NA) values in a DataFrame with a specified fill value.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `fill_value`: The value used to fill missing values.
- `step_name` (*str*, optional): Defaults to `"FillNAValues"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, fills NA values, updates the context, and returns it.

---

### ReplaceValues

**Description**:  
Replaces occurrences of specified values in a DataFrame with a new value.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `to_replace`: Value or list of values to be replaced.
- `value`: The value to replace with.
- `step_name` (*str*, optional): Defaults to `"ReplaceValues"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, replaces values, updates the context, and returns it.

---

### MergeDataFrames

**Description**:  
Merges two DataFrames from the context based on specified key(s) and merge strategy. The resulting merged DataFrame is stored in the context.

**Constructor Arguments**:
- `left_dataframe` (*str*): Name of the left DataFrame.
- `right_dataframe` (*str*): Name of the right DataFrame.
- `on` (*str or list*): Key(s) on which to merge.
- `how` (*str*, optional): Merge strategy (e.g., 'inner', 'outer', 'left', 'right'). Defaults to `'inner'`.
- `output_name` (*str*, optional): Name to store the merged DataFrame in the context. Defaults to the left DataFrame name.
- `step_name` (*str*, optional): Defaults to `"MergeDataFrames"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the left and right DataFrames, merges them, updates the context, and returns it.

---

### JoinDataFrames

**Description**:  
Joins two DataFrames from the context using the pandas `join` method. The joined DataFrame replaces the primary DataFrame in the context.

**Constructor Arguments**:
- `primary_dataframe` (*str*): The name of the primary DataFrame.
- `secondary_dataframe` (*str*): The name of the secondary DataFrame.
- `on` (*str*, optional): The key column on which to join.
- `how` (*str*, optional): The join strategy (default is `'left'`).
- `lsuffix` (*str*, optional): Suffix for overlapping columns in the primary DataFrame.
- `rsuffix` (*str*, optional): Suffix for overlapping columns in the secondary DataFrame.
- `step_name` (*str*, optional): Defaults to `"JoinDataFrames"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the primary and secondary DataFrames, joins them, updates the context, and returns it.

---

### ApplyFunction

**Description**:  
Applies a specified function to an entire DataFrame or a specific column.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `function` (*function*): The function to apply.
- `column` (*str*, optional): If provided, applies the function only to this column.
- `axis` (*int*, optional): Axis along which to apply the function (default is `0`).
- `step_name` (*str*, optional): Defaults to `"ApplyFunction"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, applies the function (to the whole DataFrame or specified column), updates the context, and returns it.

---

### ApplyMap

**Description**:  
Applies a function element-wise to all elements in a DataFrame.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `function` (*function*): The function to apply element-wise.
- `step_name` (*str*, optional): Defaults to `"ApplyMap"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, applies the function element-wise, updates the context, and returns it.

---

### MapValues

**Description**:  
Maps the values in a specified column using a provided dictionary.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `column` (*str*): The column to map.
- `mapping_dict` (*dict*): A dictionary defining the value mapping.
- `step_name` (*str*, optional): Defaults to `"MapValues"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, maps the values in the specified column, updates the context, and returns it.

---

### OneHotEncode

**Description**:  
Performs one-hot encoding on a specified categorical column. Optionally drops the original column after encoding.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame.
- `column` (*str*): The categorical column to encode.
- `drop_original` (*bool*, optional): Whether to drop the original column (default is `False`).
- `step_name` (*str*, optional): Defaults to `"OneHotEncode"`.
- `on_error` (*str*, optional): The error handling strategy.

**Method**:
- `func(context)`: Retrieves the DataFrame, applies one-hot encoding, optionally drops the original column, updates the context, and returns it.

---

## Usage Example

Below is an example demonstrating how to use one of the transformation classes (e.g., `TransposeDataFrame`) within a pypeline context:

```python
import pandas as pd
from dataframe import TransposeDataFrame
from pypeline import Pypeline

# Create a sample DataFrame
df_sample = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# Assume we have a pypeline context that stores DataFrames
class DummyContext:
    def __init__(self):
        self.dataframes = {"sample": df_sample}
    def set_dataframe(self, name, df):
        self.dataframes[name] = df

# Create a dummy context instance
context = DummyContext()

# Initialize the TransposeDataFrame transformation
transpose_transform = TransposeDataFrame(dataframe="sample")

# Execute the transformation
updated_context = transpose_transform.func(context)

# Verify the result by printing the transposed DataFrame
print(updated_context.dataframes["sample"])