# Pypeline Documentation

The `pypeline` module provides an ETL pypeline framework for building, managing, and executing a series of data processing steps. It integrates custom logging, caching, context management, transformation utilities, chunking, and type validation to offer a robust and extensible architecture for ETL workflows.

## Overview

The module implements an ETL pypeline framework using the `Pypeline` class. It offers functionality for managing and executing a sequence of data processing steps with support for caching, logging, parameter management, and execution chunking.

**Key Features:**

- **Dynamic Step Management:** Add individual or multiple steps that are automatically indexed and validated.
- **Global Context:** Share parameters and dataframes across steps through a centralized context.
- **Caching:** Optionally cache intermediate states to enable execution resumption.
- **Custom Logging:** Utilize built-in or user-defined logging for debugging and monitoring.
- **Chunked Execution:** Process large datasets in segments by integrating chunking mechanisms.
- **Execution Modes:** Operate in `"DEV"`, `"TEST"`, or `"PROD"` modes to tailor execution behavior (e.g., skipping loader steps in `"DEV"` mode).

## Class: Pypeline

The core component of the module is the `Pypeline` class. It encapsulates the logic for constructing and executing an ETL pipeline.

## Initialization

- **`__init__(self, cache=False, logger=False, mode="DEV")`**  
  Initializes a new `Pypeline` instance with optional caching, logging, and mode settings.
  
  **Parameters:**
  
  - `cache` *(Bool, AbstractCache)*: 
    - Either `False`, `True` (to instantiate a default `LFUCache`), or a user-defined cache (subclass of `AbstractCache`).
  - `logger` *(Bool, logging.logger)*: 
    - Either `False`, `True` (to instantiate a default `CustomLogger`), or a user-defined `logging.Logger` object.
  - `mode` *("DEV", "TEST", "PROD")*: 
    - A string defining the mode of operation. Valid values are `"DEV"`, `"TEST"`, or `"PROD"`.
    - `"DEV"`, Development phase: `Load` steps are skipped.
    - `"TEST"`, Test phase: currently no difference from `"DEV"` (v1.0)
    - `"PROD"`, Production phase: All steps are executed without intermediate validation.

#### Initialization Example

Below is a simple example that shows how to initialize a `Pypeline` object:

```python
  from pypeline import Pypeline
  from pypeline.cache import LFUCache

  # Initialize a pypeline with caching and logging enabled in development mode.
  pypeline = Pypeline(cache=LFUCache, logger=True, mode="DEV")
```

## Basic Execution

### Extractors, Loaders and Step Addition

- **`pypeline.target_extractor`**
  - A `Target Extractor` is simply an `Extractor` object that is initialized to always be performed as the first step in the `Pypeline` execution. 
  - A `Target Extractor` is initialized to ensure the `Pypeline` object begins with an extraction of data and has some form of data stored internally. 
  - In `"PROD"` mode, a `Target Extractor` **must** be set to ensure data is available for future steps. 
  - `MultiExtractor` objects can also be used.
- **`pypeline.target_loader`**
  - Similarly a `Target Loader` is simply a `Loader` object that is initialized to always be performed as the last step in the `Pypeline` execution. 
  - A `Target Loader` is initialized to ensure the `Pypeline` object ends with a the release of data stored internally. 
  - In `"DEV"` mode, `Loader` Steps are skipped and this includes the `Target Loader` step as well. 
  - Unlike Target Extractor's a Target Loader is **not** mandatory. 
  - This means that simply adding intermediate Load steps can turn an ETL (Extract, Transform, Load) into an ELT (Extract, Load, Transform) pipeline if so desired.
- **`add_step(self, step)`** and **`add_steps(self, steps)`**  
  - These methods are for adding one or multiple `Step` objects to the pypeline. 
  - When a `MultiExtractor` step is added, each internal `Extractor` is added as an individual step. 
  - The `Pypeline` Object will execute all steps added using these methods sequentially.
  - Any `Step` Object (including `Extractor` and `Loader` Objects) can be added to the `Pypeline` execution using these methods.

### Execution

- **`execute(self, chunker=None)`**  
  Begins the `Pypeline` execution and performs several validation steps:
  - Adds target steps (extractor/loader) to the pipeline.
  - Step names are hashed and configured based on their position and step name. This means that multiple steps with the same step name can be added to Pypeline execution and they will be treated as seperate instances.
  - Optionally sets up a chunker for processing large datasets.
  - Uses a progress bar (via `tqdm`) to show progress through the steps.
  - If caching is enabled, execution may resume from a cached checkpoint.
  - All DataFrames extracted using `Extractor` steps are stored inside a `Context` Object within the `Pypeline` Object.

#### Example

In this example, execution of steps will occur in this order: 
- MultiCSVExtractor
- TransposeDataFrame
- ExcelLoader.

```python
  from pypeline import Pypeline
  from pypeline.extract import MultiCSVExtractor # Gathering multiple csv files
  from pypeline.load import ExcelLoader # Load data to excel sheet
  from pypeline.transform import TransposeDataFrame # Transpose Dataframes gathered

  pypeline = Pypeline()
  pypeline.target_extractor = MultiCSVExtractor(...) # Set Target Extractor as MultiCSVExtractor
  pypeline.target_loader = ExcelLoader(...) # Set Target Loader as ExcelLoader

  transpose_step = TransposeDataFrame(...) # Create Transpose DataFrame Step

  pypeline.add_steps([transpose_step, ...]) # Add Transpose DataFrame Step
  pypeline.execute() # Execute Steps added
```

## Caching

The `Pypeline` Object enables caching in both *global* and *in execution* states. When the `cache` parameter is set to `True` a default `LFUCache` will be used. Custom Caches can be created and passed into the `cache` parameter however, they must confer with the `AbstractCache` interface. 

Please review the [Cache](cache.md) documentation for further information.

### Global Caching
Caching can be enabled globally to avoid re-running completed steps. When enabled, a **.cache** directory stores compressed snapshots of the pipeline’s state after each step, along with a **config.json** file that records hashes of each step’s source code and configuration. 

Before execution, these hashes are compared to detect any changes in code or step order. If a change is found, execution resumes from the step immediately after the last unchanged step, loading its saved state into the pipeline and skipping all prior steps. 

Global Caching stores the state's in **non-volatile** memory (.gzip files) and therefore are not destroyed upon program completion unless a reset_cache Step is included in execution.

- Custom Caches can be created using the **`AbstractCache`** interface.
- Global caching is configured using the **`store(self, step_index, parameter_index, global_context, step_key)`**, **`load(self, step_key)`** and **`reset(self, delete_directory=False)`** methods.

### In Execution Caching
In Execution Caching is a seperate but similar caching functionality. It allows state caching and loading within the execution of Pypeline Steps. This can essentially allow for 'branching' within the Pypeline execution. 

States are cached in-memory and are therefore **volatile**, meaning that all cached states are destroyed upon program completion.

- **`cache_state(self, step_name="cache_state")`**  
  - Returns a `CacheState` step that, when executed, caches the current state of the pipeline.

- **`reload_cached_state(self, cache_key, step_name="reload_cached_state")`**  
  - Returns a `ReloadCacheState` step that reloads a cached state during execution.

- **`reset_cache(self, step_name="reset_cache", delete_directory=False)`**  
  - Returns a `ResetCache` step that resets the cache. If `delete_directory` is set to `True`, it deletes the cache directory.

#### Example

In this example, execution of steps will occur in this order: 
 - CSVExtractor: stores csv_df
 - CacheState: caches csv_df
 - TransposeDataFrame: transposes csv_df, stores transposed_df
 - ReloadCacheState: reloads csv_df
 - PivotDataFrame: pivots csv_df, stores pivot_df
 - ExcelLoader: loads selected df

