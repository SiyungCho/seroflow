# Column Transformations Documentation

This module implements a collection of transformation classes that perform various column operations on DataFrames. These transformations update the DataFrame stored in the `Pipeline` context. Each transformation class extends the base `Transformation` class and provides a specific column operation.

- **ConvertColumnType**: Converts a specified column of a DataFrame to a new data type.
- **RenameColumns**: Renames one or more columns based on a provided mapping.
- **DropColumn**: Drops a single specified column from a DataFrame.
- **DropColumns**: Drops multiple specified columns from a DataFrame.
- **AddColumn**: Adds a new column to a DataFrame computed from a function.
- **MergeColumns**: Merges multiple columns into a single column by concatenating their string representations.
- **SplitColumn**: Splits a single column into multiple new columns based on a delimiter.
- **ExplodeColumn**: Explodes a column containing list-like elements into multiple rows.
- **CreateColumnFromVariable**: Creates a new column in a DataFrame using a constant value provided via a variable.

Each transformation retrieves the target DataFrame from the `Pipeline` context, performs the operation, updates the DataFrame, and returns the modified context.

## Column Transformation Classes

### ConvertColumnType

- **Purpose**: Converts a specified column to a new data type.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame in the context.
  - `column` (str): The column to be converted.
  - `new_type` (type): The target data type.
  - `step_name` (str, optional): Defaults to `"ConvertColumnType"`.
  - `on_error` (str, optional): The error handling strategy.

#### ConvertColumnType Example

Below is an example demonstrating how to use the Transformation `ConvertColumnType`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import ConvertColumnType

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'sales_data' with a 'price' column

  convert_col_type = ConvertColumnType(column="price", dataframe="sales_data", new_type=int) # Initialize the ConvertColumnType to convert the 'price' column to type 'int'

  pipeline.add_steps([convert_col_type])
  pipeline.execute()
```

---

### RenameColumns

- **Purpose**: Renames one or more columns in a DataFrame using a provided mapping.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `columns_mapping` (dict): Mapping of current column names to new names.
  - `step_name` (str, optional): Defaults to `"RenameColumns"`.
  - `on_error` (str, optional): The error handling strategy.

#### RenameColumns Example

Below is an example demonstrating how to use the Transformation `RenameColumns`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import RenameColumns

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads a DataFrame called 'sales_data' with 'price' and 'quantity' columns

  rename_columns = RenameColumns(dataframe="sales_data", columns_mapping={"price": "unit_price", "quantity": "units_sold"})  # Initialize RenameColumns to rename 'price' → 'unit_price' and 'quantity' → 'units_sold'

  pipeline.add_steps([rename_columns])
  pipeline.execute()
```

---

### DropColumn

- **Purpose**: Drops a specified column from a DataFrame.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `column` (str): The column to drop.
  - `step_name` (str, optional): Defaults to `"DropColumn"`.
  - `on_error` (str, optional): The error handling strategy.

#### DropColumn Example

Below is an example demonstrating how to use the Transformation `DropColumn`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import DropColumn

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  drop_column = DropColumn(column="price", dataframe="sales_data")  # Initialize DropColumn to drop the 'price' column

  pipeline.add_steps([drop_column])
  pipeline.execute()
```

---

### DropColumns

- **Purpose**: Drops multiple specified columns from a DataFrame.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `columns` (list): List of columns to drop.
  - `step_name` (str, optional): Defaults to `"DropColumns"`.
  - `on_error` (str, optional): The error handling strategy.

#### DropColumns Example

Below is an example demonstrating how to use the Transformation `DropColumns`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import DropColumns

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'price' and 'quantity' columns

  drop_columns = DropColumns(columns=["price", "quantity"], dataframe="sales_data")  # Initialize DropColumns to drop both 'price' and 'quantity'

  pipeline.add_steps([drop_columns])
  pipeline.execute()
```

---

### AddColumn

