# Context Module Documentation

This module defines the `Context` dataclass for managing pandas DataFrames and metadata. The `Context` class provides a structured way to store and retrieve multiple DataFrames, manage related metadata, and track DataFrame addresses.

---

## Overview

The `Context` class is designed to facilitate the organization of DataFrames along with their associated metadata. It provides methods to set and retrieve DataFrames, update metadata, and manage the overall state of a context.

---

## Class: Context

### Attributes

- **`context_name`** (*str*):  
  The name of the context.

- **`dataframes`** (*Dict[str, pd.DataFrame]*):  
  A dictionary mapping names to pandas DataFrame objects.

- **`metadata`** (*Dict[str, Any]*):  
  A dictionary to store metadata about the context.

- **`dataframe_addr`** (*Dict[str, id]*):  
  A dictionary mapping DataFrame names to their unique identifiers.

### Methods

- **`__post_init__(self)`**  
  *Post-initialization method.*  
  - Initializes the metadata with a key `'num_dfs'` set to zero.
  - Additional normalization of the context name can be added here.

- **`set_context_name(self, name)`**  
  Sets the name of the context.
  - **Args:**  
    - `name` (*str*): The new context name.

- **`get_dataframe(self, name)`**  
  Retrieves a DataFrame by its name.
  - **Args:**  
    - `name` (*str*): The name of the DataFrame to retrieve.
  - **Returns:**  
    - The DataFrame associated with the given name, or `None` if not found.

- **`set_dataframe(self, name, df)`**  
  Sets a DataFrame in the context with the given name.
  - **Args:**  
    - `name` (*str*): The name to assign to the DataFrame.
    - `df` (*pd.DataFrame*): The DataFrame to store.

- **`get_dataframe_names(self)`**  
  Gets the names of all stored DataFrames.
  - **Returns:**  
    - A view of the names of the DataFrames stored in the context.

- **`get_metadata(self, key)`**  
  Retrieves a metadata value by its key.
  - **Args:**  
    - `key` (*str*): The key for the metadata item.
  - **Returns:**  
    - The metadata value associated with the key, or `None` if not found.

- **`set_metadata(self, key, value)`**  
  Sets a metadata value for a given key.
  - **Args:**  
    - `key` (*str*): The key for the metadata item.
    - `value` (*Any*): The value to be stored.

- **`added_dataframe_update_metadata(self)`**  
  Updates the metadata to reflect the current number of DataFrames.
  - Updates the `'num_dfs'` key in the metadata dictionary to match the number of stored DataFrames.

- **`add_dataframe(self, name, df)`**  
  Adds a new DataFrame to the context and updates the metadata accordingly.
  - **Args:**  
    - `name` (*str*): The name to assign to the DataFrame.
    - `df` (*pd.DataFrame*): The DataFrame to add.

- **`__str__(self)`**  
  Returns a string representation of the context.
  - Prints the context name, the dataframes, and the metadata.
  - Returns an empty string.

---

## Usage Example

Below is an example demonstrating how to create and use a `Context` instance:

```python
import pandas as pd
from context_module import Context  # Adjust the import as needed

# Create a sample DataFrame
df_sample = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z']
})

# Initialize a Context instance
my_context = Context(context_name="SampleContext")

# Add the DataFrame to the context
my_context.add_dataframe("df_sample", df_sample)

# Retrieve the DataFrame by name
retrieved_df = my_context.get_dataframe("df_sample")
print("Retrieved DataFrame:")
print(retrieved_df)

# Update metadata manually
my_context.set_metadata("description", "This context contains sample data.")
print("Metadata:", my_context.metadata)

# Display all DataFrame names stored in the context
print("DataFrame Names:", list(my_context.get_dataframe_names()))