```python
  from pypeline import Pypeline
  from pypeline.extract import CSVExtractor
  from pypeline.load import ExcelLoader
  from pypeline.transform import TransposeDataFrame
  from pypeline.transform import PivotDataFrame

  pypeline = Pypeline()
  pypeline.target_extractor = CSVExtractor(...)
  pypeline.target_loader = ExcelLoader(...)

  transpose_step = TransposeDataFrame(...)
  pivot_step = PivotDataFrame(...)

  pypeline.add_steps([pypeline.cache_state(...), transpose_step, pypeline.reload_state(...), pivot_step]) # Add the cache_state and reload_state steps
  pypeline.execute()
```

## Chunking (Add image depicting chunking logic?)
Chunking is an essential technique which can be used to efficiently and safely process large datasets. The `Pypeline` Object enables chunking by passing A `Chunker` Class into the `chunker` parameter when using the `pypeline.execute(chunker=ChunkerClass)` method. 

Once a `Chunker` Class is passed, all Extractor steps containing the keyword argument `chunk_size` will be analyzed and chunking indexes (ie the start index and number of rows for each chunk) will be calculated using the **`calculate_chunks()`** method. Then, `Pypeline` execution will be partitioned horizontally, until all chunks are processed.

Custom chunker classes can be created and used however, they must conform to the `Chunker` interface. It is highly recommended you understand the chunking methodology a selected Chunker employs before executing the pypeline as unexpected scenarios may arise. 

Please review the [Chunk](chunker.md) documentation for further information.

### DirectChunker
- **Overview**
  - The `DirectChunker` methodology, calculates chunks purely based on the `chunk_size`. If multiple `Extractor` objects are used where one has already processed all chunks of its dataset however, another still has other chunks, the completed `Extractor` step will be passed a `(None, None)` tuple as its chunk parameter, essentially skipping the step.
  -  In a basic case, if one Dataset is used containing 12 rows of data, with a `chunk_size` of 5 then, `Pypeline` execution will occur 3 times. The first execution will contain the first 5 rows of data. The second execution will contain the next 5 rows of data. Lastly the third execution will contain the final 2 rows of data.
  -  In a multi `Extractor` case, say 2 datasets are extracted. The first dataset contains 10 rows of data with a `chunk_size` of 2 and the second dataset contains 5 rows of data with a `chunk_size` of 4. In this case, `Pypeline` execution will occur 5 times. The first execution will contain the first 2 rows of the first dataset and the first 4 rows in the second dataset. The second execution will contain the next 2 rows of the first dataset and the final row of the second dataset. The third and subsequent executions will contain the next 2 rows of the first dataset and no row of the second dataset, essentially skipping this step.
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
  
### DistributedChunker
  - The `DistributedChunker` methodology, calculates chunks by evenly distributing the number of rows based on the `chunk_size`. If multiple `Extractor` objects are used where one has already processed all chunks of its dataset however, another still has other chunks, the completed `Extractor` step calculate the downstream number of chunks and distribute the upstream chunks evenly. This ensures that all executions contain data for each extractor step, unless there are more execution chunks then number of rows in the dataset.
  -  In a basic case, if one Dataset is used containing 12 rows of data, with a `chunk_size` of 5 then, `Pypeline` execution will occur 3 times. The first execution will contain the first 5 rows of data. The second execution will contain the next 5 rows of data. Lastly the third execution will contain the final 2 rows of data.
  -  In a multi `Extractor` case, say 2 datasets are extracted. The first dataset contains 12 rows of data with a `chunk_size` of 6 and the second dataset contains 6 rows of data with a `chunk_size` of 2. In this case, `Pypeline` execution will occur 6 times. In this case, each execution will contain 2 rows of the first dataset and a single row of the second dataset.
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
  
#### Example
In this example, say there are 2 chunks execution will occur in this order:
- CSVExtractor
- TransposeDataFrame
- ExcelLoader
- CSVExtractor
- TransposeDataFrame
- ExcelLoader
  
```python
  from pypeline import Pypeline
  from pypeline.extract import CSVExtractor 
  from pypeline.load import ExcelLoader 
  from pypeline.transform import TransposeDataFrame
  from pypeline.chunker import DistributedChunker # Load DistributedChunker class

  pypeline = Pypeline()
  pypeline.target_extractor = CSVExtractor(...)
  pypeline.target_loader = ExcelLoader(...) 

  transpose_step = TransposeDataFrame(...)

  pypeline.add_steps([transpose_step, ...])
  pypeline.execute(chunker=DistributedChunker) # Initialize execution with the Distributed Chunker
```

