from .chunker import Chunker

class RecursiveChunker(Chunker):
    def __init__(self, step_index):
        super().__init__(step_index)

    def calculate_chunks(self):
        chunk_keys = list(self.chunk_index.keys())
        num_keys = len(chunk_keys)
        it = 0

        while any(not self.chunk_index[key][3] for key in chunk_keys):
            key = chunk_keys[it]
            it = (it + 1) % num_keys

            chunk_size, current_chunk, num_rows, finished_calculating = self.chunk_index[key]

            