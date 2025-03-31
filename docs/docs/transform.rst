.. _transformation_doc:

Transformations
==========================

The module documented here defines the base structure for creating a ``Transformation`` Step.
``Transformation`` Steps are simply subclasses of the ``Step`` class. 
However, it provide a common interface to creating operations that typically modify or analyze DataFrames and update the ``Pipeline`` context accordingly.
Subclasses simply need to implement the abstract method ``func()`` to define their specific transformation logic.

All predefined transformations, including those related to aggregations, column or string manipulations, variable management are derived from the ``Transformation`` class.

Overview
-----------------------------------

This documentation covers:

- **Transformation**: Defines the ``Transformation`` abstract class, which specifies the interface for creating transformations.

.. _transformation:
Transformation
---------------------------

The ``Transformation`` class serves as an abstract base class (inheriting from ``ABC``) designed to support transformation operations. 
It establishes a uniform interface that all transformation classes must follow, ensuring consistency in how custom transformation logic is integrated and executed.

Key Features
^^^^^^^^^^^^^^^^^

**Abstract Method Enforcement**:

   - Derived classes must implement the abstract method ``func()``, which is responsible for encapsulating the core transformation logic.
   - This requirement guarantees that every transformation provides a concrete operation that can be executed within the ``Pipeline`` Object.

**Pre- and Post-Execution Hooks**:

   - The methods ``start_step(...)`` and ``stop_step(...)`` are available to allow developers to insert custom logic immediately before and after the main transformation operation. 
   - This feature is useful for tasks such as resource initialization, logging, or cleanup, providing more control over the execution flow of the transformation.

**Flexible Parameter and Return Value Configuration**:

   - Unlike the more rigid ``Step`` class, ``Transformation`` allows you to adjust both the input parameters and the expected return values of the function:

      - ``self.update_params_list(...)``: This method lets you specify which variables should always be passed into the transformation function, ensuring that necessary context or configuration parameters are consistently available.
      - ``self.update_return_list(...)``: This method allows you to define the set of variables that the transformation function will return, ensuring that the output is well-defined and reliable.

**Initialization Similarities with Step Class**:

   - Although the initialization process for ``Transformation`` classes is similar to that of the ``Step`` class, the enhanced flexibility in managing input and output parameters distinguishes it, making it ideal for more complex transformation workflows.

.. autoclass:: seroflow.transform.transformation.Transformation
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to the ``Transformation`` class: ::

   from seroflow import Pipeline
   from seroflow.transform import Transformation  # Import the Transformation class

   class Add10toVariableAndDataFrameTransformation(Transformation):
      def __init__(self, dataframes, variable, step_name="Add10toVariableAndDataFrameTransformation", on_error="raise", **kwargs):
         # Store the variable to be modified
         self.variable = variable
         # Initialize the base Transformation class with required parameters and the custom function
         super().__init__(step_name=step_name, dataframes=dataframes, func=self.func, on_error=on_error)
         # Define the expected input parameters and return values for the transformation step
         self.update_params_list(self.variable)
         self.update_return_list(self.variable)
      
      def func(self, context, **kwargs):
         # Retrieve the DataFrame from the context using the designated key
         df = context.dataframes[self.dataframe]
         # Perform an in-place transformation: add 10 to the first column of the DataFrame
         df[0] += 10
         # Update the context with the modified DataFrame
         context.set_dataframe(self.dataframe, df)
         # Modify the provided variable by adding 10
         kwargs[self.variable] += 10
         # Return the updated context
         return context

      def start_step(self, *args, **kwargs):
         # Custom logic to execute before the transformation function runs
         pass

      def stop_step(self, *args, **kwargs):
         # Custom logic to execute after the transformation function completes
         pass

   # Create an instance of the custom transformation
   custom_transformation = Add10toVariableAndDataFrameTransformation(...)

   # Initialize the Pipeline and add the custom transformation step
   pipeline = Pipeline()
   pipeline.add_step(custom_transformation)  # The custom Transformation is now part of the pipeline

.. _agg_transformation:
Aggregation Transformations
-------------------------------------

.. automodule:: seroflow.transform.aggregation
   :members:
   :show-inheritance:
   :undoc-members:

.. _cache_transformation:
Cache Transformations
-------------------------------

.. automodule:: seroflow.transform.cache
   :members:
   :show-inheritance:
   :undoc-members:

.. _col_transformation:
Column Transformations
--------------------------------

.. automodule:: seroflow.transform.column
   :members:
   :show-inheritance:
   :undoc-members:

.. _dataframe_transformation:
Dataframe Transformations
-----------------------------------

.. automodule:: seroflow.transform.dataframe
   :members:
   :show-inheritance:
   :undoc-members:

.. _date_transformation:
Date Transformations
------------------------------

.. automodule:: seroflow.transform.date
   :members:
   :show-inheritance:
   :undoc-members:

.. _display_transformation:
Display Transformations
---------------------------------

.. automodule:: seroflow.transform.display
   :members:
   :show-inheritance:
   :undoc-members:

.. _index_transformation:
Index Transformations
-------------------------------

.. automodule:: seroflow.transform.index
   :members:
   :show-inheritance:
   :undoc-members:

.. _internal_transformation:
Internal Transformations
----------------------------------

.. automodule:: seroflow.transform.internal
   :members:
   :show-inheritance:
   :undoc-members:

.. _sql_transformation:
SQL Transformations
-----------------------------

.. automodule:: seroflow.transform.sql
   :members:
   :show-inheritance:
   :undoc-members:

.. _string_transformation:
String Transformations
--------------------------------

.. automodule:: seroflow.transform.string
   :members:
   :show-inheritance:
   :undoc-members:

.. _var_transformation:
Variable Transformations
----------------------------------

.. automodule:: seroflow.transform.variable
   :members:
   :show-inheritance:
   :undoc-members:
