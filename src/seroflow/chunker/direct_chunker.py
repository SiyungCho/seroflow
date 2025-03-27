"""
Module: direct_chunker

This module implements the DirectChunker class, an implementation of the Chunker abstract class.
DirectChunker computes chunk coordinates based on each step's defined chunk size and the
total number of rows. It enqueues tuples representing the start and stop indices for processing
each chunk, ensuring that data is divided into manageable segments. 
Once all chunks for a step are processed, it pads the coordinate queue with (None, None) tuples.
"""
from .chunker import Chunker

class DirectChunker(Chunker):
    """
    DirectChunker

    A concrete implementation of the Chunker class that calculates chunk coordinates directly.
    It iterates through the steps that support chunking, computes the start and stop indices 
    based on the chunk size and total row count, and populates the coordinate queue with values.
    If a step has finished processing all available rows, a (None, None) tuple is enqueued.
    """
    def __init__(self, step_index):
        """
        Direct Chunker Class Constructor method
        Initializes the DirectChunker object by invoking the parent class constructor and
        then invoking the calculate_chunks() method to populate the coordinate queue.

        Arguments:
            step_index (OrderedDict): 
                An ordered dictionary mapping step keys to step objects in the Pipeline.
        """
        super().__init__(step_index=step_index)

    def calculate_chunks(self):
        """
        Public method: calculate_chunks()
        Calculates the chunk coordinates for each step in the chunk index.
        The chunk coordinates are added to the coordinate queue.
        Calculates by using the chunk size and the number of rows in the step.
        If the chunk size is greater than the number of rows, the chunk size is set
        to the number of rows.
        A (None, None) tuple is added to the queue for each step that has finished calculating.

        This version produces tuples of (start_index, nrows) for compatibility with
        pandas read_csv's skiprows and nrows.
        """
        chunk_keys = list(self.chunk_index.keys())
        num_keys = len(chunk_keys)
        it = 0

        while any(not self.chunk_index[key][3] for key in chunk_keys):
            key = chunk_keys[it]
            it = (it + 1) % num_keys

            chunk_size, current_chunk, num_rows, finished_calculating = self.chunk_index[key]

            if finished_calculating:
                start_idx = None
                nrows = None
            else:
                start_idx = current_chunk * chunk_size
                if start_idx <= num_rows:
                    stop_idx = start_idx + chunk_size
                    if stop_idx >= num_rows:
                        stop_idx = num_rows
                        finished_calculating = True
                    nrows = stop_idx - start_idx
                else:
                    # If start_idx is beyond num_rows, there's nothing to read.
                    start_idx = None
                    nrows = None
                    finished_calculating = True

            self.coordinate_queue.put((start_idx, nrows))
            new_current_chunk = current_chunk + (1 if not finished_calculating else 0)
            self.chunk_index[key] = (chunk_size, new_current_chunk, num_rows, finished_calculating)

        # pad the final output so that the queue size is a multiple of the number of keys
        while self.coordinate_queue.qsize() % num_keys != 0:
            self.coordinate_queue.put((None, None))
