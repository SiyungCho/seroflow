# pypeline Module Documentation

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

### Overview

The `Pypeline` class provides a framework for constructing and executing ETL pipelines with built-in support for:

- **State Caching:** Save and resume execution from specific checkpoints.
- **Logging:** Record execution events and errors.
- **Chunked Execution:** Partition execution for handling large datasets.
- **Type and Value Validation:** Ensure that steps, parameters, and contexts are correctly defined.

### Attributes

- **`logger`** (`logging.Logger` or `None`):  
  Logger instance used for tracking pypeline execution details.

- **`mode`** (`str`):  
  The current execution mode (`"DEV"`, `"TEST"`, or `"PROD"`). In `"DEV"` mode, for example, loader steps may be skipped.

- **`cache`** (`AbstractCache` or `None`):  
  Caching mechanism for storing intermediate pypeline states.

- **`parameter_index`** (`dict`):  
  Dictionary for storing parameters and variables shared across steps.

- **`step_index`** (`OrderedDict`):  
  Ordered dictionary mapping unique step keys to their corresponding step objects.

- **`step_name_index`** (`OrderedDict`):  
  Ordered dictionary mapping unique step keys to step names.

- **`dataframe_index`** (`dict`):  
  Dictionary mapping step keys to requested dataframe names.

- **`globalcontext`** (`Context`):  
  Global context object that holds all dataframes used throughout the pipeline.

- **`chunker`** (`Chunker` or `None`):  
  Optional chunker object to partition and manage segmented execution.

### Methods

#### Initialization and Basic Methods

- **`__init__(self, cache=False, logger=False, mode="DEV")`**  
  Initializes a new `Pypeline` instance with optional caching, logging, and mode settings.
  
  **Parameters:**
  
  - `cache`: Either `False`, `True` (to instantiate a default `LFUCache`), or a user-defined cache (subclass of `AbstractCache`).
  - `logger`: Either `False`, `True` (to instantiate a default `CustomLogger`), or a user-defined `logging.Logger` object.
  - `mode`: A string defining the mode of operation. Valid values are `"DEV"`, `"TEST"`, or `"PROD"`.

- **`__str__(self)`**  
  Custom print method that displays the internal state including parameter, step, and dataframe indexes.

- **`__del__(self)`**  
  Destructor for cleanup upon deletion of the pypeline object.

- **`__display_message(self, message, _print=False)`**  
  Logs and optionally prints a formatted message. If a logger is set, it logs the message; if `_print` is `True`, it also prints it.

#### Property Getters and Setters

The class defines several properties with associated getters and setters that enforce type validation and proper initialization. These include:

- **`logger`**  
  - *Getter:* Retrieves the current logger.
  - *Setter:* Validates that the logger is either a boolean value or an instance of `logging.Logger`.

- **`target_extractor`** and **`target_loader`**  
  - Ensure that the target extractor and loader are of valid types before setting.

- **`cache`**  
  - *Getter/Setter:* Manages the caching mechanism with validation to accept either a boolean or an instance of a subclass of `AbstractCache`.

- **`parameter_index`**, **`step_index`**, **`step_name_index`**, **`dataframe_index`**  
  - *Getters:* Provide access to internal mappings for parameters, steps, and dataframes.

- **`globalcontext`**  
  - *Getter/Setter:* Manages the global context object. The setter validates that the context is valid.

- **`chunker`**  
  - *Getter/Setter:* Manages an optional chunker object used for partitioning execution.

- **`mode`**  
  - *Getter/Setter:* Ensures the execution mode is a valid string (`"DEV"`, `"TEST"`, or `"PROD"`).

#### Execution and Step Management

- **`execute(self, chunker=None)`**  
  Begins the ETL pipeline execution. It performs several validation steps:
  
  - Adds target steps (extractor/loader) to the pipeline.
  - Optionally sets up a chunker for processing large datasets.
  - Uses a progress bar (via `tqdm`) to show progress through the steps.
  - If caching is enabled, execution may resume from a cached checkpoint.
  
- **`add_step(self, step)`** and **`add_steps(self, steps)`**  
  Methods for adding one or multiple step objects to the pipeline. When a multiextractor step is added, each internal extractor is added as an individual step.

- **`cache_state(self, step_name="cache_state")`**  
  Returns a `CacheState` step that, when executed, caches the current state of the pipeline.

- **`reload_cached_state(self, cache_key, step_name="reload_cached_state")`**  
  Returns a `ReloadCacheState` step that reloads a cached state during execution.

- **`reset_cache(self, step_name="reset_cache", delete_directory=False)`**  
  Returns a `ResetCache` step that resets the cache. If `delete_directory` is set to `True`, it deletes the cache directory.

#### Internal Helper Methods

A number of internal methods (prefixed with `__`) support the pypeline functionality, including:

- **Step Parsing and Indexing:**  
  Methods like `__parse_step`, `__update_step_index`, and `__update_step_name_index` handle the creation of unique step keys and mapping steps to their identifiers.

- **Parameter and Context Management:**  
  Methods such as `__parse_parameters`, `__update_parameter_index`, and `__update_globalcontext` ensure that parameters and context dataframes are correctly passed between steps.

- **Cache Management:**  
  Methods like `__load_from_cache` and `__store_in_cache` handle saving and resuming execution states when caching is enabled.

- **Chunking and Execution:**  
  The method `__perform_step` executes an individual step, incorporating logic to skip loader steps in `"DEV"` mode and to update the cache after successful execution.

## Usage Example

Below is a simple example that shows how to initialize a `Pypeline`, add a step, and execute the pipeline:

```python
from pypeline import Pypeline

# Initialize a pypeline with caching and logging enabled in development mode.
pypeline = Pypeline(cache=True, logger=True, mode="DEV")

# Add a processing step (assuming `my_step` is a valid step function).
pypeline.add_step(my_step)

# Execute the pipeline.
pypeline.execute()