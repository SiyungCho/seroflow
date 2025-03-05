from dataclasses import dataclass, field
from typing import Dict, Any
import pandas as pd

@dataclass
class context:
    context_name: str
    dataframes: Dict[str, pd.DataFrame] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    dataframe_addr: Dict[str, id] = field(default_factory=dict)

    def __post_init__(self):
        self.metadata['num_dfs'] = 0
        # Normalize context name if necessary

    def set_context_name(self, name):
        self.context_name = name

    def get_dataframe(self, name):
        return self.dataframes.get(name)

    def set_dataframe(self, name, df):
        self.dataframes[name] = df

    def get_metadata(self, key):
        return self.metadata.get(key)

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def added_dataframe_update_metadata(self):
        self.metadata['num_dfs'] = len(list(self.dataframes.keys()))

    def add_dataframe(self, name, df):
        self.set_dataframe(name, df)
        self.added_dataframe_update_metadata()

    def __str__(self):
        print(self.context_name)
        print(self.dataframes)
        print(self.metadata)
        return ""