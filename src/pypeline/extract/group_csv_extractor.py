"""
"""

import pandas as pd
from ..utils.utils import check_directory, gather_files, remove_extension
from ..extract.csv_extractor import CSVExtractor

class GroupCSVExtractor():

    def __init__(self, source, chunk_size=None, **kwargs):

        if not check_directory(source): 
            raise FileNotFoundError("Error directory not found")

        self.source = source
        self.file_paths, self.file_names = gather_files(self.source, ["csv"])
        extractors = {}

        for file in self.file_paths:
            new_extractor = CSVExtractor(file, chunk_size=chunk_size, kwargs=kwargs)
            extractors.append(new_extractor)
        return extractors
