# Variable Transformations Documentation

This module implements transformation classes for manipulating scalar variables within a Pypeline. Each class extends the base `Transformation` and performs a simple arithmetic or assignment operation on a named variable. The result of each transformation is returned and can be stored back into the Pypeline context.

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
  from pypeline import Pypeline
  from pypeline.transform import CopyVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  cp_var = CopyVariable(variable="x", new_variable="x_copy")
  pypeline.add_steps([cp_var])
  pypeline.execute()
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
  from pypeline import Pypeline
  from pypeline.transform import DivideVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  div_var = DivideVariable(variable="x", divide_by=2)
  pypeline.add_steps([div_var])
  pypeline.execute()
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
  from pypeline import Pypeline
  from pypeline.transform import MultiplyVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  mul_var = MultiplyVariable(variable="y", multiply_by=3)
  pypeline.add_steps([mul_var])
  pypeline.execute()
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
  from pypeline import Pypeline
  from pypeline.transform import IncrementVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  inc_var = IncrementVariable(variable="x", increment_by=10)
  pypeline.add_steps([inc_var])
  pypeline.execute()
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
  from pypeline import Pypeline
  from pypeline.transform import DecrementVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  dec_var = DecrementVariable(variable="y", decrement_by=5)
  pypeline.add_steps([dec_var])
  pypeline.execute()
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
  from pypeline import Pypeline
  from pypeline.transform import CreateVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  create_var = CreateVariable(variable="z", value=42)
  pypeline.add_steps([create_var])
  pypeline.execute()
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
  from pypeline import Pypeline
  from pypeline.transform import UpdateVariable

  pypeline = Pypeline()
  pypeline.target_extractor = ... 

  update_var = UpdateVariable(variable="x", value=200)
  pypeline.add_steps([update_var])
  pypeline.execute()
```

---