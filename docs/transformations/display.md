# Display Transformations Documentation

This module implements a suite of transformation classes that displays key information of a DataFrame. Each transformation class extends the base `Transformation` class and is designed to operate on a specified DataFrame stored in the Pypeline context. The available transformations include:

- **DisplayInfo**: Prints basic information (shape, columns, and data types) for each DataFrame.
- **DisplayColumns**: Prints the list of column names for each DataFrame.
- **DisplayHead**: Prints the first N rows of each DataFrame.
- **DisplayTail**: Prints the last N rows of each DataFrame.
- **DisplayColumnMean**: Displays the mean of a specified column for each DataFrame.
- **DisplayColumnMedian**: Displays the median of a specified column for each DataFrame.
- **DisplayColumnMode**: Displays the mode(s) of a specified column for each DataFrame.
- **DisplayColumnVariance**: Displays the variance of a specified column for each DataFrame.
- **DisplayColumnStdDev**: Displays the standard deviation of a specified column for each DataFrame.
- **DisplayColumnSum**: Displays the sum of a specified column for each DataFrame.
- **DisplayColumnMin**: Displays the minimum value of a specified column for each DataFrame.
- **DisplayColumnMax**: Displays the maximum value of a specified column for each DataFrame.
- **DisplayColumnCount**: Displays the count of non-null values in a specified column for each DataFrame.
- **DisplayColumnUnique**: Displays the unique values in a specified column for each DataFrame.
- **DisplayColumnNUnique**: Displays the number of unique values in a specified column for each DataFrame.
- **DisplayColumnDType**: Displays the data type of a specified column for each DataFrame.
- **DisplayStringCount**: Displays the value counts for a specified column in each DataFrame.
- **DisplayMostFrequentString**: Displays the most frequent item(s) in a specified column for each DataFrame.
- **DisplayAllCategories**: Displays all unique categories in a specified column for each DataFrame.
- **DisplaySubstringOccurrence**: Counts and displays the total occurrences of a substring in a specified column for each DataFrame.

It is important to note that these classes are purely visual and meant solely to view information. Future versions will seek to store the display results into variables/log the display results via `'logging.logger'`.

## Display Transformation Classes
 
### DisplayInfo

- **Purpose**: Displays general information (shape, columns, data types) about the specified dataframes.
- **Parameters**:
  - `dataframes` (str or List[str]): List of Names of the DataFrames.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayInfo`".

#### DisplayInfo Example

Below is an example demonstrating how to use the Transformation `DisplayInfo`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayInfo

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers dataframes called 'states' and 'regions'

  display_info = DisplayInfo(dataframes=['states', 'regions']) # Initialize the DisplayInfo Step

  pypeline.add_steps([display_info])
  pypeline.execute()
```

---

### DisplayColumns

- **Purpose**: Prints the list of column names for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumns`".

#### DisplayColumns Example

Below is an example demonstrating how to use the Transformation `DisplayColumns`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumns

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'sales'

  display_columns = DisplayColumns(dataframes='sales')  # Initialize the DisplayColumns step

  pypeline.add_steps([display_columns])
  pypeline.execute()
```

---

### DisplayHead

- **Purpose**: Prints the first N rows of each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `n` (int, optional): Number of rows to display from the top. Defaults to 5.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayHead`".

#### DisplayHead Example

Below is an example demonstrating how to use the Transformation `DisplayHead`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayHead

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'employees'

  display_head = DisplayHead(dataframes='employees', n=10)  # Initialize the DisplayHead step to show first 10 rows

  pypeline.add_steps([display_head])
  pypeline.execute()
```

---

### DisplayTail

- **Purpose**: Prints the last N rows of each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `n` (int, optional): Number of rows to display from the bottom. Defaults to 5.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayTail`".

#### DisplayTail Example

Below is an example demonstrating how to use the Transformation `DisplayTail`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayTail

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'orders'

  display_tail = DisplayTail(dataframes='orders', n=5)  # Initialize the DisplayTail step

  pypeline.add_steps([display_tail])
  pypeline.execute()
```

---

### DisplayColumnMean

