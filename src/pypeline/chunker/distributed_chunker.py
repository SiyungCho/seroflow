"""
Module: distributed_chunker

This module implements the DistributedChunker class, a concrete subclass of the Chunker abstract base class.
DistributedChunker calculates chunk coordinates using a distributed strategy. It computes the total number of chunks
by multiplying the number of chunks available for each step and then evenly distributes rows among those chunks.
This approach ensures a balanced allocation of rows across all chunks for efficient parallel or segmented processing.
"""

import math
from .chunker import Chunker

class DistributedChunker(Chunker):
    """
    DistributedChunker

    A concrete implementation of the Chunker class that calculates chunk coordinates using a distributed strategy.
    Instead of processing chunks in a round-robin manner, this chunker computes the total number of chunks based on
    the individual chunk sizes of the steps and then calculates the start and end indices for each chunk, ensuring an
    even distribution of rows.
    """
    def __init__(self, step_index):
        """
        Distributed Chunker Class Constructor
        Initializes the DistributedChunker object by invoking the parent class constructor
        and then invoking the calculate_chunks() method to populate the coordinate queue.

        Arguments:
            step_index (OrderedDict): 
                An ordered dictionary mapping step keys to step objects in the pypeline.
        """
        super().__init__(step_index)

    def calculate_chunks(self):
        """
        Public method: calculate_chunks()
        Calculates the chunk coordinates for each step in the chunk index.
        The chunk coordinates are added to the coordinate queue.
        Recusive Chunker calculates the chunk coordinates by first calculating the total number of chunks
        and then iterating through each chunk to calculate the start and end index for each chunk.
        By using the total number of chunks, the method calculates the base number of rows per chunk and the remainder.
        This way, the method can distribute the remainder among the chunks.
        ie the chunks will have an even distribution of rows.
        """
        chunk_keys = list(self.chunk_index.keys())

        chunks_per_key = {}
        for key in chunk_keys:
            chunk_size, _, num_rows, _ = self.chunk_index[key]
            chunks_per_key[key] = math.ceil(num_rows / chunk_size)

        total_chunks = 1
        for key in chunk_keys:
            total_chunks *= chunks_per_key[key]

        for chunk in range(total_chunks):
            for key in chunk_keys:
                _, _, num_rows, _ = self.chunk_index[key]
                base = num_rows // total_chunks
                remainder = num_rows % total_chunks
                start_idx = chunk * base + min(chunk, remainder)
                end_idx = start_idx + base + (1 if chunk < remainder else 0)
                if start_idx == end_idx:
                    break
                self.coordinate_queue.put((start_idx, end_idx))
