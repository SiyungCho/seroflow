from abc import ABC, abstractmethod
from ..types import is_extractor, is_loader
"""
TODO: 
- add chunking:
Method 1 Batching:
- add add chunksize flag to all extractors. and global chunk (bool) to all extractors
- when parsing steps check for extractors, check if global chunk is true then add extractor step to chunk index, if not then step level chunking is performed (ie data is only chunked till next step)
- create a chunk index, step_key -> (chunksize, current_chunk, total_rows)
- ensure all subsequent loaders have 'append' turned on

cases:
- one(one) to one, (one extractor, one df, one loader)
- one(many) to one, (one extractor, many df, one loader)
- one(one) to many, (one extractor, one df, many loader)
- one(many) to many, (one extractor, many df, many loader)
- many(one, one) to one, (many extractor, combo df, one loader)
- many(one, many) to one, (many extractor, combo df, one loader)
- many(many, one) to one, (many extractor, combo df, one loader)
- many(many, many) to one, (many extractor, combo df, one loader)

- many(one, many) to many, (many extractor, combo df, many loader)
- many(many, one) to many, (many extractor, combo df, many loader)
- many(one, one) to many, (many extractor, combo df, many loader)
- many(many, many) to many, (many extractor, combo df, many loader)

**need to figure out how caching is going to be used with this

one(one) to one
one file (1 df:100 rows, chunk 50) -> 50 rows -> append via loader
                                   -> 50 rows -> append via loader
one(many) to one
many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 50) -> df1:50 rows, df2: 50 rows, df3:50rows -> append via loader
                                                            -> df1:50 rows, df2: 50 rows, df3:empty  -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> append via loader
one(one) to many
one file (1 df:100 rows, chunk 50) -> 50 rows -> append via loader -> transformation -> append via loader
                                   -> 50 rows -> append via loader -> transformation -> append via loader

one(many) to many
many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 50) -> df1:50 rows, df2: 50 rows, df3:50rows -> append via loader -> transformation -> append via loader
                                                            -> df1:50 rows, df2: 50 rows, df3:empty  -> append via loader -> transformation -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> append via loader -> transformation -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> append via loader -> transformation -> append via loader
many(one, one) to one
** issue is that the 2nd transformation occurs twice on the initial dataframe chunks so we need to split the initial dataframe again (recursive splitting)
one file (1 df1:150 rows, chunk 50) -> 50 rows -> transformation -> one file (1 df2:100 rows, chunk 50) -> df1: 25 rows, df2:16rows -> transformation -> append via loader
                                                                                                        -> df1: 25 rows, df2:16rows -> transformation -> append via loader
                                    -> 50 rows -> transformation -> one file (1 df2:100 rows, chunk 50) -> df1: 25 rows, df2:16rows -> transformation -> append via loader
                                                                                                        -> df1: 25 rows, df2:16rows -> transformation -> append via loader
                                    -> 50 rows -> transformation -> one file (1 df2:100 rows, chunk 50) -> df1: 25 rows, df2:16rows -> transformation -> append via loader
                                                                                                        -> df1: 25 rows, df2:20rows -> transformation -> append via loader
many(one, many) to one
one file (1 df1:100 rows, chunk 20) -> 20 rows -> transformation -> many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 5) -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                ... 40 downstream chunksbut df 1 only has 20 rows to split from, so rows are split among first 20 chunks and rest are empty
                                    -> 20 rows -> transformation -> many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 5) -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                    -> 20 rows -> transformation -> many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 5) -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                    -> 20 rows -> transformation -> many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 5) -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                    -> 20 rows -> transformation -> many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 5) -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->
                                                                                                                                -> df1:  rows, df2:  rows, df3:  rows, df4:  rows ->                                                                                                                                
many(many, one) to one
many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 50) -> df1:50 rows, df2: 50 rows, df3:50rows -> one file (1 df4:100 rows, chunk 50) -> df1: 25 rows, df2: 25 rows, df3: 25 rows, df4: 12 rows -> transformation -> append via loader
                                                                                                                                            -> df1: 25 rows, df2: 25 rows, df3: 25 rows, df4: 12 rows -> transformation -> append via loader
                                                            -> df1:50 rows, df2: 50 rows, df3:empty  -> one file (1 df4:100 rows, chunk 50) -> df1: 25 rows, df2: 25 rows, df3: empty rows, df4: 12 rows -> transformation -> append via loader
                                                                                                                                            -> df1: 25 rows, df2: 25 rows, df3: empty rows, df4: 12 rows -> transformation -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> one file (1 df4:100 rows, chunk 50) -> df1: empty rows, df2: 25 rows, df3: empty rows, df4: 12 rows -> transformation -> append via loader
                                                                                                                                            -> df1: empty rows, df2: 25 rows, df3: empty rows, df4: 12 rows -> transformation -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> one file (1 df4:100 rows, chunk 50) -> df1: empty rows, df2: 25 rows, df3: empty rows, df4: 12 rows -> transformation -> append via loader
                                                                                                                                            -> df1: empty rows, df2: 25 rows, df3: empty rows, df4: 16 rows -> transformation -> append via loader
many(many, many) to one
many files (3 dfs , 100 rows, 200 rows, 150 rows, chunk 50) -> df1:50 rows, df2: 50 rows, df3:50rows -> one file (2 dfs, 100 rows, 150 rows, chunk 50) -> df1: 16 rows, df2: 16 rows, df3: 16 rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: 16 rows, df2: 16 rows, df3: 16 rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: 18 rows, df2: 18 rows, df3: 18 rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                            -> df1:50 rows, df2: 50 rows, df3:empty  -> one file (2 dfs, 100 rows, 150 rows, chunk 50) -> df1: 16 rows, df2: 16 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: 16 rows, df2: 16 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: 18 rows, df2: 18 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> one file (2 dfs, 100 rows, 150 rows, chunk 50) -> df1: empty rows, df2: 16 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: empty rows, df2: 16 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: empty rows, df2: 18 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                            -> df1:empty, df2: 50 rows, df3:empty    -> one file (2 dfs, 100 rows, 150 rows, chunk 50) -> df1: empty rows, df2: 16 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: empty rows, df2: 16 rows, df3: empty rows, df4: 8 rows, df5: 12 -> transformation -> append via loader
                                                                                                                                                       -> df1: empty rows, df2: 18 rows, df3: empty rows, df4: 12 rows, df5: 18 -> transformation -> append via loader

downstream chunk formulas: 
total downstream chunks = # chunks ex1 * # chunks ex2 * ...
chunksize = ex# total rows/total downstream chunks (up to ex#)
"""

