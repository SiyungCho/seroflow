# Aggregation Transformations Documentation

This module implements a suite of transformation classes that compute various statistical metrics on columns of a DataFrame. Each transformation class extends the base `Transformation` class and is designed to operate on a specified DataFrame stored in the `Pipeline` context. The available transformations include:

- **GetColMean**: Computes the mean of a specified column.
- **GetColMedian**: Computes the median of a specified column.
- **GetColMode**: Computes the mode of a specified column.
- **GetColStd**: Computes the standard deviation of a specified column.
- **GetColSum**: Computes the sum of a specified column.
- **GetColVariance**: Computes the variance of a specified column.
- **GetColQuantile**: Computes a given quantile of a specified column.
- **GetColCorrelation**: Computes the correlation between two specified columns.
- **GetColCovariance**: Computes the covariance between two specified columns.
- **GetColSkew**: Computes the skewness of a specified column.

Each class is initialized with the name of the column(s) to be processed, the DataFrame name, an optional variable name for storing the result (defaulting to a suffix based on the column name), and an error handling strategy. The transformation is executed by calling its `func()` method, which retrieves the DataFrame from the context and computes the desired statistic.

## Aggregation Transformation Classes

### GetColMean

- **Purpose**: Computes the mean of a specified column.
- **Parameters**:
  - `column` (str): Column Name to compute the mean.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the mean result. Defaults to `"<column>_mean"`.

#### GetColMean Example

Below is an example demonstrating how to use the Transformation `GetColMean`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColMean

  pipeline = Pipeline()
  pipeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'sales_data' with a 'price' column

  get_mean = GetColMean(column="price", dataframe="sales_data", variable="mean_price") # Initialize the GetColMean to compute the mean of the 'price' column

  pipeline.add_steps([get_mean])
  pipeline.execute()
```

---

### GetColMedian

- **Purpose**: Computes the median of a specified column.
- **Parameters**:
  - `column` (str): Column to compute the median.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the median result. Defaults to `"<column>_median"`.

#### GetColMedian Example

Below is an example demonstrating how to use the Transformation `GetColMedian`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColMedian

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads a DataFrame named 'sales_data' with a 'price' column

  get_median = GetColMedian(column="price", dataframe="sales_data", variable="median_price") # Initialize the GetColMedian to compute the median of the 'price' column

  pipeline.add_steps([get_median])
  pipeline.execute()
```

---

### GetColMode

- **Purpose**: Computes the mode of a specified column.
- **Parameters**:
  - `column` (str): Column to compute the mode.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the mode result. Defaults to `"<column>_mode"`.

#### GetColMode Example

Below is an example demonstrating how to use the Transformation `GetColMode`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColMode

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  get_mode = GetColMode(column="price", dataframe="sales_data", variable="mode_price") # Initialize the GetColMode to compute the mode of the 'price' column

  pipeline.add_steps([get_mode])
  pipeline.execute()
```

---

### GetColStd

- **Purpose**: Computes the standard deviation of a specified column.
- **Parameters**:
  - `column` (str): Column to compute the standard deviation.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the result. Defaults to `"<column>_std"`.

#### GetColStd Example

Below is an example demonstrating how to use the Transformation `GetColStd`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColStd

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  get_std = GetColStd(column="price", dataframe="sales_data", variable="price_std") # Initialize the GetColStd to compute the standard deviation of the 'price' column

  pipeline.add_steps([get_std])
  v.execute()
```

---

### GetColSum

- **Purpose**: Computes the sum of a specified column.
- **Parameters**:
  - `column` (str): Column to compute the sum.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the sum result. Defaults to `"<column>_sum"`.

#### GetColSum Example

Below is an example demonstrating how to use the Transformation `GetColSum`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColSum

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  get_sum = GetColSum(column="price", dataframe="sales_data", variable="price_sum") # Initialize the GetColSum to compute the sum of the 'price' column

  pipeline.add_steps([get_sum])
  pipeline.execute()