## Context Management
Another key component to the Pypeline object is the Context dataclass. A context object dynamically stores DataFrame(s) and relevant metadata. The `Pypeline` object stores any DataFrame(s) gathered by `Extractor` Steps into a global context object. This global context stores the DataFrames between Steps during execution and any changes made to the DataFrames within a Step then updates the DataFrames inside the global context. 

Subcontext objects are passed to each Step that requests the use of a DataFrame. These subcontexts contain only the requested DataFrame. This ensures that each Step does not load all DataFrames only the ones required. It is important to understand how the Pypeline object interacts with a context primarily in the scenarios below. However, in most basic cases context objects will not need to be handled by users. 

Please review the [Context](context.md) documentation for further information.

### Case 1: Creating Custom Steps
There are multiple ways users can create custom `Step` objects, however, all of them require an understanding of how the `context` keyword is used. When a custom step function is created, the function's signature must contain the argument `context` in order to have a subcontext object passed into it via the Pypeline object. This is only if a context is to be used, if a context is not required in the `Step` function, then the `context` argument is also not required. It is recommended to set the `context` argument as the first item in the function signature, however, this is also not required.

#### Example
In this example, we create a custom Step object which can be passed into the Pypeline execution.
```python
  from pypeline import Pypeline
  from pypeline.step import Step # Import the Step class
  
  @Step(dataframes=['df1', ...], params={'a':10, ...}) # Create a Custom Step using the wrapper format
  def sample_function(context, a, b=1):
    df1 = context.get_dataframe('df1')
    print(a)
    return context, b

  pypeline = Pypeline()
  pypeline.add_step(sample_function) # We can add the Custom Step function by passing the function name as an object
```

Please review the [Step](step.md) documentation for further information.

### Case 2: Creating Custom Extractors and Loaders
Because `Extractor` and `Loader` Objects are simply subclasses of the `Step` class, custom variations can be created in a similar manner. For custom `Extractors`, an empty subcontext is given, and dataframes can be appended to this subcontext. The subcontext is then returned at the end of the function where it is parsed by the `Pypeline` Object and the global context is updated. For custom `Loaders`, any requested dataframes are inserted into a subcontext via the global context. The subcontext dataframes can then be accessed and loaded to the target destination. It is important to note that for custom `Extractors` and `Loaders`, the wrapper method of creating steps is not possible and therefore the a custom subclass of the `Step` class must be created. In addition, the step function must be configured with the name: `func(...)`.

#### Example
In this example, we create a custom Extractor object
```python
  from pypeline import Pypeline
  from pypeline.extract import Extractor # Import the Extractor class which is the interface for extractors and a subclass of the Step Class
  
  class SampleExtractor(Extractor):
    ...
    def func(context):
      df = ... # retrieve dataframe from source
      context.append_dataframe("sample_df", df)
      return context
```

#### Example
In this example, we create a custom Loader object
```python
  from pypeline import Pypeline
  from pypeline.load import Loader # Import the Loader class which is the interface for loaders and a subclass of the Step Class
  
  class SampleExtractor(Extractor):
    ...
    def func(context):
      df = context.get_dataframe("sample_df")
      df... # load dataframe to target
```

Please review the [Extractor](extract.md) and [Loader](load.md) documentation for further information.

### Case 3: Creating Custom Caches
When caching, the `Pypeline` object also caches the current state of the global context. This saves the current state of the DataFrames at a particular step and allows execution to continue from any cached state. In some cases, users may want to create a custom `Cache` using the `AbstractCache` interface, which simply caches a subcontext of the global context, storing only a subset of the DataFrames instead of all of them. This is possible by manipulating the `store(self, step_index, parameter_index, global_context, step_key)` method to remove any unwanted DataFrames before the actual store is executed.

Please review the [Cache](cache.md) documentation for further information.
