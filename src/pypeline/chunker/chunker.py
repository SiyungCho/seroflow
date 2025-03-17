from abc import abstractmethod
from collections import OrderedDict
from queue import Queue
from copy import deepcopy
from ..types import is_extractor, is_loader

class Chunker:
    def __init__(self, step_index):
        self.chunk_index = OrderedDict()
        for step_key, step in step_index.items():
            if hasattr(step, 'chunk_size') and is_extractor(step, _raise=False):
                if not(step.chunk_size is None):
                    self.chunk_index[step_key] = (step.chunk_size, 0, step.get_max_row_count(), False)
	
            if is_loader(step, _raise=False) and hasattr(step, 'exists'):
                if step.exists != 'append':
                    raise ValueError("All loaders must be set to 'append' when using chunking")
        self.keep_executing = True
        self.coordinate_queue = Queue()
        self.saved_state = {}
        self.calculate_chunks()

    def check_keep_executing(self):
        if self.coordinate_queue.qsize() == 0:
            return False
        return True

    def enqueue(self, value):
        self.coordinate_queue.put(value)

    def dequeue(self):
        value = self.coordinate_queue.get()
        self.keep_executing = self.check_keep_executing()
        return value

    def reload(self):
        return self.saved_state['parameter_index'], self.saved_state['globalcontext']

    def save(self, **kwargs):
        for key, value in kwargs.items():
            self.saved_state[key] = deepcopy(value)

    def print_coordinate_queue(self):
        """
        Print the current state of the coordinate queue, including the total number of items
        and each individual coordinate in order.
        """
        queue_size = self.coordinate_queue.qsize()
        print(f"Coordinate Queue (Total items: {queue_size}):")
        if self.coordinate_queue.empty():
            print("The coordinate queue is empty.")
        else:
            for idx, coordinate in enumerate(list(self.coordinate_queue.queue), start=1):
                print(f"  {idx}: {coordinate}")

    @abstractmethod
    def calculate_chunks(self):
        """
        """
