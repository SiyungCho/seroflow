# Variable Transformations Documentation

This module implements transformation classes for manipulating scalar variables within a `Pipeline`. Each class extends the base `Transformation` and performs a simple arithmetic or assignment operation on a named variable. The result of each transformation is returned and can be stored back into the `Pipeline` context.

- **CopyVariable**: Copies the value of an existing variable under a new name.
- **DivideVariable**: Divides a variable’s value by a specified divisor.
- **MultiplyVariable**: Multiplies a variable’s value by a specified factor.
- **IncrementVariable**: Increments a variable’s value by a specified amount.
- **DecrementVariable**: Decrements a variable’s value by a specified amount.
- **CreateVariable**: Creates a new variable with a constant value.
- **UpdateVariable**: Updates an existing variable with a new value.

# Variable Transformation Classes

## CopyVariable

- **Purpose**: Copies the value of an existing variable under a new name.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `new_variable` (str): Name for the copied variable.
  - `step_name` (str, optional): Defaults to `"CopyVariable"`.
  - `on_error` (str, optional): Error handling strategy.

#### CopyVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import CopyVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  cp_var = CopyVariable(variable="x", new_variable="x_copy")
  pipeline.add_steps([cp_var])
  pipeline.execute()
```

---

## DivideVariable
- **Purpose**: Divides a variable’s value by a specified divisor.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `divide_by` (numeric, optional): Defaults to 1.
  - `step_name` (str, optional): Defaults to "DivideVariable".

#### DivideVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import DivideVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  div_var = DivideVariable(variable="x", divide_by=2)
  pipeline.add_steps([div_var])
  pipeline.execute()
```

---

## MultiplyVariable
- **Purpose**: Multiplies a variable’s value by a specified factor.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `multiply_by` (numeric, optional): Defaults to 1.

#### MultiplyVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import MultiplyVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  mul_var = MultiplyVariable(variable="y", multiply_by=3)
  pipeline.add_steps([mul_var])
  pipeline.execute()
```

---

## IncrementVariable
- **Purpose**: Increments a variable’s value by a specified amount.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `increment_by` (numeric, optional): Defaults to 1.

#### IncrementVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import IncrementVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  inc_var = IncrementVariable(variable="x", increment_by=10)
  pipeline.add_steps([inc_var])
  pipeline.execute()
```

---

## DecrementVariable
- **Purpose**: Decrements a variable’s value by a specified amount.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `decrement_by` (numeric, optional): Defaults to 1.

#### DecrementVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import DecrementVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  dec_var = DecrementVariable(variable="y", decrement_by=5)
  pipeline.add_steps([dec_var])
  pipeline.execute()
```

---

## CreateVariable
- **Purpose**: Creates a new variable with a constant value.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `value` (any): Value given to variable.

#### CreateVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import CreateVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  create_var = CreateVariable(variable="z", value=42)
  pipeline.add_steps([create_var])
  pipeline.execute()
```

---

## UpdateVariable
- **Purpose**: Updates an existing variable with a new value.
- **Parameters**:
  - `variable` (str): Name of the existing variable.
  - `value` (any): Value given to variable.

#### UpdateVariable Example

```python
  import pandas as pd
  from pydra import Pipeline
  from pydra.transform import UpdateVariable

  pipeline = Pipeline()
  pipeline.target_extractor = ... 

  update_var = UpdateVariable(variable="x", value=200)
  pipeline.add_steps([update_var])
  pipeline.execute()
```

---