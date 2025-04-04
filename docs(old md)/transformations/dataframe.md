# DataFrame Transformations Documentation

This module implements a collection of transformation classes that perform various operations on DataFrames. Each transformation class extends the base `Transformation` class and updates the DataFrame stored in the `Pipeline` context accordingly.

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

Each transformation retrieves the target DataFrame from the `Pipeline` context, applies the desired operation, updates the DataFrame, and returns the modified context.

## DataFrame Transformation Classes

### TransposeDataFrame

- **Purpose**: Transposes the specified DataFrame using pandas' transpose method. The transposed DataFrame replaces the original in the context.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame in the context to be transposed.
  - `step_name` (*str*, optional): Defaults to `"TransposeDataFrame"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### TransposeDataFrame Example

Below is an example demonstrating how to use the Transformation `TransposeDataFrame`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import TransposeDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads a DataFrame called 'sales_data'

  transpose_df = TransposeDataFrame(dataframe="sales_data")  # Initialize TransposeDataFrame to transpose 'sales_data'

  pipeline.add_steps([transpose_df])
  pipeline.execute()
```

---

### PivotDataFrame

- **Purpose**: Creates a pivot table from a DataFrame using specified index, columns, values, and an aggregation function. The resulting pivot table is added to the context.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `index` (*str or list*): Column(s) to set as the pivot table index.
  - `columns` (*str or list*): Column(s) to pivot.
  - `values` (*str*): Column to aggregate.
  - `aggfunc` (*str or function*, optional): Aggregation function to apply (default is `'mean'`).
  - `step_name` (*str*, optional): Defaults to `"PivotDataFrame"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### PivotDataFrame Example

Below is an example demonstrating how to use the Transformation `PivotDataFrame`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import PivotDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'region', 'month', and 'sales' columns

  pivot_df = PivotDataFrame(
      dataframe="sales_data",
      index="region",
      columns="month",
      values="sales",
      aggfunc="sum"
  )  # Initialize PivotDataFrame to create a pivot table of sales by region and month

  pipeline.add_steps([pivot_df])
  pipeline.execute()
```

---

### MeltDataFrame

- **Purpose**: Unpivots a DataFrame from wide to long format using pandas' `melt` function. The melted DataFrame is updated in the context.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `id_vars` (*str or list*): Identifier variable(s) that will remain unpivoted.
  - `value_vars` (*str or list*): Column(s) to unpivot.
  - `var_name` (*str*, optional): Name for the variable column (default is `"variable"`).
  - `value_name` (*str*, optional): Name for the value column (default is `"value"`).
  - `step_name` (*str*, optional): Defaults to `"MeltDataFrame"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### MeltDataFrame Example

Below is an example demonstrating how to use the Transformation `MeltDataFrame`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import MeltDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'region', 'sales_Q1', 'sales_Q2' columns

  melt_df = MeltDataFrame(
      dataframe="sales_data",
      id_vars="region",
      value_vars=["sales_Q1", "sales_Q2"],
      var_name="quarter",
      value_name="sales"
  )  # Initialize MeltDataFrame to unpivot quarterly sales into long format

  pipeline.add_steps([melt_df])
  pipeline.execute()
```

---

### GroupByAggregate

- **Purpose**: Groups a DataFrame by specified column(s) and aggregates other columns using provided functions. The resulting aggregated DataFrame is updated in the context.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `groupby_columns` (*str or list*): Column(s) to group by.
  - `agg_dict` (*dict*): Dictionary specifying aggregation functions for columns.
  - `step_name` (*str*, optional): Defaults to `"GroupByAggregate"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### GroupByAggregate Example

Below is an example demonstrating how to use the Transformation `GroupByAggregate`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GroupByAggregate

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'region' and 'sales' columns

  groupby_agg = GroupByAggregate(
      dataframe="sales_data",
      groupby_columns="region",
      agg_dict={"sales": "sum"}
  )  # Initialize GroupByAggregate to compute total sales per region

  pipeline.add_steps([groupby_agg])
  pipeline.execute()
```

---

### FilterRows

- **Purpose**: Filters rows in a DataFrame based on a provided boolean function. The function should accept a DataFrame and return a boolean Series used for filtering.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `filter_func` (*function*): Function that returns a boolean Series for filtering rows.
  - `step_name` (*str*, optional): Defaults to `"FilterRows"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### FilterRows Example

Below is an example demonstrating how to use the Transformation `FilterRows`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import FilterRows

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'sales' column

  filter_rows = FilterRows(
      dataframe="sales_data",
      filter_func=lambda df: df["sales"] > 1000
  )  # Initialize FilterRows to keep only rows with sales > 1000

  pipeline.add_steps([filter_rows])
  pipeline.execute()
```

