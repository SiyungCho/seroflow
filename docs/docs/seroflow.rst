.. _seroflow:

Seroflow
================

This documentation provides a framework for building, managing, and executing a series of data processing steps with ``Seroflow's`` ``Pipeline`` Object.
It integrates custom logging, caching, context management, transformation utilities, chunking, and type validation to offer a robust and extensible architecture for data pipeline workflows.

Overview
-----------------------------------

The module implements the ``Pipeline`` class. Below are several key features:

- **Dynamic Step Management**: Add individual or multiple steps that are automatically indexed and validated.

- **Global Context**: Share parameters and dataframes across steps through a centralized context.

- **Caching**: Optionally cache intermediate states to enable execution resumption.

- **Custom Logging**: Utilize built-in or user-defined logging for debugging and monitoring.
   
- **Chunked Execution**: Process large datasets in segments by integrating chunking mechanisms.

- **Execution Modes**: Operate in ``"DEV"`` or ``"PROD"`` modes to tailor execution behavior (e.g., skipping loader steps in ``"DEV"`` mode).

Pipeline
-------------------------------

The core component of the module is the ``Pipeline`` class. It encapsulates the logic for constructing and executing a data pipeline.

.. autoclass:: seroflow.Pipeline
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to initialize a ``Pipeline`` object: ::

  from seroflow import Pipeline
  from seroflow.cache import LFUCache

  # Initialize a pipeline with caching and logging enabled in development mode.
  pipeline = Pipeline(cache=LFUCache, logger=True, mode="DEV")

Pipeline Basics
-------------------------------

Extractors, Loaders and Step Addition
^^^^^^^^^^^^^^^^^

- ``pipeline.target_extractor``:

  - A ``Target Extractor`` is simply an ``Extractor`` object that is initialized to always be performed as the first step in the ``Pipeline`` execution. 
  - A ``Target Extractor`` is initialized to ensure the ``Pipeline`` object begins with an extraction of data and has some form of data stored internally. 
  - In ``"PROD"`` mode, a ``Target Extractor`` **must** be set to ensure data is available for future steps. 
  - ``MultiExtractor`` objects can also be used.

- ``pipeline.target_loader``:

  - Similarly a ``Target Loader`` is simply a ``Loader`` object that is initialized to always be performed as the last step in the ``Pipeline`` execution. 
  - A ``Target Loader`` is initialized to ensure the ``Pipeline`` object ends with a the release of data stored internally. 
  - In ``"DEV"`` mode, ``Loader`` Steps are skipped and this includes the ``Target Loader`` step as well. 
  - Unlike ``Target Extractor's`` a ``Target Loader`` is **not** mandatory. 
  - This means that simply adding intermediate ``Load`` steps can turn an ETL (Extract, Transform, Load) into an ELT (Extract, Load, Transform) pipeline if so desired.

- ``add_step(self, step)`` and ``add_steps(self, steps)``:

  - These methods are for adding one or multiple ``Step`` objects to the pipeline. 
  - When a ``MultiExtractor`` step is added, each internal ``Extractor`` is added as an individual step. 
  - The ``Pipeline`` Object will execute all steps added using these methods sequentially.
  - Any ``Step`` Object (including ``Extractor`` and ``Loader`` Objects) can be added to the ``Pipeline`` execution using these methods.

Pipeline Execution
^^^^^^^^^^^^^^^^^

- ``execute(self, chunker=None)``: Begins the ``Pipeline`` execution and performs several validation steps:

  - Adds target steps (extractor/loader) to the pipeline.
  - Step names are hashed and configured based on their position and step name. This means that multiple steps with the same step name can be added to Pipeline execution and they will be treated as seperate instances.
  - Optionally sets up a chunker for processing large datasets.
  - Uses a progress bar (via ``tqdm``) to show progress through the steps.
  - If caching is enabled, execution may resume from a cached checkpoint.
  - All DataFrames extracted using ``Extractor`` steps are stored inside a ``Context`` Object within the ``Pipeline`` Object.

Usage Example
^^^^^^^^^^^^^^^^^

In this example, execution of steps will occur in this order: 

- MultiCSVExtractor
- TransposeDataFrame
- ExcelLoader.

