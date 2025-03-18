# Chunker Module Documentation

This module defines the base functionality for partitioning (chunking) in the pypeline framework. It provides an abstract `Chunker` class responsible for calculating chunk coordinates, managing a queue of chunking coordinates, and saving/restoring the chunker's state. In addition, the module includes concrete implementations—`DirectChunker` and `DistributedChunker`—which compute chunk coordinates using different strategies to ensure that data is processed in manageable segments.

---

## Overview

- **Chunker:**  
  The abstract base class that:
  - Iterates through a pypeline's step index to identify steps supporting chunking.
  - For each extractor step with a defined `chunk_size`, initializes chunk coordinates as a tuple:
    - `(chunk_size, 0, step.get_max_row_count(), False)`
  - Validates that loader steps are configured to append data (i.e., their `exists` attribute is set to `'append'`).
  - Manages a coordinate queue for chunk processing.
  - Provides methods for saving and reloading the chunker state.
  - Declares an abstract method `calculate_chunks()` that must be implemented by subclasses.

- **DirectChunker:**  
  A concrete subclass of `Chunker` that calculates chunk coordinates in a round-robin fashion. It computes start and stop indices based on each step's `chunk_size` and total number of rows, enqueuing tuples of `(start_index, nrows)` for use with functions like pandas `read_csv`.

- **DistributedChunker:**  
  A concrete subclass of `Chunker` that calculates chunk coordinates using a distributed strategy. It computes the total number of chunks by combining the number of chunks available for each step and then evenly distributes rows among those chunks. This ensures a balanced allocation of rows across all chunks for efficient parallel or segmented processing.

---

## Class: Chunker

### Constructor

#### `__init__(self, step_index)`

- **Arguments:**
  - `step_index` (*OrderedDict*): An ordered dictionary mapping step keys to step objects in the pypeline.

- **Behavior:**
  - Iterates through the provided step index.
  - For each extractor step with a defined `chunk_size` (i.e., not `None`), initializes chunk coordinates as:
    - `(chunk_size, 0, step.get_max_row_count(), False)`
  - Validates that any loader step (determined via `is_loader`) has its `exists` attribute set to `'append'`.
  - Initializes:
    - `self.chunk_index` as an `OrderedDict` containing the chunk coordinates.
    - `self.coordinate_queue` as a `Queue` for managing chunk coordinates.
    - `self.saved_state` as a dictionary for storing the chunker state.
  - Calls `calculate_chunks()` to populate the coordinate queue.

### Methods

- **`check_keep_executing(self)`**  
  Checks if the coordinate queue is empty.
  - **Returns:**  
    - *bool*: `True` if the queue is not empty; otherwise, `False`.

- **`enqueue(self, value)`**  
  Adds a value to the coordinate queue.
  - **Arguments:**  
    - `value` (*tuple*): A tuple containing start and stop index values corresponding to a chunk.

- **`dequeue(self)`**  
  Removes a value from the coordinate queue and updates the execution flag.
  - **Returns:**  
    - *tuple*: A tuple containing start and stop index values corresponding to a chunk.
  - **Behavior:**  
    - Updates `self.keep_executing` based on the current queue size.

- **`reload(self)`**  
  Reloads the chunker state.
  - **Returns:**  
    - *tuple*: A tuple containing the saved parameter index and global context from `self.saved_state`.

- **`save(self, **kwargs)`**  
  Saves the chunker state.
  - **Arguments:**  
    - `**kwargs`: Keyword arguments (e.g., parameter index and global context) to be saved.
  - **Behavior:**  
    - Iterates over the provided key-value pairs and stores a deep copy of each in `self.saved_state`.

- **`calculate_chunks(self)`** *(Abstract Method)*  
  Calculates coordinate values for the chunker.
  - **Note:**  
    Subclasses must implement this method to provide the specific logic for calculating chunk coordinates.

---

## Class: DirectChunker

A concrete implementation of the `Chunker` class that calculates chunk coordinates directly in a round-robin manner.

### Constructor

#### `__init__(self, step_index)`

- **Arguments:**
  - `step_index` (*OrderedDict*): An ordered dictionary mapping step keys to step objects in the pypeline.
- **Behavior:**
  - Calls the parent `Chunker` constructor.
  - Automatically invokes `calculate_chunks()` to populate the coordinate queue.

### Methods

#### `calculate_chunks(self)`

Calculates the chunk coordinates for each step in the chunk index and enqueues them.

- **Logic:**
  - Retrieves a list of keys from `self.chunk_index` and iterates over them in a round-robin fashion.
  - For each key, retrieves the current chunk data: `(chunk_size, current_chunk, num_rows, finished_calculating)`.
  - If a step has finished processing, enqueues `(None, None)`.
  - Otherwise, calculates:
    - `start_idx` as `current_chunk * chunk_size`.
    - `stop_idx` as the minimum of `start_idx + chunk_size` and `num_rows`.
    - `nrows` as `stop_idx - start_idx`.
    - Updates the finished flag if `stop_idx` reaches `num_rows`.
  - Enqueues the tuple `(start_idx, nrows)`.
  - Updates the chunk index with the new current chunk count and finished flag.
  - Pads the coordinate queue with `(None, None)` tuples so that the total number of enqueued values is a multiple of the number of keys.

---

## Class: DistributedChunker

A concrete implementation of the `Chunker` class that calculates chunk coordinates using a distributed strategy. Instead of processing chunks in a round-robin manner, `DistributedChunker` computes the total number of chunks based on the individual chunk sizes of the steps and then evenly distributes rows among those chunks. This approach ensures a balanced allocation of rows for efficient parallel or segmented processing.

### Constructor

#### `__init__(self, step_index)`

- **Arguments:**
  - `step_index` (*OrderedDict*): An ordered dictionary mapping step keys to step objects in the pypeline.
- **Behavior:**
  - Invokes the parent `Chunker` constructor.
  - Automatically calls `calculate_chunks()` to populate the coordinate queue.

### Methods

#### `calculate_chunks(self)`

Calculates the chunk coordinates for each step in the chunk index and enqueues them.

- **Logic:**
  - **Step 1:** Determine the number of chunks per step.
    - For each key in `self.chunk_index`, retrieve `(chunk_size, _, num_rows, _)`.
    - Calculate the number of chunks for that step as `ceil(num_rows / chunk_size)` and store it in a dictionary `chunks_per_key`.
  - **Step 2:** Compute the total number of chunks.
    - Multiply the number of chunks for each step together to get `total_chunks`.
  - **Step 3:** For each chunk (from 0 to `total_chunks - 1`):
    - For each key in the chunk index:
      - Retrieve `num_rows` for the step.
      - Calculate the base number of rows per chunk as `num_rows // total_chunks` and the remainder as `num_rows % total_chunks`.
      - Determine `start_idx` as `chunk * base + min(chunk, remainder)`.
      - Compute `end_idx` as `start_idx + base + (1 if chunk < remainder else 0)`.
      - Calculate `nrows` as `end_idx - start_idx`.
      - If `nrows` is 0, break out of the loop for that key.
      - Enqueue the tuple `(start_idx, nrows)` in the coordinate queue.
  - This produces tuples of `(start_index, nrows)` that are compatible with functions such as pandas `read_csv`.

---