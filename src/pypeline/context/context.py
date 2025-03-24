"""
Module that defines the Context dataclass for managing pandas DataFramesand metadata.

The Context class provides a structured way to store and retrieve multiple DataFrames,
manage related metadata, and track DataFrame addresses.
"""

from dataclasses import dataclass, field
from typing import Dict, Any
import pandas as pd


@dataclass
class Context:
    """
    A class to represent a context containing pandas DataFrames and metadata.

    Attributes:
        context_name (str): The name of the context.
        dataframes (Dict[str, pd.DataFrame]): A dictionary mapping names to DataFrame objects.
        metadata (Dict[str, Any]): A dictionary to store metadata about the context.
        dataframe_addr (Dict[str, id]): Dictionary mapping DataFrame names to their ids.
    """
    context_name: str
    dataframes: Dict[str, pd.DataFrame] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    dataframe_addr: Dict[str, id] = field(default_factory=dict)

    def __post_init__(self):
        """
        Post-initialization processing for the Context instance.

        This method initializes the 'num_dfs' metadata to zero.
        Additional normalization of the context name can be added here.
        """
        self.metadata['num_dfs'] = 0
        # Normalize context name if necessary

    def set_context_name(self, name):
        """
        Set the name of the context.

        Args:
            name (str): The new context name.
        """
        self.context_name = name

    def get_dataframe(self, name):
        """
        Retrieve a DataFrame by its name.

        Args:
            name (str): The name of the DataFrame to retrieve.

        Returns:
            pd.DataFrame or None: 
                The DataFrame associated with the given name, or None if not found.
        """
        return self.dataframes.get(name)

    def set_dataframe(self, name, df):
        """
        Set a DataFrame in the context with the given name.

        Args:
            name (str): The name to assign to the DataFrame.
            df (pd.DataFrame): The DataFrame to store.
        """
        self.dataframes[name] = df

    def get_dataframe_names(self):
        """
        Get the names of all stored DataFrames.

        Returns:
            KeysView[str]: A view of the names of the DataFrames stored in the context.
        """
        return self.dataframes.keys()

    def get_metadata(self, key):
        """
        Retrieve a metadata value by its key.

        Args:
            key (str): The key for the metadata item.

        Returns:
            Any or None: The metadata value associated with the key, or None if not found.
        """
        return self.metadata.get(key)

    def set_metadata(self, key, value):
        """
        Set a metadata value for a given key.

        Args:
            key (str): The key for the metadata item.
            value (Any): The value to be stored.
        """
        self.metadata[key] = value

    def added_dataframe_update_metadata(self):
        """
        Update the metadata to reflect the current number of DataFrames.

        This method updates the 'num_dfs' key in the metadata dictionary to match
        the number of DataFrames currently stored.
        """
        self.metadata['num_dfs'] = len(list(self.dataframes.keys()))

    def add_dataframe(self, name, df):
        """
        Add a new DataFrame to the context and update metadata accordingly.

        This method sets the DataFrame with the given name and then updates the
        metadata to reflect the new total count of DataFrames.

        Args:
            name (str): The name to assign to the DataFrame.
            df (pd.DataFrame): The DataFrame to add.
        """
        self.set_dataframe(name, df)
        self.added_dataframe_update_metadata()

    def delete_dataframe(self, name: str) -> bool:
        """
        Delete a DataFrame from the context by its name and update metadata accordingly.

        Args:
            name (str): The name of the DataFrame to delete.
        
        Returns:
            bool: True if the DataFrame was successfully deleted, False otherwise.
        """
        if name in self.dataframes:
            # Remove the DataFrame from the main dictionary
            del self.dataframes[name]
            
            # Remove the DataFrame address if it exists
            if name in self.dataframe_addr:
                del self.dataframe_addr[name]
            
            # Update the metadata count of DataFrames
            self.added_dataframe_update_metadata()
            return True
        else:
            print(f"DataFrame with name '{name}' does not exist.")
            return False

    def __str__(self):
        """
        Return a string representation of the Context.

        This implementation prints the context name, the dataframes, and the metadata.
        Note that it returns an empty string after printing.

        Returns:
            str: An empty string.
        """
        print(self.context_name)
        print(self.dataframes)
        print(self.metadata)
        return ""
