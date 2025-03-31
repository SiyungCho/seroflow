.. _step_doc:
Step
=====================

The modules documented here define the interface and a concrete implementation for custom ``Step`` creation compatible with the ``Seroflow`` ``Pipeline`` Object.
They provide a common interface to initialize, clean up, and execute operations (steps) within a ``Seroflow`` ``Pipeline``.

Overview
-----------------------------------

This documentation covers two modules:

- **abstract_step**: Defines the ``AbstractStep`` abstract class, which specifies the interface for creating steps.

- **step**: Implements the ``Step`` class, a concrete subclass of ``AbstractStep`` that encapsulates a single operation or transformation.
The ``Step`` class manages function initialization, parameter handling, default values, error handling, and dynamic updates to return and parameter lists.
It can be used to create a custom ``Step`` via, subclass creation, the transformation subclass or wrapper definition.


AbstractStep
-------------------------------

``AbstractStep`` is an abstract base class that defines the structure of a ``Seroflow's`` ``Pipeline`` step.
This design enforces a standardized interface and behavior across different ``Step`` operations and strategies.

.. autoclass:: seroflow.step.base_step.AbstractStep
   :members:
   :show-inheritance:
   :undoc-members:

Usage Example
^^^^^^^^^^^^^^^^^

Below is an example demonstrating how a concrete step implementation might inherit from ``AbstractStep`` and implement its methods: ::

   from seroflow.step import AbstractStep

   class MyStep(AbstractStep):
      def start_step(self):
         # Initialize resources or validate input
         pass

      def stop_step(self):
         # Perform cleanup after execution
         pass

      def execute(self):
         # Implement the step's main logic
         return "Step executed"

Although the ``AbstractStep`` class can be used to create Custom ``Step`` Objects, it is not recommended due to the fact that the user will need to implement the logic for interaction between the Custom ``Step`` and the ``Pipeline`` Object. 
It is instead recommended to use the ``Step`` Class documented below.

Step
-------------------------

The ``Step`` class is a concrete implementation of ``AbstractStep`` that encapsulates the logic for executing a function with given parameters and DataFrames.
It also serves as a convenient wrapper, allowing you to easily create custom steps by simply decorating your function with ``@Step()``. 
It is highly recommended that any custom step operations users may want to develop are subclasses of the ``Step`` Class if the user wishes to implement a pre and post execution logic.
In other general cases, the wrapper technique is recommended.
However unlike the ``AbstractStep`` this is not obligatory.

Variables created inside a ``Step`` Function can be returned and will subsequently be saved as a variable internally within the ``Pipeline`` Object.
Subsequent steps that request a variable will be passed the value most recently stored.
This way interstep variable communication can be performed.
Other methods such as caching can also aid with this.

.. autoclass:: seroflow.step.step.Step
   :members:
   :show-inheritance:
   :undoc-members:

Creating Custom Steps via the ``Step`` Class
-------------------------

There are 3 main ways to create custom ``Step`` Objects to use within the ``Pipeline`` execution.
For most basic and quick step creation the wrapper method is recommended.
For more complex transformations and operations, inheriting the ``Step`` or ``Transformation`` Class is recommended.

Option 1: Wrapper Method
^^^^^^^^^^^^^^^^^

The wrapper method is the simplest way to create a custom ``Step`` object.
It allows the user to insert the ``Step`` using the ``add_step(s)(...)`` methods.
The wrapper method also allows users to call the step function as if it were a regular python function by creating the needed variables and passing them into the function to test its execution.

To create a custom ``Step`` using the wrapper method, users simply add the ``@Step()`` wrapper above a function.
This turns the function into a ``Step`` function and allows it to be passed into the ``Pipeline`` object. 

- A ``step_name`` argument can be passed as a parameter in the ``@Step(step_name="...")`` wrapper to give the step a specific name, however, this is optional and if omitted the function's name is the default name used. 
- A ``dataframes`` argument can be passed as a parameter in the ``@Step(dataframes=[...])`` wrapper to specify which DataFrames are to be passed into the step during ``Pipeline`` execution. **If omitted then all DataFrames are loaded into the step.**
- A ``params`` argument can be passed as a parameter in the ``@Step(params={"...": ...})`` wrapper to pass values to variables used in the function. In ``Pipeline`` execution, these values passed via the ``params`` parameter take precedence over any current value stored internally within the ``Pipeline`` Object. 
- Default values within the functions signature can also be used however, these have the lowest level of precedence.
- In ``Pipeline`` execution the priority hierarchy for a variables value goes as such:
  
  1. Values stored via a ``Step``'s params parameter.
  2. Values stored internally within the ``Pipeline`` Object
  3. Default values defined by the function's signature

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to create a custom ``Step`` using the wrapper method: ::

  from seroflow import Pipeline
  from seroflow.step import Step # Import the Step class
  
  @Step(dataframes=['df1', ...], params={'a':10, ...}) # Create a Custom Step using the wrapper format
  def sample_function(context, a, b=1):
    df1 = context.get_dataframe('df1')
    print(a)
    return context, b

  pipeline = Pipeline()
  pipeline.add_step(sample_function) # We can add the Custom Step function by passing the function name as an object

  sample_function(...) # Wrapper based function can also be called as a normal python function


Option 2: Inherit the ``Step`` Class
^^^^^^^^^^^^^^^^^

Inherit the ``Step`` Class method is a slightly more involved way to create a custom ``Step`` object. 
It allows the user to insert the ``Step`` using the ``add_step(s)(...)`` methods. 
However, unlike the wrapper method does not intuitively allow users to call the step function as if it were a regular python function. 

Inheriting the ``Step`` Class does however, allow users to define a more complex methodology for how the custom step is to be executed.
Namely the methods: ``start_step(...)`` and ``stop_step(...)`` allow users to define logic which occurs directly before and after the execution of the step function.
This allows for pre and post validation, type checking and more.

Parameter definition is the same as the wrapper method, however, a ``step_name`` must be defined as the name ``func`` will cause errors in ``Pipeline`` execution.

Usage Example
^^^^^^^^^^^^^^^^^

Below is a simple example that shows how to create a custom ``Step`` by inheriting the ``Step`` class: ::

  from seroflow import Pipeline
  from seroflow.step import Step # Import the Step class
  
  class CustomStep(Step):
    def __init__(self, dataframes, params, step_name="sample_function", on_error="raise", ...):
      super().__init__(step_name=step_name, dataframes=dataframes, params=params, func=self.func, on_error=on_error)
    
    def func(context, a, b=1):
      df1 = context.get_dataframe('df1')
      print(a)
      return context, b

    def start_step(...):
      ...

    def stop_step(...):
      ...

  custom_step = CustomStep(...)

  pipeline = Pipeline()
  pipeline.add_step(custom_step) # We can add the Custom Step function by passing the object

Option 3: Inherit the ``Transformation`` Class
^^^^^^^^^^^^^^^^^

Please review the :ref:`transformation_doc` documentation for further information.