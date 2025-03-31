Chunker
========================

The modules documented here define the interface and concrete implementation for ``Seroflow`` ``Pipeline`` partitioning (chunking).
They provide a common interface to calculating chunk coordinates, managing a queue of chunking coordinates, and saving/restoring the chunker's state.
This ensures consistent chunker behavior across different chunking strategies.

Overview
-----------------------------------

This documentation covers three modules:

- **chunker**: Defines the ``Chunker`` abstract class, which specifies the interface for creating custom chunkers.
  
- **direct_chunker**: A concrete subclass of ``Chunker`` that calculates chunk coordinates in a round-robin fashion.
It computes start and stop indices based on each ``Step's`` ``chunk_size`` and total number of rows, enqueuing tuples of ``(start_index, nrows)`` for use with ``Extractor`` Objects.

- **distributed_chunker** : A concrete subclass of ``Chunker`` that calculates chunk coordinates using a distributed strategy.
It computes the total number of chunks by combining the number of chunks available for each step and then evenly distributes rows among those chunks.
This ensures a balanced allocation of rows across all chunks for efficient parallel or segmented processing.

Chunker 
-------------------------------

``Chunker`` is an abstract base class (inheriting from ``ABC``) for implementing chunking. 
Derived classes must implement all the abstract methods to handle chunking operations.
This design enforces a standardized interface and behavior across different chunking strategies.

.. autoclass:: seroflow.chunker.chunker.Chunker
   :members:
   :show-inheritance:
   :undoc-members:

DirectChunker
---------------------------------------

A concrete implementation of the ``Chunker`` class that calculates chunk coordinates directly in a round-robin manner.

.. autoclass:: seroflow.chunker.direct_chunker.DirectChunker
   :members:
   :show-inheritance:
   :undoc-members:


Initialization Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``LFUCache``: ::

  from seroflow import Pipeline
  from seroflow.chunker import DirectChunker

  pipeline = Pipeline()
  pipeline.execute(chunker=DirectChunker) # Execute Pipeline with chunker

DirectChunker Methodology
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``DirectChunker`` partitions each extractor’s dataset into fixed‑size blocks in a simple round‑robin sequence.
It does not attempt to balance work across ``Extractors`` — instead, it iterates through each step in order, slicing off one chunk at a time until all rows for that step are consumed, then moving on to the next.

Key behaviors:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Fixed‑size chunks**: 
   Each chunk’s row count equals the extractor’s configured chunk_size, except the final chunk (which may be smaller if the total row count isn’t a multiple of chunk_size).

- **Round‑robin ordering**: 
   Execution cycles through ``Extractors`` in ``Pipeline`` order. On each cycle, it emits one chunk coordinate ``(start_index, nrows)`` for each ``Extractor`` that still has rows remaining.
- **Skipping finished extractors**: 
   Once an extractor has emitted all of its chunks, subsequent cycles enqueue ``(None, None)`` for that step—telling ``Pipeline`` to skip it.

- **Total iterations = sum of chunks across all ``Extractors``.**

- **Logic**:

  - Retrieves a list of keys from ``self.chunk_index`` and iterates over them in a round-robin fashion.
  - For each key, retrieves the current chunk data: ``(chunk_size, current_chunk, num_rows, finished_calculating)``.
  - If a step has finished processing, enqueues ``(None, None)``.
  - Otherwise, calculates:

    - ``start_idx`` as ``current_chunk * chunk_size``.
    - ``stop_idx`` as the minimum of ``start_idx + chunk_size`` and ``num_rows``.
    - ``nrows`` as ``stop_idx - start_idx``.
    - Updates the finished flag if ``stop_idx`` reaches ``num_rows``.

  - Enqueues the tuple ``(start_idx, nrows)``.
  - Updates the chunk index with the new current chunk count and finished flag.
  - Pads the coordinate queue with ``(None, None)`` tuples so that the total number of enqueued values is a multiple of the number of keys.


DirectChunker Methodology Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: direct_chunker.md
   :parser: myst_parser.sphinx_

DistributedChunker
--------------------------------------------

A concrete implementation of the ``Chunker`` class that calculates chunk coordinates using a distributed strategy.
Instead of processing chunks in a round-robin manner, ``DistributedChunker`` computes the total number of chunks based on the individual chunk sizes of the steps and then evenly distributes rows among those chunks.
This approach ensures a balanced allocation of rows for efficient parallel or segmented processing.

.. autoclass:: seroflow.chunker.distributed_chunker.DistributedChunker
   :members:
   :show-inheritance:
   :undoc-members:

Initialization Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object with an ``LFUCache``: ::

  from seroflow import Pipeline
  from seroflow.chunker import DistributedChunker

  pipeline = Pipeline()
  pipeline.execute(chunker=DistributedChunker) # Execute Pipeline with chunker

DistributedChunker Methodology
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``DistributedChunker`` evenly spreads rows across a unified set of execution chunks so that every run contains work for every extractor (unless the extractor has fewer total rows than the number of chunks).
It computes the total number of chunks as the product of each extractor’s chunk‑count, then divides each extractor’s rows evenly across those chunks.

Key behaviors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Balanced distribution**: 
   Rows for each extractor are split into nearly equal‑sized pieces, minimizing empty (zero‑row) runs.

- **Total iterations = ∏ (ceil(total_rows_i / chunk_size_i)) for all extractors.**

- **Remainder handling**: 
   If rows don’t divide evenly, earlier chunks receive one extra row until the remainder is exhausted.

- **Zero‑row chunks**: 
   If an extractor’s total rows are fewer than the total number of chunks, some chunks will contain (None, None) for that extractor.

- **Logic**:
  - **Step 1:** Determine the number of chunks per step.
    - For each key in ``self.chunk_index``, retrieve ``(chunk_size, _, num_rows, _)``.
    - Calculate the number of chunks for that step as ``ceil(num_rows / chunk_size)`` and store it in a dictionary ``chunks_per_key``.
  - **Step 2:** Compute the total number of chunks.
    - Multiply the number of chunks for each step together to get ``total_chunks``.
  - **Step 3:** For each chunk (from 0 to ``total_chunks - 1``):
    - For each key in the chunk index:
      - Retrieve ``num_rows`` for the step.
      - Calculate the base number of rows per chunk as ``num_rows // total_chunks`` and the remainder as ``num_rows % total_chunks``.
      - Determine ``start_idx`` as ``chunk * base + min(chunk, remainder)``.
      - Compute ``end_idx`` as ``start_idx + base + (1 if chunk < remainder else 0)``.
      - Calculate ``nrows`` as ``end_idx - start_idx``.
      - If ``nrows`` is 0, break out of the loop for that key.
      - Enqueue the tuple ``(start_idx, nrows)`` in the coordinate queue.
  - This produces tuples of ``(start_index, nrows)`` that are compatible with functions such as pandas ``read_csv``.

DistributedChunker Methodology Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. include:: distributed_chunker.md
   :parser: myst_parser.sphinx_
