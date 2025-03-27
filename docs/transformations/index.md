# Index Transformations Documentation

This module implements transformation classes for manipulating the index of a DataFrame. Each transformation class extends the base `Transformation` class and operates on a specified DataFrame stored in the `Pipeline` context. The available transformations include:

- **SetIndex**: Sets a specified column as the DataFrame’s index.
- **ResetIndex**: Resets the DataFrame’s index, with an option to drop the existing index.

## Index Transformation Classes

### SetIndex

- **Purpose**: Sets a specified column as the index of a DataFrame using pandas’ `set_index`.
- **Parameters**:
  - `dataframe` (*str*): Name of the DataFrame in the `Pipeline` context.
  - `index_column` (*str*): Column to set as the new index.
  - `step_name` (*str*, optional): Name of this transformation step. Defaults to `"SetIndex"`.
  - `on_error` (*str*, optional): Error handling strategy.

#### SetIndex Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import SetIndex

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Extractor extracts 'sample_data' with 'id' column

  # Initialize and execute SetIndex
  set_index = SetIndex(dataframe="sample_data", index_column="id")
  pipeline.add_steps([set_index])
  pipeline.execute()
```

---

### ResetIndex
- **Purpose**: Resets the index of a DataFrame using pandas’ reset_index.
- **Parameters**:
  - `dataframe` (*str*): Name of the DataFrame in the `Pipeline` context.
  - `drop` (*bool*, optional): Whether to drop the current index. Defaults to False.
  - `step_name` (*str*, optional): Name of this transformation step. Defaults to "ResetIndex".
  - `on_error` (*str*, optional): Error handling strategy.

#### SetIndex Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import ResetIndex

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Extractor extracts 'sample_data'

  # Initialize and execute ResetIndex (dropping the index)
  reset_index = ResetIndex(dataframe="sample_data", drop=True)
  pipeline.add_steps([reset_index])
  pipeline.execute()
```

---