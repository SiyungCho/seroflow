# Chunker Documentation

The modules documented here define the base structure and a concrete implementation for `Pipeline` partitioning (chunking). They provide a common interface to calculating chunk coordinates, managing a queue of chunking coordinates, and saving/restoring the chunker's state. This ensures consistent chunker behavior across different chunking strategies.

## Overview

This documentation covers three modules:

- **chunker:**  
  The abstract base class that:
  - Iterates through a `Pipeline`'s step index to identify steps supporting chunking.
  - For each extractor step with a defined `chunk_size`, initializes chunk coordinates as a tuple:
    - `(chunk_size, 0, step.get_max_row_count(), False)`
  - Validates that loader steps are configured to append data (i.e., their `exists` attribute is set to `'append'`).
  - Manages a coordinate queue for chunk processing.
  - Provides methods for saving and reloading the chunker state.
  - Declares an abstract method `calculate_chunks()` that must be implemented by subclasses.

- **direct_chunker:**  
  A concrete subclass of `Chunker` that calculates chunk coordinates in a round-robin fashion. It computes start and stop indices based on each step's `chunk_size` and total number of rows, enqueuing tuples of `(start_index, nrows)` for use with `Extractor` Objects.

- **distributed_chunker:**  
  A concrete subclass of `Chunker` that calculates chunk coordinates using a distributed strategy. It computes the total number of chunks by combining the number of chunks available for each step and then evenly distributes rows among those chunks. This ensures a balanced allocation of rows across all chunks for efficient parallel or segmented processing.

## Class: Chunker

`Chunker` is an abstract base class (inheriting from `ABC`) for implementing chunking mechanisms within the `Pipeline` framework. Derived classes must implement all the abstract methods below to handle chunking operations. This design enforces a standardized interface and behavior across different chunking strategies.

- **`__init__(self, step_index)`**
  - **Parameters:**
    - `step_index` (*OrderedDict*): An ordered dictionary mapping step keys to step objects in the `Pipeline`.

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

- **`check_keep_executing(self)`**  
  Checks if the coordinate queue is empty.
  - **Returns:**  
    - *bool*: `True` if the queue is not empty; otherwise, `False`.

- **`enqueue(self, value)`**  
  Adds a value to the coordinate queue.
  - **Parameters:**  
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
  - **Parameters:**  
    - `**kwargs`: Keyword arguments (e.g., parameter index and global context) to be saved.
  - **Behavior:**  
    - Iterates over the provided key-value pairs and stores a deep copy of each in `self.saved_state`.

- **`calculate_chunks(self)`** *(Abstract Method)*  
  Calculates coordinate values for the chunker.
  - **Note:**  
    Subclasses must implement this method to provide the specific logic for calculating chunk coordinates.

## Class: DirectChunker

A concrete implementation of the `Chunker` class that calculates chunk coordinates directly in a round-robin manner.

## Initialization

- **`__init__(self, step_index)`**  
  Initializes a new `DirectChunker` instance.
  
  **Parameters:**
    - `step_index` (*OrderedDict*): An ordered dictionary mapping step keys to step objects in the `Pipeline`.
  **Behavior:**
    - Calls the parent `Chunker` constructor.
    - Automatically invokes `calculate_chunks()` to populate the coordinate queue.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `LFUCache`:

```python
  from seroflow import Pipeline
  from seroflow.chunker import DirectChunker

  pipeline = Pipeline()
  pipeline.execute(chunker=DirectChunker) # Execute Pipeline with chunker
```

## DirectChunker Methodology
The `DirectChunker` partitions each extractor’s dataset into fixed‑size blocks in a simple round‑robin sequence. It does not attempt to balance work across extractors — instead, it iterates through each step in order, slicing off one chunk at a time until all rows for that step are consumed, then moving on to the next.

### Key behaviors:
- Fixed‑size chunks: Each chunk’s row count equals the extractor’s configured chunk_size, except the final chunk (which may be smaller if the total row count isn’t a multiple of chunk_size).
- Round‑robin ordering: Execution cycles through extractors in `Pipeline` order. On each cycle, it emits one chunk coordinate (start_index, nrows) for each extractor that still has rows remaining.
- Skipping finished extractors: Once an extractor has emitted all of its chunks, subsequent cycles enqueue (None, None) for that step—telling `Pipeline` to skip it.
- Total iterations = sum of chunks across all extractors.

#### DirectChunker Methodology Example

<div style="background:rgba(0,0,0,0.2); border-left:4px solid #0366d6; padding:1em; border-radius:4px;">

Imagine three extractors (A, B, C) with differing dataset sizes and chunk sizes:

