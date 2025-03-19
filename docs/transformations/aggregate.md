# Aggregation Module Documentation

This module implements a suite of transformation classes that compute various statistical metrics on columns of a DataFrame. Each transformation class extends the base `Transformation` class and is designed to operate on a specified DataFrame stored in the Pypeline context. The available transformations include:

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

---

## Common Characteristics

- **Initialization**:  
  Each transformation class receives parameters such as the column name, the DataFrame name, an optional variable name (if not provided, a default is set based on the column name), the step name (defaulting to the transformation class name), and an optional error handling strategy.

- **Execution**:  
  The transformation is executed by calling the `func(context)` method. This method retrieves the target DataFrame from the provided `context` (which stores all DataFrames) and computes the statistic for the specified column(s).

- **Result Storage**:  
  Each class calls `override_return_list()` with the variable name, ensuring that the computed statistic is stored in the Pypeline context under a designated variable name.

---

## Transformation Classes

### GetColMean

- **Purpose**: Computes the mean of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the mean.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the mean result. Defaults to `"<column>_mean"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the mean of the specified column.

---

### GetColMedian

- **Purpose**: Computes the median of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the median.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the median result. Defaults to `"<column>_median"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the median of the specified column.

---

### GetColMode

- **Purpose**: Computes the mode of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the mode.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the mode result. Defaults to `"<column>_mode"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the mode (first mode if multiple exist) of the specified column.

---

### GetColStd

- **Purpose**: Computes the standard deviation of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the standard deviation.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the result. Defaults to `"<column>_std"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the standard deviation of the specified column.

---

### GetColSum

- **Purpose**: Computes the sum of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the sum.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the sum result. Defaults to `"<column>_sum"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the sum of the specified column.

---

### GetColVariance

- **Purpose**: Computes the variance of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the variance.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the variance result. Defaults to `"<column>_variance"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the variance of the specified column.

---

### GetColQuantile

- **Purpose**: Computes a specified quantile of a column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column for which to compute the quantile.
    - `dataframe` (str): Name of the DataFrame.
    - `quantile` (float): The quantile to compute (e.g., 0.5 for the median).
    - `variable` (str, optional): Variable name to store the quantile result. Defaults to `"<column>_quantile_<quantile>"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the computed quantile of the specified column.

---

### GetColCorrelation

- **Purpose**: Computes the correlation between two specified columns.
- **Usage**:
  - **Constructor Arguments**:
    - `column1` (str): First column.
    - `column2` (str): Second column.
    - `dataframe` (str): Name of the DataFrame containing the columns.
    - `variable` (str, optional): Variable name to store the correlation result. Defaults to `"<column1>_<column2>_correlation"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the correlation between the two columns.

---

### GetColCovariance

- **Purpose**: Computes the covariance between two specified columns.
- **Usage**:
  - **Constructor Arguments**:
    - `column1` (str): First column.
    - `column2` (str): Second column.
    - `dataframe` (str): Name of the DataFrame containing the columns.
    - `variable` (str, optional): Variable name to store the covariance result. Defaults to `"<column1>_<column2>_covariance"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the covariance between the two columns.

---

### GetColSkew

- **Purpose**: Computes the skewness of a specified column.
- **Usage**:
  - **Constructor Arguments**:
    - `column` (str): Column to compute the skewness.
    - `dataframe` (str): Name of the DataFrame.
    - `variable` (str, optional): Variable name to store the skewness result. Defaults to `"<column>_skew"`.
  - **Method**:
    - `func(context)`: Retrieves the DataFrame from `context` and returns the skewness of the specified column.

---

## Usage Example

Below is an example demonstrating how to use one of the transformation classes (e.g., `GetColMean`) within a pypeline context:

```python
import pandas as pd
from aggregation import GetColMean

# Create a sample DataFrame
df_sample = pd.DataFrame({
    'price': [10, 20, 30, 40, 50],
    'quantity': [1, 2, 3, 4, 5]
})

# Assume we have a Pypeline context with dataframes
class DummyContext:
    def __init__(self):
        self.dataframes = {"sales_data": df_sample}

# Create an instance of the DummyContext
context = DummyContext()

# Initialize the GetColMean transformation to compute the mean of the 'price' column
get_mean = GetColMean(column="price", dataframe="sales_data")

# Execute the transformation
mean_value = get_mean.func(context)
print("Mean of 'price':", mean_value)