- **Purpose**: Adds a new column computed from a provided function.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `column` (str): Name of the new column.
  - `compute_func` (function): Function that computes the column’s values from the DataFrame.
  - `step_name` (str, optional): Defaults to `"AddColumn"`.
  - `on_error` (str, optional): The error handling strategy.

#### AddColumn Example

Below is an example demonstrating how to use the Transformation `AddColumn`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import AddColumn

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'price' and 'quantity' columns

  add_column = AddColumn(
      column="total_sales",
      dataframe="sales_data",
      compute_func=lambda df: df["price"] * df["quantity"]
  )  # Initialize AddColumn to create 'total_sales' by multiplying 'price' × 'quantity'

  pipeline.add_steps([add_column])
  pipeline.execute()
```

---

### MergeColumns

- **Purpose**: Merges multiple columns into a single column by concatenating their string representations.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `columns` (list): List of columns to merge.
  - `new_column` (str): Name of the resulting merged column.
  - `separator` (str, optional): Separator to use between values (default is a space).
  - `step_name` (str, optional): Defaults to `"MergeColumns"`.
  - `on_error` (str, optional): The error handling strategy.

#### MergeColumns Example

Below is an example demonstrating how to use the Transformation `MergeColumns`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import MergeColumns

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'first_name' and 'last_name' columns

  merge_columns = MergeColumns(
      columns=["first_name", "last_name"],
      new_column="full_name",
      dataframe="sales_data",
      separator=" "
  )  # Initialize MergeColumns to concatenate first_name and last_name into 'full_name'

  pipeline.add_steps([merge_columns])
  pipeline.execute()
```

---

### SplitColumn

- **Purpose**: Splits a single column into multiple new columns based on a delimiter.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `column` (str): The column to split.
  - `new_columns` (list): List of new column names.
  - `delimiter` (str, optional): Delimiter to use for splitting (default is a space).
  - `step_name` (str, optional): Defaults to `"SplitColumn"`.
  - `on_error` (str, optional): The error handling strategy.

#### SplitColumn Example

Below is an example demonstrating how to use the Transformation `SplitColumn`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import SplitColumn

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'full_name' column

  split_column = SplitColumn(
      column="full_name",
      new_columns=["first_name", "last_name"],
      dataframe="sales_data",
      delimiter=" "
  )  # Initialize SplitColumn to split 'full_name' into 'first_name' and 'last_name'

  pipeline.add_steps([split_column])
  pipeline.execute()
```

---

### ExplodeColumn

- **Purpose**: Explodes a column containing list-like elements into multiple rows, duplicating the other column values.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `column` (str): The column to explode.
  - `step_name` (str, optional): Defaults to `"ExplodeColumn"`.
  - `on_error` (str, optional): The error handling strategy.

#### ExplodeColumn Example

Below is an example demonstrating how to use the Transformation `ExplodeColumn`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import ExplodeColumn

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'tags' column containing lists

  explode_column = ExplodeColumn(column="tags", dataframe="sales_data")  # Initialize ExplodeColumn to expand each list in 'tags' into separate rows

  pipeline.add_steps([explode_column])
  pipeline.execute()
```

---

### CreateColumnFromVariable

- **Purpose**: Creates a new column in a DataFrame using a constant value provided via a variable.
- **Parameters**:
  - `dataframe` (str): Name of the DataFrame.
  - `column` (str): Name of the new column.
  - `variable`: The constant value to assign to the new column.
  - `step_name` (str, optional): Defaults to `"CreateColumnFromVariable"`.
  - `on_error` (str, optional): The error handling strategy.

#### CreateColumnFromVariable Example

Below is an example demonstrating how to use the Transformation `CreateColumnFromVariable`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import CreateColumnFromVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data'

  create_column = CreateColumnFromVariable(column="region", dataframe="sales_data", variable="North_America")  # Initialize CreateColumnFromVariable to add a 'region' column with constant value 'North America'

  pipeline.add_steps([create_column])
  pipeline.execute()
```

---