# Chunking implementation:
# we are going to implement 2 main principles behind chunking data
# 1. Recursive Chunking
#     - at each extractor
#         - number of chunks is determined by the floor(largest df/chunksize)
#         - # rows is determined proportionally to amount of chunks (spread evenly)
#     - multiple extractors
#         - previous chunks and new data rows are spread evenly across new chunks downstream
# 2. Direct Chunking
#     - at each extractor
#         - number of chunks is determined by the floor(largest df/chunksize)
#         - # rows is equal to chunk size, once smaller dfs reach end then empty df is used in their place for subsequent chunks
#     - multiple extractors
#         - directly gather data one after another by chunksize

# - on step level, set chunksize
# - from ... import RecursiveChunker
# - on pypeline.execute(chunk_method = RecursiveChunker)
# - inside pypeline:
#     - chunker is init and added to pypeline obj
#     - chunker iterates through steps, makes sure allloaders are set to append, finds all extractor steps with chunksize and appends to internal index; step_key -> chunksize, current_chunk
#     - somehow figure out number of rows in each to be extracted df
#     - calculate all # chunks, chunk coordinates, (different depending if recursive or direct)
#     - branch execution using cache? (give special keys to cache)
#     - send coords to extractor functions by manip internal step kwargs

# - need to add get_number_rows abstract method to all extractor steps, always ran on post_init

# Interacting with Cache
# - * There is only ever 1 cache, each branch/sub branch can access the same cache 

class Chunker:
    def __init__(self, step_index):
        self.chunk_index = {}
        for step_key, step in step_index.items():
            if hasattr(step, 'chunk_size') and is_extractor(step, _raise=False):
                self.chunk_index[step_key] = (step.chunk_size, 0, step.get_number_rows())
            
            if is_loader(step, _raise=False) and hasattr(step, 'exists'):
                if step.exists != 'append':
                    raise ValueError("All loaders must have 'append' as the 'exists' parameter when using chunking")
        self.calculate_chunks()
        self.keep_executing = False
        self.coordinate_queue = {}

    @abstractmethod
    def calculate_chunks(self):
        pass

    @abstractmethod
    def enqueue(self):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    @abstractmethod
    def reload(self):
        pass
