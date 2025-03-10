from .chunker import Chunker

class DirectChunker(Chunker):
    def __init__(self, step_index):
        super().__init__(step_index)

    def calculate_chunks(self):
        pass