from .chunker import Chunker

class DirectChunker(Chunker):
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

            if finished_calculating:
                start_idx = None
                stop_idx = None
            else:
                start_idx = current_chunk * chunk_size
                if start_idx <= num_rows:
                    # Calculate stop index.
                    stop_idx = start_idx + chunk_size
                    if stop_idx >= num_rows:
                        stop_idx = num_rows
                        finished_calculating = True

            # Put the chunk coordinates into the coordinate queue.
            self.coordinate_queue.put((start_idx, stop_idx))

            # Update the chunk info for this key.
            self.chunk_index[key] = (chunk_size, current_chunk + (1 if not finished_calculating else 0), num_rows, finished_calculating)

        if self.coordinate_queue.qsize() % 2 == 1:
            self.coordinate_queue.put((None, None))

    def __str__(self):
        print(self.keep_executing)
        print(self.coordinate_queue)
        print(self.saved_state)
        print(self.chunk_index)
        return ""