---

### SortDataFrame

- **Purpose**: Sorts a DataFrame by one or more specified columns.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `by` (*str or list*): Column(s) to sort by.
  - `ascending` (*bool*, optional): Sort order (default is `True` for ascending).
  - `step_name` (*str*, optional): Defaults to `"SortDataFrame"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### SortDataFrame Example

Below is an example demonstrating how to use the Transformation `SortDataFrame`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import SortDataFrame

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'sales' column

  sort_df = SortDataFrame(
      dataframe="sales_data",
      by="sales",
      ascending=False
  )  # Initialize SortDataFrame to sort sales in descending order

  pipeline.add_steps([sort_df])
  pipeline.execute()
```

---

### DropDuplicates

- **Purpose**: Removes duplicate rows from a DataFrame based on specified subset columns.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `subset` (*str or list*, optional): Columns to consider for identifying duplicates.
  - `keep` (*str*, optional): Which duplicate to keep ('first', 'last', or `False`). Defaults to `'first'`.
  - `step_name` (*str*, optional): Defaults to `"DropDuplicates"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### DropDuplicates Example

Below is an example demonstrating how to use the Transformation `DropDuplicates`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import DropDuplicates

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with duplicate rows

  drop_dups = DropDuplicates(
      dataframe="sales_data",
      subset=["customer_id"]
  )  # Initialize DropDuplicates to remove duplicate customer records

  pipeline.add_steps([drop_dups])
  pipeline.execute()
```

---

### SelectColumns

- **Purpose**: Selects a subset of columns from a DataFrame.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `columns` (*list*): List of columns to retain.
  - `step_name` (*str*, optional): Defaults to `"SelectColumns"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### SelectColumns Example

Below is an example demonstrating how to use the Transformation `SelectColumns`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import SelectColumns

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with multiple columns

  select_cols = SelectColumns(
      dataframe="sales_data",
      columns=["customer_id", "sales"]
  )  # Initialize SelectColumns to keep only customer_id and sales columns

  pipeline.add_steps([select_cols])
  pipeline.execute()
```

---

### FillNAValues

- **Purpose**: Fills missing (NA) values in a DataFrame with a specified fill value.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `fill_value`: The value used to fill missing values.
  - `step_name` (*str*, optional): Defaults to `"FillNAValues"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### FillNAValues Example

Below is an example demonstrating how to use the Transformation `FillNAValues`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import FillNAValues

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with missing values

  fill_na = FillNAValues(
      dataframe="sales_data",
      fill_value=0
  )  # Initialize FillNAValues to replace NaNs with 0

  pipeline.add_steps([fill_na])
  pipeline.execute()
```

---

### ReplaceValues

- **Purpose**: Replaces occurrences of specified values in a DataFrame with a new value.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `to_replace`: Value or list of values to be replaced.
  - `value`: The value to replace with.
  - `step_name` (*str*, optional): Defaults to `"ReplaceValues"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### ReplaceValues Example

Below is an example demonstrating how to use the Transformation `ReplaceValues`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import ReplaceValues

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with placeholder values

  replace_vals = ReplaceValues(
      dataframe="sales_data",
      to_replace="N/A",
      value=None
  )  # Initialize ReplaceValues to convert 'N/A' to None

  pipeline.add_steps([replace_vals])
  pipeline.execute()
```

---

### MergeDataFrames

- **Purpose**: Merges two DataFrames from the context based on specified key(s) and merge strategy. The resulting merged DataFrame is stored in the context.
- **Parameters**:
  - `left_dataframe` (*str*): Name of the left DataFrame.
  - `right_dataframe` (*str*): Name of the right DataFrame.
  - `on` (*str or list*): Key(s) on which to merge.
  - `how` (*str*, optional): Merge strategy (e.g., 'inner', 'outer', 'left', 'right'). Defaults to `'inner'`.
  - `output_name` (*str*, optional): Name to store the merged DataFrame in the context. Defaults to the left DataFrame name.
  - `step_name` (*str*, optional): Defaults to `"MergeDataFrames"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### MergeDataFrames Example

Below is an example demonstrating how to use the Transformation `MergeDataFrames`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import MergeDataFrames

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' and 'customer_data'

  merge_dfs = MergeDataFrames(
      left_dataframe="sales_data",
      right_dataframe="customer_data",
      on="customer_id",
      how="left",
      output_name="merged_sales"
  )  # Initialize MergeDataFrames to join sales_data with customer_data

  pipeline.add_steps([merge_dfs])
  pipeline.execute()
```