- **Purpose**: Calculates and prints the mean of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the mean is to be computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnMean`".

#### DisplayColumnMean Example

Below is an example demonstrating how to use the Transformation `DisplayColumnMean`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnMean

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'metrics' with a 'score' column

  display_mean = DisplayColumnMean(dataframes='metrics', column='score')  # Initialize the DisplayColumnMean step

  pypeline.add_steps([display_mean])
  pypeline.execute()
```

---

### DisplayColumnMedian

- **Purpose**: Calculates and prints the median of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the median is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnMedian`".

#### DisplayColumnMedian Example

Below is an example demonstrating how to use the Transformation `DisplayColumnMedian`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnMedian

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'data' with a 'age' column

  display_median = DisplayColumnMedian(dataframes='data', column='age')  # Initialize the DisplayColumnMedian step

  pypeline.add_steps([display_median])
  pypeline.execute()
```

---

### DisplayColumnMode

- **Purpose**: Computes and prints the mode(s) of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the mode is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnMode`".

#### DisplayColumnMode Example

Below is an example demonstrating how to use the Transformation `DisplayColumnMode`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnMode

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'survey' with a 'response' column

  display_mode = DisplayColumnMode(dataframes='survey', column='response')  # Initialize the DisplayColumnMode step

  pypeline.add_steps([display_mode])
  pypeline.execute()
```

---

### DisplayColumnVariance

- **Purpose**: Calculates and prints the variance of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the variance is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnVariance`".

#### DisplayColumnVariance Example

Below is an example demonstrating how to use the Transformation `DisplayColumnVariance`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnVariance

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'finance' with a 'revenue' column

  display_variance = DisplayColumnVariance(dataframes='finance', column='revenue')  # Initialize the DisplayColumnVariance step

  pypeline.add_steps([display_variance])
  pypeline.execute()
```

---

### DisplayColumnStdDev

- **Purpose**: Calculates and prints the standard deviation of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the standard deviation is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnStdDev`".

#### DisplayColumnStdDev Example

Below is an example demonstrating how to use the Transformation `DisplayColumnStdDev`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnStdDev

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'stats' with a 'duration' column

  display_stddev = DisplayColumnStdDev(dataframes='stats', column='duration')  # Initialize the DisplayColumnStdDev step

  pypeline.add_steps([display_stddev])
  pypeline.execute()
```

---

### DisplayColumnSum

- **Purpose**: Calculates and prints the sum of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the sum is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnSum`".

#### DisplayColumnSum Example

Below is an example demonstrating how to use the Transformation `DisplayColumnSum`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnSum

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'transactions' with a 'amount' column

  display_sum = DisplayColumnSum(dataframes='transactions', column='amount')  # Initialize the DisplayColumnSum step

  pypeline.add_steps([display_sum])
  pypeline.execute()
```

---

### DisplayColumnMin

- **Purpose**: Finds and prints the minimum value of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the minimum value is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnMin`".

#### DisplayColumnMin Example

Below is an example demonstrating how to use the Transformation `DisplayColumnMin`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnMin

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'inventory' with a 'price' column

  display_min = DisplayColumnMin(dataframes='inventory', column='price')  # Initialize the DisplayColumnMin step

  pypeline.add_steps([display_min])
  pypeline.execute()
```

---

### DisplayColumnMax

- **Purpose**: Finds and prints the maximum value of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the maximum value is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnMax`".

#### DisplayColumnMax Example

Below is an example demonstrating how to use the Transformation `DisplayColumnMax`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnMax

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'inventory' with a 'price' column

  display_max = DisplayColumnMax(dataframes='inventory', column='price')  # Initialize the DisplayColumnMax step

  pypeline.add_steps([display_max])
  pypeline.execute()
```

---

### DisplayColumnCount

- **Purpose**: Counts and prints the number of non-null values in a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which the non-null count is computed.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnCount`".

#### DisplayColumnCount Example

Below is an example demonstrating how to use the Transformation `DisplayColumnCount`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnCount

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'customers' with a 'email' column

  display_count = DisplayColumnCount(dataframes='customers', column='email')  # Initialize the DisplayColumnCount step

  pypeline.add_steps([display_count])
  pypeline.execute()
```

