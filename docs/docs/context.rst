Context
========================

This module defines the ``Context`` dataclass for managing ``pandas`` DataFrames and metadata. 
The ``Context`` class provides a structured way to store and retrieve multiple DataFrames, manage related metadata, and track DataFrame addresses.

Overview
-------------------------------
The ``Context`` class is designed to facilitate the organization of DataFrames along with their associated metadata.
It provides methods to set and retrieve DataFrames, update metadata, and manage the overall state of a ``context``.

Context
-------------------------------

.. automodule:: seroflow.context.context
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize and use a ``Context``: ::

  import pandas as pd
  from seroflow.context import Context  # Adjust the import as needed

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