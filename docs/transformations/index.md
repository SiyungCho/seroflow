# Index Transformations Module Documentation

This module implements transformation classes for manipulating the index of a DataFrame. It provides classes to set a specified column as the index (`SetIndex`) and to reset the index (`ResetIndex`) of a DataFrame. Each transformation updates the DataFrame stored in the pypeline context.

---

## Overview

- **SetIndex**:  
  Sets a specified column as the index of a DataFrame using pandas' `set_index` method.

- **ResetIndex**:  
  Resets the index of a DataFrame using pandas' `reset_index` method, with an option to drop the current index.

Each transformation retrieves the target DataFrame from the context, applies the index manipulation, updates the context with the modified DataFrame, and returns the updated context.

---

## Transformation Classes

### SetIndex

**Description**:  
The `SetIndex` transformation sets a specified column as the index of a DataFrame. It updates the DataFrame in the pypeline context by calling pandas' `set_index` method.

**Attributes**:
- `dataframe` (*str*): Name of the DataFrame in the context.
- `index_column` (*str*): The column to be set as the new index.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame to update.
- `index_column` (*str*): The column to set as the index.
- `step_name` (*str*, optional): Name of the transformation step (default `"SetIndex"`).
- `on_error` (*str*, optional): Error handling strategy.

**Key Method**:
- `func(context)`:  
  - Retrieves the DataFrame from the context.
  - Sets the specified column as the index.
  - Updates the DataFrame in the context.
  - Returns the updated context.

**Implementation Note**:  
The helper method `__set_index` calls `df.set_index(self.index_column, inplace=True)`. Since `inplace=True` returns `None`, the transformation effectively modifies the DataFrame in place.

---

### ResetIndex

**Description**:  
The `ResetIndex` transformation resets the index of a DataFrame. It updates the DataFrame in the pypeline context by calling pandas' `reset_index` method. The transformation allows the option to drop the existing index.

**Attributes**:
- `dataframe` (*str*): Name of the DataFrame in the context.
- `drop` (*bool*): Indicates whether to drop the current index. Defaults to `False`.

**Constructor Arguments**:
- `dataframe` (*str*): The name of the DataFrame to update.
- `drop` (*bool*, optional): Whether to drop the existing index (default `False`).
- `step_name` (*str*, optional): Name of the transformation step (default `"ResetIndex"`).
- `on_error` (*str*, optional): Error handling strategy.

**Key Method**:
- `func(context)`:  
  - Retrieves the DataFrame from the context.
  - Resets its index according to the `drop` parameter.
  - Updates the DataFrame in the context.
  - Returns the updated context.

**Implementation Note**:  
The helper method `__reset_index` calls `df.reset_index(drop=self.drop, inplace=True)`, which modifies the DataFrame in place.

---

## Usage Example

Below is an example demonstrating how to use the `SetIndex` and `ResetIndex` transformations within a pypeline context:

```python
from index import SetIndex, ResetIndex
from pypeline import Pypeline
import pandas as pd

# Create a sample DataFrame
df_sample = pd.DataFrame({
    'id': [101, 102, 103],
    'value': ['A', 'B', 'C']
})

# Dummy context simulating the pypeline context
class DummyContext:
    def __init__(self):
        self.dataframes = {"sample_df": df_sample}
    def set_dataframe(self, name, df):
        self.dataframes[name] = df

context = DummyContext()

# Use SetIndex to set 'id' as the index of the DataFrame
set_index_transform = SetIndex(dataframe="sample_df", index_column="id")
context = set_index_transform.func(context)

# Check the result
print("After setting index:")
print(context.dataframes["sample_df"])

# Use ResetIndex to reset the index, dropping the current index
reset_index_transform = ResetIndex(dataframe="sample_df", drop=True)
context = reset_index_transform.func(context)

# Check the result
print("After resetting index:")
print(context.dataframes["sample_df"])