---

### DisplayColumnUnique

- **Purpose**: Retrieves and prints the unique values present in a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index from which to retrieve unique values.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnUnique`".

#### DisplayColumnUnique Example

Below is an example demonstrating how to use the Transformation `DisplayColumnUnique`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnUnique

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'logs' with a 'user_id' column

  display_unique = DisplayColumnUnique(dataframes='logs', column='user_id')  # Initialize the DisplayColumnUnique step

  pypeline.add_steps([display_unique])
  pypeline.execute()
```

---

### DisplayColumnNUnique

- **Purpose**: Calculates and prints the number of unique values in a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which to count unique values.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnNUnique`".

#### DisplayColumnNUnique Example

Below is an example demonstrating how to use the Transformation `DisplayColumnNUnique`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnNUnique

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'responses' with a 'answer' column

  display_nunique = DisplayColumnNUnique(dataframes='responses', column='answer')  # Initialize the DisplayColumnNUnique step

  pypeline.add_steps([display_nunique])
  pypeline.execute()
```

---

### DisplayColumnDType

- **Purpose**: Retrieves and prints the data type of a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which to display the data type.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayColumnDType`".

#### DisplayColumnDType Example

Below is an example demonstrating how to use the Transformation `DisplayColumnDType`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayColumnDType

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'records' with a 'date' column

  display_dtype = DisplayColumnDType(dataframes='records', column='date')  # Initialize the DisplayColumnDType step

  pypeline.add_steps([display_dtype])
  pypeline.execute()
```

---

### DisplayStringCount

- **Purpose**: Computes and prints the frequency counts of unique string values in a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which to display value counts.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayStringItemCount`".

#### DisplayStringCount Example

Below is an example demonstrating how to use the Transformation `DisplayStringCount`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayStringCount

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'reviews' with a 'comment' column

  display_string_count = DisplayStringCount(dataframes='reviews', column='comment')  # Initialize the DisplayStringCount step

  pypeline.add_steps([display_string_count])
  pypeline.execute()
```

---

### DisplayMostFrequentString

- **Purpose**: Determines and prints the most frequent string(s) (mode) in a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index for which to determine the most frequent item(s).
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayMostFrequentString`".

#### DisplayMostFrequentString Example

Below is an example demonstrating how to use the Transformation `DisplayMostFrequentString`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayMostFrequentString

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'feedback' with a 'rating' column

  display_most_frequent = DisplayMostFrequentString(dataframes='feedback', column='rating')  # Initialize the DisplayMostFrequentString step

  pypeline.add_steps([display_most_frequent])
  pypeline.execute()
```

---

### DisplayAllCategories

- **Purpose**: Retrieves and prints all unique categories present in a specified column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index from which to retrieve unique categories.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplayAllCategories`".

#### DisplayAllCategories Example

Below is an example demonstrating how to use the Transformation `DisplayAllCategories`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplayAllCategories

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'products' with a 'category' column

  display_categories = DisplayAllCategories(dataframes='products', column='category')  # Initialize the DisplayAllCategories step

  pypeline.add_steps([display_categories])
  pypeline.execute()
```

---

### DisplaySubstringOccurrence

- **Purpose**: Counts and prints the total number of occurrences of a specified substring in a given column for each DataFrame in the context.
- **Parameters**:
  - `dataframes` (str or List[str]): Name(s) of the DataFrame(s) in the context.
  - `column` (str or int): The column name or index in which to count substring occurrences.
  - `substring` (str): The substring whose occurrences are to be counted.
  - `step_name` (str, optional): Name of this transformation step. Defaults to "`DisplaySubstringOccurrence`".

#### DisplaySubstringOccurrence Example

Below is an example demonstrating how to use the Transformation `DisplaySubstringOccurrence`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import DisplaySubstringOccurrence

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers a dataframe called 'logs' with a 'message' column

  display_substring = DisplaySubstringOccurrence(dataframes='logs', column='message', substring='error')  # Initialize the DisplaySubstringOccurrence step 

  pypeline.add_steps([display_substring])
  pypeline.execute()
```

---