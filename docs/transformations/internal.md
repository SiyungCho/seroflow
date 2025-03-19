# Internal DataFrame Transformations Documentation

This module implements a suite of transformation classes that can manipulate internal DataFrames within the Pypeline Context. Each transformation class extends the base `Transformation` class and is designed to operate with Pypeline Object. The available transformations include:

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
  from pypeline import Pypeline
  from pypeline.transform import AddDataFrame

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  df = pd.DataFrame(...)

  add_df = AddDataFrame(dataframe=df, name="new_df") # Initialize the AddDataFrame Step

  pypeline.add_steps([add_df])
  pypeline.execute()
```

---

### DeleteDataFrame

- **Purpose**: Deletes DataFrame from Pypeline Object.
- **Parameters**:
  - `dataframe` (str): Name of DataFrame to delete.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DeleteDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### DeleteDataFrame Example

Below is an example demonstrating how to use the Transformation `DeleteDataFrame`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DeleteDataFrame

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  del_df = DeleteDataFrame(dataframe="df1") # Initialize the DeleteDataFrame Step

  pypeline.add_steps([del_df])
  pypeline.execute()
```

---

### RenameDataFrame

- **Purpose**: Renames a DataFrame stored in Pypeline Object.
- **Parameters**:
  - `old_name` (str): Previous DataFrame Name.
  - `new_name` (str): New DataFrame Name.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`RenameDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### RenameDataFrame Example

Below is an example demonstrating how to use the Transformation `RenameDataFrame`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import RenameDataFrame

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  rename_df = RenameDataFrame(old_name="sales", new_name="updated_sale") # Initialize the RenameDataFrame Step

  pypeline.add_steps([rename_df])
  pypeline.execute()
```

---

### CopyDataFrame

- **Purpose**: Creates copy of DataFrame within Pypeline Object and stores copy in Pypeline Object.
- **Parameters**:
  - `source_dataframe` (str): Name of DataFrame to copy.
  - `target_dataframe` (str): Name of new DataFrame.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`CopyDataFrame`".
  - `on_error` (str, optional): Error handling strategy.

#### CopyDataFrame Example

Below is an example demonstrating how to use the Transformation `CopyDataFrame`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import CopyDataFrame

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  df = pd.DataFrame(...)

  copy_df = CopyDataFrame(source_dataframe="revenue", target_dataframe="finances") # Initialize the CopyDataFrame Step

  pypeline.add_steps([copy_df])
  pypeline.execute()
```

---