::

  from seroflow import Pipeline
  from seroflow.extract import MultiCSVExtractor # Gathering multiple csv files
  from seroflow.load import ExcelLoader # Load data to excel sheet
  from seroflow.transform import TransposeDataFrame # Transpose Dataframes gathered

  pipeline = Pipeline()
  pipeline.target_extractor = MultiCSVExtractor(...) # Set Target Extractor as MultiCSVExtractor
  pipeline.target_loader = ExcelLoader(...) # Set Target Loader as ExcelLoader

  transpose_step = TransposeDataFrame(...) # Create Transpose DataFrame Step

  pipeline.add_steps([transpose_step, ...]) # Add Transpose DataFrame Step
  pipeline.execute() # Execute Steps added

Pipeline Caching
^^^^^^^^^^^^^^^^^

The ``Pipeline`` Object enables caching in both *global* and *in execution* states.
When the ``cache`` parameter is set to ``True`` a default ``LFUCache`` will be used.
Custom Caches can be created and passed into the ``cache`` parameter however, they must confer with the ``AbstractCache`` interface. 

Please review the :ref:`cache` documentation for further information.

Global Caching
^^^^^^^^^^^^^^^^^

Caching can be enabled globally to avoid re-running completed steps.
When enabled, a ``.cache``directory stores compressed snapshots of the pipeline’s state after each step, along with a ``config.json`` file that records hashes of each step’s source code and configuration. 
Before execution, these hashes are compared to detect any changes in code or step order.
If a change is found, execution resumes from the step immediately after the last unchanged step, loading its saved state into the pipeline and skipping all prior steps. 

Global Caching stores the state's in **non-volatile** memory (.gzip files) and therefore are not destroyed upon program completion unless a ``reset_cache`` ``Step`` is included in execution.

- Custom Caches can be created using the ``AbstractCache`` interface.
- Global caching is configured using the ``store(...)``, ``load(...)`` and ``reset(...)`` methods.

In Execution Caching
^^^^^^^^^^^^^^^^^

In Execution Caching is a seperate but similar caching functionality.
It allows state caching and loading within the execution of ``Pipeline`` Steps.
This can essentially allow for 'branching' within the ``Pipeline`` execution. 

States are cached in-memory and are therefore **volatile**, meaning that all cached states are destroyed upon program completion.

- ``cache_state(...)``
   Returns a ``CacheState`` step that, when executed, caches the current state of the pipeline.

- ``reload_cached_state(...)``
   Returns a ``ReloadCacheState`` step that reloads a cached state during execution.

- ``reset_cache(...)``
   Returns a ``ResetCache`` step that resets the cache. If ``delete_directory`` is set to ``True``, it deletes the cache directory.

Please Review the :ref:`cache_transformation` documentation for further information on ``CacheState``, ``ReloadCacheState`` and ``ResetCache``.

Usage Example
^^^^^^^^^^^^^^^^^

In this example, execution of steps will occur in this order: 

 - CSVExtractor: stores csv_df
 - CacheState: caches csv_df
 - TransposeDataFrame: transposes csv_df, stores transposed_df
 - ReloadCacheState: reloads csv_df
 - PivotDataFrame: pivots csv_df, stores pivot_df
 - ExcelLoader: loads selected df
 
::

   from seroflow import Pipeline
   from seroflow.extract import CSVExtractor
   from seroflow.load import ExcelLoader
   from seroflow.transform import TransposeDataFrame
   from seroflow.transform import PivotDataFrame

   pipeline = Pipeline()
   pipeline.target_extractor = CSVExtractor(...)
   pipeline.target_loader = ExcelLoader(...)

   transpose_step = TransposeDataFrame(...)
   pivot_step = PivotDataFrame(...)

   pipeline.add_steps([pipeline.cache_state(...), transpose_step, pipeline.reload_state(...), pivot_step]) # Add the cache_state and reload_state steps
   pipeline.execute()

Pipeline Chunking
^^^^^^^^^^^^^^^^^

Chunking is an essential technique which can be used to efficiently and safely process large datasets.
The ``Pipeline`` Object enables chunking by passing A ``Chunker`` Class into the ``chunker`` parameter when using the ``pipeline.execute(chunker=ChunkerClass)`` method. 
Once a ``Chunker`` Class is passed, all Extractor steps containing the keyword argument ``chunk_size`` will be analyzed and chunking indexes (ie the start index and number of rows for each chunk) will be calculated using the ``calculate_chunks()`` method.
Then, ``Pipeline`` execution will be partitioned horizontally, until all chunks are processed.

Custom chunker classes can be created and used however, they must conform to the ``Chunker`` interface.
It is highly recommended you understand the chunking methodology a selected Chunker employs before executing the ``Pipeline`` as unexpected scenarios may arise. 