---

### JoinDataFrames

- **Purpose**: Joins two DataFrames from the context using the pandas `join` method. The joined DataFrame replaces the primary DataFrame in the context.
- **Parameters**:
  - `primary_dataframe` (*str*): The name of the primary DataFrame.
  - `secondary_dataframe` (*str*): The name of the secondary DataFrame.
  - `on` (*str*, optional): The key column on which to join.
  - `how` (*str*, optional): The join strategy (default is `'left'`).
  - `lsuffix` (*str*, optional): Suffix for overlapping columns in the primary DataFrame.
  - `rsuffix` (*str*, optional): Suffix for overlapping columns in the secondary DataFrame.
  - `step_name` (*str*, optional): Defaults to `"JoinDataFrames"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### JoinDataFrames Example

Below is an example demonstrating how to use the Transformation `JoinDataFrames`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import JoinDataFrames

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' and 'customer_data'

  join_dfs = JoinDataFrames(
      primary_dataframe="sales_data",
      secondary_dataframe="customer_data",
      on="customer_id",
      how="inner"
  )  # Initialize JoinDataFrames to perform an inner join on customer_id

  pipeline.add_steps([join_dfs])
  pipeline.execute()
```

---

### ApplyFunction

- **Purpose**: Applies a specified function to an entire DataFrame or a specific column.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `function` (*function*): The function to apply.
  - `column` (*str*, optional): If provided, applies the function only to this column.
  - `axis` (*int*, optional): Axis along which to apply the function (default is `0`).
  - `step_name` (*str*, optional): Defaults to `"ApplyFunction"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### ApplyFunction Example

Below is an example demonstrating how to use the Transformation `ApplyFunction`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import ApplyFunction

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data'

  apply_fn = ApplyFunction(
      dataframe="sales_data",
      function=lambda df: df.assign(sales=df["sales"].round(2))
  )  # Initialize ApplyFunction to round sales to two decimal places

  pipeline.add_steps([apply_fn])
  pipeline.execute()
```

---

### ApplyMap

- **Purpose**: Applies a function element-wise to all elements in a DataFrame.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `function` (*function*): The function to apply element-wise.
  - `step_name` (*str*, optional): Defaults to `"ApplyMap"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### ApplyMap Example

Below is an example demonstrating how to use the Transformation `ApplyMap`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import ApplyMap

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data'

  apply_map = ApplyMap(
      dataframe="sales_data",
      function=lambda x: str(x).upper()
  )  # Initialize ApplyMap to convert all values to uppercase strings

  pipeline.add_steps([apply_map])
  pipeline.execute()
```

---

### MapValues

- **Purpose**: Maps the values in a specified column using a provided dictionary.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `column` (*str*): The column to map.
  - `mapping_dict` (*dict*): A dictionary defining the value mapping.
  - `step_name` (*str*, optional): Defaults to `"MapValues"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### MapValues Example

Below is an example demonstrating how to use the Transformation `MapValues`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import MapValues

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'region' column

  map_values = MapValues(
      dataframe="sales_data",
      column="region",
      mapping_dict={"NY": "New York", "CA": "California"}
  )  # Initialize MapValues to expand region codes into full names

  pipeline.add_steps([map_values])
  pipeline.execute()
```

---

### OneHotEncode

- **Purpose**: Performs one-hot encoding on a specified categorical column. Optionally drops the original column after encoding.
- **Parameters**:
  - `dataframe` (*str*): The name of the DataFrame.
  - `column` (*str*): The categorical column to encode.
  - `drop_original` (*bool*, optional): Whether to drop the original column (default is `False`).
  - `step_name` (*str*, optional): Defaults to `"OneHotEncode"`.
  - `on_error` (*str*, optional): The error handling strategy.

#### OneHotEncode Example

Below is an example demonstrating how to use the Transformation `OneHotEncode`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import OneHotEncode

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'region' column

  one_hot = OneHotEncode(
      dataframe="sales_data",
      column="region",
      drop_original=True
  )  # Initialize OneHotEncode to one-hot encode region and drop the original column

  pipeline.add_steps([one_hot])
  pipeline.execute()
```

---