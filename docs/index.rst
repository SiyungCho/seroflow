.. Seroflow documentation master file

Getting Started with Seroflow!
===================================

Welcome to **Seroflow**!
This guide will walk you through the basics of key components, configuring, and using the package to build and execute efficient data pipelines.

Introduction
-----------------------------------
**Seroflow** is a powerful Python package that allows users to easily build and execute data pipelines.
It simplifies pipeline creation by breaking each phase—extraction, transformation, and loading—into concrete step objects.

Basics
-----------------------------------
**Seroflow** uses 5 main components to build and execute data pipelines.
In the next section, we will discuss each of these components at a high level and then review how a collection of these components can be used to execute the ``Pipeline``.

Key Components
^^^^^^^^^^^^^^^^^
**Pipelines**: 
   The ``Pipeline`` Object is the main container and executor of the data pipeline.
   It sequentially analyses and stores any added Steps, then when ready executes these steps, storing and validating the outputs.
   The ``Pipeline`` object receives and stores ``pandas`` dataframes and can also store intermediate single variables to be used throughout execution.
   If we think of a freight train analogy, the ``Pipeline`` object is the engine and conductor, whilst our step object are the containers being stored onboard.
   The ``Pipeline`` object can also log, chunk and cache during execution making it extremely robust and easy to monitor.

**Steps**: 
   ``Step`` Objects are the main building blocks of a data pipeline.
   They perform the individual operations that will be performed and ensure the operations are performed correctly.
   They also configure and analyze the resources needed so that the ``Pipeline`` object can easily distribute any needed variables or dataframes.
   The ``Step`` Class is an interface used to create custom operations and as you will see essentially all components derive from this class.

**Extractors**: 
   ``Extractor`` Objects are the 'Extract' operations in a data pipeline and are a subclass of the ``Step`` Class.
   They are the data gatherers and connect, read and conform to data sources in order to move data from source into a ``pandas`` dataframe.
   ``Extractor`` Objects then send this extracted dataframe to the ``Pipeline`` Object to be used in future steps.
   ``Target Extractors``, are a special type of ``Extractor``.
   They are essential, and when configured are always the first ``Step`` executed by the ``Pipeline``.
   ``Target Extractors`` are mandatory in *Production modes*, as they ensure there is always data inside the ``Pipeline``. 

**Loaders**: 
   ``Loader`` Objects are the 'Load' operations in a data pipeline and are a subclass of the ``Step`` Class.
   They are the data senders and connect, read and conform to a target location in order to move data from a ``pandas`` dataframe to the destination.
   ``Loader`` Objects then receive transformed dataframes from the ``Pipeline`` Object. ``Target Loaders``, are a special type of ``Loader``.
   They are essential, and when configured are always the last ``Step`` executed by the ``Pipeline``.
   ``Target Loaders`` are not mandatory in *any modes*, however, they are recommended to ensure the transformed data is always released.

**Transformations**: 
   ``Transformation`` Objects are the intermediate Steps that perform singular data operations on specified dataframes and are a subclass of the ``Step`` Class.
   These operations can range in complexity however the ``Seroflow`` package offers over 70+ predefined transformations to be used.
   Users simply select, configure and add a ``Transformation`` Object to the ``Pipeline`` object and the operation will be performed on the selected dataframes.

Basic Execution
^^^^^^^^^^^^^^^^^
After adding all necessary Steps and components, in order to execute the ``Pipeline`` Object, we simply run the ``.execute()`` method on the ``Pipeline`` Object.
This sequentially performs all the added steps and runs the entire data pipeline.

Usage Example
^^^^^^^^^^^^^^^^^
In the example below, we will create a simple data ``Pipeline`` by extracting data from a csv file, performing a transpose operation on the data then releasing the transformed data to an excel file.::

   from seroflow.seroflow import Pipeline
   from seroflow.extract import CSVExtractor
   from seroflow.load import ExcelLoader
   from seroflow.transform import TransposeDataFrame

   pipeline = Pipeline()

   csv_extractor = CSVExtractor(source='.../datafolder/testdata.csv', index_col=False, header=None)
   excel_loader = ExcelLoader(target='.../datafolder/export/', dataframe='testdata', index=False, header=False)
   transpose_dataframe = TransposeDataFrame(dataframe='testdata')

   pipeline.target_extractor = csv_extractor
   pipeline.target_loader = excel_loader
   pipeline.add_steps([transpose_dataframe])
   pipeline.execute()

Easily Create Custom Steps
-----------------------------------
Say there is a custom ``Step`` operation, a user may need that is not predefined by the ``Seroflow`` package.
One of the main features of ``Seroflow`` is the ability to easily create and integrate custom ``Steps`` to be executed by the ``Pipeline`` Object.
One of the simplest methods to create a custom ``Step`` is to use the ``Step`` Class as a function wrapper.
All we need to do, is create a python function which performs an operation on a dataframe and then wrap that function in the ``@Step()`` decorator.

Usage Example
^^^^^^^^^^^^^^^^^
In the example below, we will build off our previous data pipeline, but this time creates and adds a custom step which prints the first 5 rows of a dataframe using the ``@Step()`` decorator.::

   from seroflow.seroflow import Pipeline
   from seroflow.extract import CSVExtractor
   from seroflow.load import ExcelLoader
   from seroflow.transform import TransposeDataFrame
   from seroflow.step import Step

   @Step(dataframes='testdata')
   def print_first_5_dataframe_rows(context):
      dataframe = context.get_dataframe('testdata')
      print(dataframe.head(5))
      return context

   pipeline = Pipeline()

   csv_extractor = CSVExtractor(source='.../datafolder/testdata.csv', index_col=False, header=None)
   excel_loader = ExcelLoader(target='.../datafolder/export/', dataframe='testdata', index=False, header=False)
   transpose_dataframe = TransposeDataFrame(dataframe='testdata')

   pipeline.target_extractor = csv_extractor
   pipeline.target_loader = excel_loader
   pipeline.add_steps([transpose_dataframe, print_first_5_dataframe_rows])
   pipeline.execute()

Please refer to the [Pipeline](pipeline.md) documentation to learn more about creating custom Steps.

Advanced Features
-----------------------------------
``Seroflow`` supports several other advanced features to enhance your data pipelines such as:

* **Logging**: Automatically logs pipeline execution details.
* **Caching**: Supports caching intermediate data for improved performance.
* **Chunking**: Processes data in manageable chunks.

Refer to the [Documentation](../README.md#documentation) for detailed usage and configuration options.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   Getting Started with Seroflow <self>
   docs/seroflow
   docs/cache
   docs/chunker
   docs/context
   docs/engine
   docs/extract
   docs/load
   docs/log
   docs/step
   docs/transform
   docs/types
   docs/utils
   docs/wrappers
