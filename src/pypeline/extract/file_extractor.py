# """

# """

# import pandas as pd
# from ..utils.utils import check_directory, gather_files, remove_extension
# from ..extract.extractor import Extractor


# class FileExtractor(Extractor):
#     """
#     """

#     def __init__(self, source, step_name, chunk_size, **kwargs):
#         """
#         """
#         super().__init__(step_name=step_name, func= self.func if chunk_size is None else self.chunk_func, chunk_size=chunk_size)

#     def func(self, context):
#         pass

#     def chunk_func(self, context, chunk_coordinates):
#         pass   
    
#     def get_max_row_count(self):
#         max_rows = 0
#         for file in self.file_paths:
#             with open(file, 'r') as f:
#                 row_count = sum(1 for row in f)
#                 if row_count > max_rows:
#                     max_rows = row_count
#         return max_rows