| Extractor | Total Rows | Chunk Size | # Chunks | Coordinates (start, nrows)      |
|:---------:|:----------:|:----------:|:--------:|:--------------------------------|
| **A**     |     7      |     3      |    3     | (0,3)<br/>(3,3)<br/>(6,1)       |
| **B**     |     4      |     2      |    2     | (0,2)<br/>(2,2)                 |
| **C**     |     5      |     4      |    2     | (0,4)<br/>(4,1)                 |

The greatest # Chunks in this case belongs to extractor A.
Therefore, the `Pipeline` will execute 3 seperate times:

| Execution |       A       |       B       |       C       |
|:---------:|:-------------:|:-------------:|:-------------:|
| 1         | (0,3)         | (0,2)         | (0,4)         |
| 2         | (3,3)         | (2,2)         | (4,1)         |
| 3         | (6,1)         | —             | —             |

</div>

## DirectChunker Methods

### `calculate_chunks(self)`

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

## Class: DistributedChunker

A concrete implementation of the `Chunker` class that calculates chunk coordinates using a distributed strategy. Instead of processing chunks in a round-robin manner, `DistributedChunker` computes the total number of chunks based on the individual chunk sizes of the steps and then evenly distributes rows among those chunks. This approach ensures a balanced allocation of rows for efficient parallel or segmented processing.

## Initialization

- **`__init__(self, step_index)`**  
  Initializes a new `DistributedChunker` instance.
  
  **Parameters:**
    - `step_index` (*OrderedDict*): An ordered dictionary mapping step keys to step objects in the `Pipeline`.
  **Behavior:**
    - Calls the parent `Chunker` constructor.
    - Automatically invokes `calculate_chunks()` to populate the coordinate queue.
  
#### Initialization Example

Below is a simple example that shows how to initialize a `Pipeline` object with an `LFUCache`:

```python
  from seroflow import Pipeline
  from seroflow.chunker import DistributedChunker

  pipeline = Pipeline()
  pipeline.execute(chunker=DistributedChunker) # Execute Pipeline with chunker
```

## DistributedChunker Methodology
The `DistributedChunker` evenly spreads rows across a unified set of execution chunks so that every run contains work for every extractor (unless the extractor has fewer total rows than the number of chunks). It computes the total number of chunks as the product of each extractor’s chunk‑count, then divides each extractor’s rows evenly across those chunks.

### Key behaviors
- Balanced distribution: Rows for each extractor are split into nearly equal‑sized pieces, minimizing empty (zero‑row) runs.
- Total iterations = ∏ (ceil(total_rows_i / chunk_size_i)) for all extractors.
- Remainder handling: If rows don’t divide evenly, earlier chunks receive one extra row until the remainder is exhausted.
- Zero‑row chunks: If an extractor’s total rows are fewer than the total number of chunks, some chunks will contain (None, None) for that extractor.

#### DistributedChunker Methodology Example

<div style="background:rgba(0,0,0,0.2); border-left:4px solid #0366d6; padding:1em; border-radius:4px;">

Imagine three extractors (A, B, C) with differing dataset sizes and chunk sizes:

| Extractor | Total Rows | Chunk Size | # Chunks | Coordinates              |
|:---------:|:----------:|:----------:|:--------:|:-------------------------|
| **X**     |     100    |     50     |    2     | (0,16), (16,16)<br/>(32,16), (48,16)<br/>(64,16), (80,16)|
| **Y**     |     60     |     20     |    3     | (0,10), (10,10)<br/>(20,10), (30,10)<br/>(40,10), (50,10)|
| **Z**     |     30     |     30     |    1     | (0,5), (5,5)<br/>(10,5), (15,5)<br/>(20,5), (25,5)       |

The total # of executions = #Chunks X * #Chunks Y * #Chunks Z = 2 × 3 × 1 = 6.

Now to calculate the chunk coordinates we distribute the total rows across all 6 executions.

Extractor X: 100/6 = 16 Remainder 4

Extractor Y: 60/6 = 10 

Extractor Z: 30/6 = 5

Therefore, the `Pipeline` will execute 6 seperate times:

| Execution |       X       |       Y       |       Z       |
|:---------:|:-------------:|:-------------:|:-------------:|
| 1         | (0,16)        | (0,10)        | (0,5)         |
| 2         | (16,16)       | (10,10)       | (5,5)         |
| 3         | (32,16)       | (20,10)       | (10,5)        |
| 4         | (48,16)       | (30,10)       | (15,5)        |
| 5         | (64,16)       | (40,10)       | (20,5)        |
| 6         | (80,16)       | (50,10)       | (25,5)        |

The last execution will include the final chunk as well as any remaining rows of data.

</div>

## DistributedChunker Methods

### `calculate_chunks(self)`

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