```

---

### GetColVariance

- **Purpose**: Computes the variance of a specified column.
- **Parameters**:
  - `column` (str): Column to compute the variance.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the variance result. Defaults to `"<column>_variance"`.

#### GetColVariance Example

Below is an example demonstrating how to use the Transformation `GetColVariance`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColVariance

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  get_variance = GetColVariance(column="price", dataframe="sales_data", variable="price_variance") # Initialize the GetColVariance to compute the variance of the 'price' column

  pipeline.add_steps([get_variance])
  pipeline.execute()
```

---

### GetColQuantile

- **Purpose**: Computes a specified quantile of a column.
- **Parameters**:
  - `column` (str): Column for which to compute the quantile.
  - `dataframe` (str): Name of the DataFrame.
  - `quantile` (float): The quantile to compute (e.g., 0.5 for the median).
  - `variable` (str, optional): Variable name to store the quantile result. Defaults to `"<column>_quantile_<quantile>"`.

#### GetColQuantile Example

Below is an example demonstrating how to use the Transformation `GetColQuantile`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColQuantile

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  get_quantile = GetColQuantile(column="price", dataframe="sales_data", quantile=0.75, variable="price_quantile_0.75") # Initialize the GetColQuantile to compute the quantile of the 'price' column

  pipeline.add_steps([get_quantile])
  pipeline.execute()
```

---

### GetColCorrelation

- **Purpose**: Computes the correlation between two specified columns.
- **Parameters**:
  - `column1` (str): First column.
  - `column2` (str): Second column.
  - `dataframe` (str): Name of the DataFrame containing the columns.
  - `variable` (str, optional): Variable name to store the correlation result. Defaults to `"<column1>_<column2>_correlation"`.

#### GetColCorrelation Example

Below is an example demonstrating how to use the Transformation `GetColCorrelation`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColCorrelation

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'price' and 'quantity' columns

  get_corr = GetColCorrelation(column1="price", column2="quantity", dataframe="sales_data", variable="price_quantity_correlation") # Initialize the GetColCorrelation to compute the correlation of the 'price' column to the 'quantity' column

  pipeline.add_steps([get_corr])
  pipeline.execute()
```

---

### GetColCovariance

- **Purpose**: Computes the covariance between two specified columns.
- **Parameters**:
  - `column1` (str): First column.
  - `column2` (str): Second column.
  - `dataframe` (str): Name of the DataFrame containing the columns.
  - `variable` (str, optional): Variable name to store the covariance result. Defaults to `"<column1>_<column2>_covariance"`.

#### GetColCovariance Example

Below is an example demonstrating how to use the Transformation `GetColCovariance`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColCovariance

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with 'price' and 'quantity' columns

  get_cov = GetColCovariance(column1="price", column2="quantity", dataframe="sales_data", variable="price_quantity_covariance") # Initialize the GetColCovariance to compute the covariance of the 'price' column to the 'quantity' column

  pipeline.add_steps([get_cov])
  pipeline.execute()
```

---

### GetColSkew

- **Purpose**: Computes the skewness of a specified column.
- **Parameters**:
  - `column` (str): Column to compute the skewness.
  - `dataframe` (str): Name of the DataFrame.
  - `variable` (str, optional): Variable name to store the skewness result. Defaults to `"<column>_skew"`.

#### GetColSkew Example

Below is an example demonstrating how to use the Transformation `GetColSkew`:

```python
  import pandas as pd
  from seroflow import Pipeline
  from seroflow.transform import GetColSkew

  pipeline = Pipeline()
  pipeline.target_extractor = ...  # Extractor loads 'sales_data' with a 'price' column

  get_skew = GetColSkew(column="price", dataframe="sales_data", variable="price_skew") # Initialize the GetColSkew to compute the skew of the 'price' column

  pipeline.add_steps([get_skew])
  pipeline.execute()
```

---