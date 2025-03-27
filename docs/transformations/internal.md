# Internal DataFrame Transformations Documentation

This module implements a suite of transformation classes that can manipulate internal DataFrames within the `Pipeline` Context. Each transformation class extends the base `Transformation` class and is designed to operate with `Pipeline` Object. The available transformations include:

- **AddDataFrame**: Adds a new DataFrame to the context.
- **DeleteDataFrame**: Deletes a DataFrame from the context.
- **RenameDataFrame**: Renames an existing DataFrame in the context.
- **CopyDataFrame**: Creates a copy of an existing DataFrame under a new name.

## Internal DataFrame Transformation Classes
 
### AddDataFrame

- **Purpose**: Adds a predefined Pandas DataFrame.
- **Parameters**:
  - `dataframe` (pd.DataFrame): DataFrame to add.
  - `name` (str): Name of DataFrame to add.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`AddDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### AddDataFrame Example

Below is an example demonstrating how to use the Transformation `AddDataFrame`:

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import AddDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Add Extractor which gathers data

  df = pd.DataFrame(...)

  add_df = AddDataFrame(dataframe=df, name="new_df") # Initialize the AddDataFrame Step

  pipeline.add_steps([add_df])
  pipeline.execute()
```

---

### DeleteDataFrame

- **Purpose**: Deletes DataFrame from `Pipeline` Object.
- **Parameters**:
  - `dataframe` (str): Name of DataFrame to delete.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DeleteDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### DeleteDataFrame Example

Below is an example demonstrating how to use the Transformation `DeleteDataFrame`:

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import DeleteDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Add Extractor which gathers data

  del_df = DeleteDataFrame(dataframe="df1") # Initialize the DeleteDataFrame Step

  pipeline.add_steps([del_df])
  pipeline.execute()
```

---

### RenameDataFrame

- **Purpose**: Renames a DataFrame stored in `Pipeline` Object.
- **Parameters**:
  - `old_name` (str): Previous DataFrame Name.
  - `new_name` (str): New DataFrame Name.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`RenameDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### RenameDataFrame Example

Below is an example demonstrating how to use the Transformation `RenameDataFrame`:

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import RenameDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Add Extractor which gathers data

  rename_df = RenameDataFrame(old_name="sales", new_name="updated_sale") # Initialize the RenameDataFrame Step

  pipeline.add_steps([rename_df])
  pipeline.execute()
```

---

### CopyDataFrame

- **Purpose**: Creates copy of DataFrame within `Pipeline` Object and stores copy in `Pipeline` Object.
- **Parameters**:
  - `source_dataframe` (str): Name of DataFrame to copy.
  - `target_dataframe` (str): Name of new DataFrame.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`CopyDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### CopyDataFrame Example

Below is an example demonstrating how to use the Transformation `CopyDataFrame`:

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import CopyDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Add Extractor which gathers data

  df = pd.DataFrame(...)

  copy_df = CopyDataFrame(source_dataframe="revenue", target_dataframe="finances") # Initialize the CopyDataFrame Step

  pipeline.add_steps([copy_df])
  pipeline.execute()
```

---