Please review the :ref:`chunker` documentation for further information.

DirectChunker
^^^^^^^^^^^^^^^^^
The ``DirectChunker`` methodology, calculates chunks purely based on the ``chunk_size``. 
If multiple ``Extractor`` objects are used where one has already processed all chunks of its dataset however, another still has other chunks, the completed ``Extractor`` step will be passed a ``(None, None)`` tuple as its chunk parameter, essentially skipping the step.

- In a basic case, if one Dataset is used containing 12 rows of data, with a ``chunk_size`` of 5 then, ``Pipeline`` execution will occur 3 times. The first execution will contain the first 5 rows of data. The second execution will contain the next 5 rows of data. Lastly the third execution will contain the final 2 rows of data.
- In a multi ``Extractor`` case, say 2 datasets are extracted. The first dataset contains 10 rows of data with a ``chunk_size`` of 2 and the second dataset contains 5 rows of data with a ``chunk_size`` of 4. In this case, ``Pipeline`` execution will occur 5 times. The first execution will contain the first 2 rows of the first dataset and the first 4 rows in the second dataset. The second execution will contain the next 2 rows of the first dataset and the final row of the second dataset. The third and subsequent executions will contain the next 2 rows of the first dataset and no row of the second dataset, essentially skipping this step.

**Logic**:

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

DistributedChunker
^^^^^^^^^^^^^^^^^

The ``DistributedChunker`` methodology, calculates chunks by evenly distributing the number of rows based on the ``chunk_size``.
If multiple ``Extractor`` objects are used where one has already processed all chunks of its dataset however, another still has other chunks, the completed ``Extractor`` step calculate the downstream number of chunks and distribute the upstream chunks evenly. 
This ensures that all executions contain data for each extractor step, unless there are more execution chunks then number of rows in the dataset.

- In a basic case, if one Dataset is used containing 12 rows of data, with a ``chunk_size`` of 5 then, ``Pipeline`` execution will occur 3 times. The first execution will contain the first 5 rows of data. The second execution will contain the next 5 rows of data. Lastly the third execution will contain the final 2 rows of data.
- In a multi ``Extractor`` case, say 2 datasets are extracted. The first dataset contains 12 rows of data with a ``chunk_size`` of 6 and the second dataset contains 6 rows of data with a ``chunk_size`` of 2. In this case, ``Pipeline`` execution will occur 6 times. Each execution will contain 2 rows of the first dataset and a single row of the second dataset.

**Logic**:

- **Step 1**: Determine the number of chunks per step.

   - For each key in ``self.chunk_index``, retrieve ``(chunk_size, _, num_rows, _)``.
   - Calculate the number of chunks for that step as ``ceil(num_rows / chunk_size)`` and store it in a dictionary ``chunks_per_key``.

- **Step 2**: Compute the total number of chunks.

   - Multiply the number of chunks for each step together to get ``total_chunks``.

- **Step 3**: For each chunk (from 0 to ``total_chunks - 1``) and for each key in the chunk index:
   
   - Retrieve ``num_rows`` for the step.
   - Calculate the base number of rows per chunk as ``num_rows // total_chunks`` and the remainder as ``num_rows % total_chunks``.
   - Determine ``start_idx`` as ``chunk * base + min(chunk, remainder)``.
   - Compute ``end_idx`` as ``start_idx + base + (1 if chunk < remainder else 0)``.
   - Calculate ``nrows`` as ``end_idx - start_idx``.
   - If ``nrows`` is 0, break out of the loop for that key.
   - Enqueue the tuple ``(start_idx, nrows)`` in the coordinate queue.

- This produces tuples of ``(start_index, nrows)`` that are compatible with functions such as pandas ``read_csv``.
  
Usage Example
^^^^^^^^^^^^^^^^^

In this example, say there are 2 chunks execution will occur in this order:

- CSVExtractor
- TransposeDataFrame
- ExcelLoader
- CSVExtractor
- TransposeDataFrame
- ExcelLoader
  
::

  from seroflow import Pipeline
  from seroflow.extract import CSVExtractor 
  from seroflow.load import ExcelLoader 
  from seroflow.transform import TransposeDataFrame
  from seroflow.chunker import DistributedChunker # Load DistributedChunker class

  pipeline = Pipeline()
  pipeline.target_extractor = CSVExtractor(...)
  pipeline.target_loader = ExcelLoader(...) 

  transpose_step = TransposeDataFrame(...)

  pipeline.add_steps([transpose_step, ...])
  pipeline.execute(chunker=DistributedChunker) # Initialize execution with the Distributed Chunker

Pipeline Context Management
^^^^^^^^^^^^^^^^^

Another key component to the ``Pipeline`` object is the Context dataclass.
A context object dynamically stores DataFrame(s) and relevant metadata.
The ``Pipeline`` object stores any DataFrame(s) gathered by ``Extractor`` Steps into a global context object.
This global context stores the DataFrames between ``Steps`` during execution and any changes made to the DataFrames within a ``Step`` then updates the DataFrames inside the global context. 

``Subcontext`` objects are passed to each ``Step`` that requests the use of a DataFrame.
These subcontexts contain only the requested DataFrame.
This ensures that each Step does not load all DataFrames only the ones required.
It is important to understand how the ``Pipeline`` object interacts with a context primarily in the scenarios below.
However, in most basic cases context objects will not need to be handled by users. 

Please review the :ref:`context` documentation for further information.

Case 1: Creating Custom Steps
^^^^^^^^^^^^^^^^^

There are multiple ways users can create custom ``Step`` objects, however, all of them require an understanding of how the ``context`` keyword is used.
When a custom step function is created, the function's signature must contain the argument ``context`` in order to have a subcontext object passed into it via the ``Pipeline`` object.
This is only if a context is to be used, if a context is not required in the ``Step`` function, then the ``context`` argument is also not required.
It is recommended to set the ``context`` argument as the first item in the function signature, however, this is also not required.

Usage Example
^^^^^^^^^^^^^^^^^

In this example, we create a custom Step object which can be passed into the ``Pipeline`` execution. ::

  from seroflow import Pipeline
  from seroflow.step import Step # Import the Step class
  
  @Step(dataframes=['df1', ...], params={'a':10, ...}) # Create a Custom Step using the wrapper format
  def sample_function(context, a, b=1):
    df1 = context.get_dataframe('df1')
    print(a)
    return context, b

  pipeline = Pipeline()
  pipeline.add_step(sample_function) # We can add the Custom Step function by passing the function name as an object

Please review the :ref:`step_doc` documentation for further information.

Case 2: Creating Custom Extractors and Loaders
^^^^^^^^^^^^^^^^^

Because ``Extractor`` and ``Loader`` Objects are simply subclasses of the ``Step`` class, custom variations can be created in a similar manner.
For custom ``Extractors``, an empty subcontext is given, and dataframes can be appended to this subcontext. 
The subcontext is then returned at the end of the function where it is parsed by the ``Pipeline`` Object and the global context is updated.
For custom ``Loaders``, any requested dataframes are inserted into a subcontext via the global context.
The subcontext dataframes can then be accessed and loaded to the target destination.
It is important to note that for custom ``Extractors`` and ``Loaders``, the wrapper method of creating steps is not possible and therefore the a custom subclass of the ``Step`` class must be created.
In addition, the step function must be configured with the name: ``func(...)``.

Usage Example
^^^^^^^^^^^^^^^^^

In this example, we create a custom Extractor object ::

  from seroflow import Pipeline
  from seroflow.extract import Extractor # Import the Extractor class which is the interface for extractors and a subclass of the Step Class
  
  class SampleExtractor(Extractor):
    ...
    def func(context):
      df = ... # retrieve dataframe from source
      context.append_dataframe("sample_df", df)
      return context

Usage Example
^^^^^^^^^^^^^^^^^

In this example, we create a custom Loader object ::

  from seroflow import Pipeline
  from seroflow.load import Loader # Import the Loader class which is the interface for loaders and a subclass of the Step Class
  
  class SampleExtractor(Extractor):
    ...
    def func(context):
      df = context.get_dataframe("sample_df")
      df... # load dataframe to target

Please review the :ref:`extractors` and :ref:`loaders` documentation for further information.

Case 3: Creating Custom Caches
^^^^^^^^^^^^^^^^^

When caching, the ``Pipeline`` object also caches the current state of the global context.
This saves the current state of the DataFrames at a particular step and allows execution to continue from any cached state.
In some cases, users may want to create a custom ``Cache`` using the ``AbstractCache`` interface, which simply caches a subcontext of the global context, storing only a subset of the DataFrames instead of all of them.
This is possible by manipulating the ``store(self, step_index, parameter_index, global_context, step_key)`` method to remove any unwanted DataFrames before the actual store is executed.

Please review the :ref:`cache` documentation for further information.
