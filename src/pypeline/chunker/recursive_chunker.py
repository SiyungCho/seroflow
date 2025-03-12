from .chunker import Chunker
import math

class RecursiveChunker(Chunker):
    def __init__(self, step_index):
        super().__init__(step_index)

    def calculate_chunks(self):
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
