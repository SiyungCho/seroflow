# String Transformations Documentation

This module implements a suite of transformation classes that can perform String Manipulations on DataFrames in the Pypeline Context. Each transformation class extends the base `Transformation` class and is designed to operate with Pypeline Object. The available transformations include:

- **RemoveCharacterFromColumn**: Removes all occurrences of a specified character from a string column.
- **RemoveCharactersFromColumn**: Removes all occurrences of a list of characters from a string column.
- **ReplaceStringInColumn**: Replaces occurrences of a specified substring with another string in a column.

## String Transformation Classes
 
### RemoveCharacterFromColumn

- **Purpose**: Removes all occurrences of a specific character from a specified string column in a DataFrame.
- **Parameters**:
  - `dataframe` (str): The name of the DataFrame to be updated in the context.
  - `column` (str): The name of the column to process.
  - `char_to_remove` (str): The character to remove from the column's string values.
  - `step_name` (str, optional): The name of the transformation step. Defaults to "`RemoveCharacterFromColumn`".
  - `on_error` (str, optional): The error handling strategy.

#### RemoveCharacterFromColumn Example

Below is an example demonstrating how to use the Transformation `RemoveCharacterFromColumn`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import RemoveCharacterFromColumn

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  remove_char = RemoveCharacterFromColumn(dataframe="states", column="name", char_to_remove="&") # Initialize the RemoveCharacterFromColumn Step

  pypeline.add_steps([remove_char])
  pypeline.execute()
```

---

### RemoveCharactersFromColumn

- **Purpose**: Removes all occurrences of a list of specified characters from a target string column in a DataFrame.
- **Parameters**:
  - `dataframe` (str): The name of the DataFrame to update in the context.
  - `column` (str): The name of the column to process.
  - `chars_to_remove` (iterable): A list or iterable of characters to remove from the column's string values.
  - `step_name` (str, optional): The name of the transformation step. Defaults to "`RemoveCharactersFromColumn`".
  - `on_error` (str, optional): The error handling strategy.

#### RemoveCharactersFromColumn Example

Below is an example demonstrating how to use the Transformation `RemoveCharactersFromColumn`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import RemoveCharactersFromColumn

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  remove_chars = RemoveCharactersFromColumn(dataframe="states", column="name", char_to_remove=["&", "#", "*"]) # Initialize the RemoveCharactersFromColumn Step

  pypeline.add_steps([remove_chars])
  pypeline.execute()
```

---

### ReplaceStringInColumn

- **Purpose**: Replaces all occurrences of a specified substring with another string in a target column of a DataFrame.
- **Parameters**:
  - `dataframe` (str): The name of the DataFrame to update in the context.
  - `column` (str): The name of the column in which the replacement is to occur.
  - `to_replace` (str): The substring to be replaced.
  - `replacement` (str): The string to replace the substring with.
  - `step_name` (str, optional): The name of the transformation step. Defaults to "`ReplaceStringInColumn`".
  - `on_error` (str, optional): The error handling strategy.

#### ReplaceStringInColumn Example

Below is an example demonstrating how to use the Transformation `ReplaceStringInColumn`:

```python
  import pandas as pd
  from pypeline import Pypeline
  from pypeline.transform import ReplaceStringInColumn

  pypeline = Pypeline()
  pypeline.target_extractor = ... # Add Extractor which gathers data

  replace_string = ReplaceStringInColumn(dataframe="states", column="name", to_replace="and", replacement="&") # Initialize the ReplaceStringInColumn Step

  pypeline.add_steps([replace_string])
  pypeline.execute()
```

---
