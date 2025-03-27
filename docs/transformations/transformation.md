# Transformation Documentation

The module documented here defines the base structure for creating a Transformation Step. Transformation Steps are simply subclasses of the Step class. However, it provide a common interface to creating operations that typically modify or analyze DataFrames and update the `Pipeline` context accordingly. Subclasses simply need to implement the abstract method `func()` to define their specific transformation logic.

All predefined transformations, including those related to aggregations, column or string manipulations, variable management are derived from the Transformation class.

## Overview

This documentation covers:

- **Transformation**:  
  Defines the `Transformation` abstract class, which specifies the interface for creating transformations. Subclasses must implement the abstract method:
  - `func(self, context)`

## Class: Transformation

The `Transformation` class serves as an abstract base class (inheriting from `ABC`) designed to support transformation operations within the `Pipeline` framework. It establishes a uniform interface that all transformation classes must follow, ensuring consistency in how custom transformation logic is integrated and executed.

**Key Features**:
- **Abstract Method Enforcement**:
  - Derived classes must implement the abstract method `func()`, which is responsible for encapsulating the core transformation logic. This requirement guarantees that every transformation provides a concrete operation that can be executed within the `Pipeline`.
- **Pre- and Post-Execution Hooks**:
  - The methods `start_step(...)` and `stop_step(...)` are available to allow developers to insert custom logic immediately before and after the main transformation operation. 
  - This feature is useful for tasks such as resource initialization, logging, or cleanup, providing more control over the execution flow of the transformation.
- **Flexible Parameter and Return Value Configuration**:
  - Unlike the more rigid `Step` class, `Transformation` allows you to adjust both the input parameters and the expected return values of the function:
    - `self.update_params_list(...)`: This method lets you specify which variables should always be passed into the transformation function, ensuring that necessary context or configuration parameters are consistently available.
    - `self.update_return_list(...)`: This method allows you to define the set of variables that the transformation function will return, ensuring that the output is well-defined and reliable.
- **Initialization Similarities with Step Class**:
  - Although the initialization process for `Transformation` classes is similar to that of the `Step` class, the enhanced flexibility in managing input and output parameters distinguishes it, making it ideal for more complex transformation workflows.

#### Example

Below is a simple example that shows how to create a custom `Step` by inheriting the `Step` class:

```python
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
```

## List of Predefined Transformations:

### [Aggregation Transformations](aggregate.md)
- **GetColMean**: Computes the mean of a specified column.
- **GetColMedian**: Computes the median of a specified column.
- **GetColMode**: Computes the mode of a specified column.
- **GetColStd**: Computes the standard deviation of a specified column.
- **GetColSum**: Computes the sum of a specified column.
- **GetColVariance**: Computes the variance of a specified column.
- **GetColQuantile**: Computes a given quantile of a specified column.
- **GetColCorrelation**: Computes the correlation between two specified columns.
- **GetColCovariance**: Computes the covariance between two specified columns.
- **GetColSkew**: Computes the skewness of a specified column.

### [Column Transformations](column.md)
- **ConvertColumnType**: Converts a specified column of a DataFrame to a new data type.
- **RenameColumns**: Renames one or more columns based on a provided mapping.
- **DropColumn**: Drops a single specified column from a DataFrame.
- **DropColumns**: Drops multiple specified columns from a DataFrame.
- **AddColumn**: Adds a new column to a DataFrame computed from a function.
- **MergeColumns**: Merges multiple columns into a single column by concatenating their string representations.
- **SplitColumn**: Splits a single column into multiple new columns based on a delimiter.
- **ExplodeColumn**: Explodes a column containing list-like elements into multiple rows.
- **CreateColumnFromVariable**: Creates a new column in a DataFrame using a constant value provided via a variable.

### [DataFrame Transformations](dataframe.md) 
- **TransposeDataFrame**: Transposes the DataFrame.
- **PivotDataFrame**: Creates a pivot table from a DataFrame.
- **MeltDataFrame**: Unpivots a DataFrame from wide to long format.
- **GroupByAggregate**: Groups a DataFrame by specified columns and aggregates using provided functions.
- **FilterRows**: Filters rows based on a boolean function.
- **SortDataFrame**: Sorts a DataFrame by one or more columns.
- **DropDuplicates**: Removes duplicate rows from a DataFrame.
- **SelectColumns**: Selects a subset of columns from a DataFrame.
- **FillNAValues**: Fills missing (NA) values with a specified fill value.
- **ReplaceValues**: Replaces specified values in a DataFrame with a new value.
- **MergeDataFrames**: Merges two DataFrames based on specified keys and merge strategy.
- **JoinDataFrames**: Joins two DataFrames using the pandas join method.
- **ApplyFunction**: Applies a function to an entire DataFrame or a specified column.
- **ApplyMap**: Applies a function element-wise to a DataFrame.
- **MapValues**: Maps values in a specified column based on a provided dictionary.
- **OneHotEncode**: Performs one-hot encoding on a categorical column.

### [Date Transformations](date.md) 
- **ConvertToDateTime**: Converts a specified column to pandas datetime format, with optional format parsing.

### [Display Transformations](display.md) 
- **DisplayInfo**: Prints basic information (shape, columns, and data types) for each DataFrame.
- **DisplayColumns**: Prints the list of column names for each DataFrame.
- **DisplayHead**: Prints the first N rows of each DataFrame.
- **DisplayTail**: Prints the last N rows of each DataFrame.
- **DisplayColumnMean**: Displays the mean of a specified column for each DataFrame.
- **DisplayColumnMedian**: Displays the median of a specified column for each DataFrame.
- **DisplayColumnMode**: Displays the mode(s) of a specified column for each DataFrame.
- **DisplayColumnVariance**: Displays the variance of a specified column for each DataFrame.
- **DisplayColumnStdDev**: Displays the standard deviation of a specified column for each DataFrame.
- **DisplayColumnSum**: Displays the sum of a specified column for each DataFrame.
- **DisplayColumnMin**: Displays the minimum value of a specified column for each DataFrame.
- **DisplayColumnMax**: Displays the maximum value of a specified column for each DataFrame.
- **DisplayColumnCount**: Displays the count of non-null values in a specified column for each DataFrame.
- **DisplayColumnUnique**: Displays the unique values in a specified column for each DataFrame.
- **DisplayColumnNUnique**: Displays the number of unique values in a specified column for each DataFrame.
- **DisplayColumnDType**: Displays the data type of a specified column for each DataFrame.
- **DisplayStringCount**: Displays the value counts for a specified column in each DataFrame.
- **DisplayMostFrequentString**: Displays the most frequent item(s) in a specified column for each DataFrame.
- **DisplayAllCategories**: Displays all unique categories in a specified column for each DataFrame.
- **DisplaySubstringOccurrence**: Counts and displays the total occurrences of a substring in a specified column for each DataFrame.

### [Index Transformations](index.md) 
- **SetIndex**: Sets a specified column as the DataFrame’s index.
- **ResetIndex**: Resets the DataFrame’s index, with an option to drop the existing index.

### [Internal Transformations](internal.md) 
- **AddDataFrame**: Adds a new DataFrame to the context.
- **DeleteDataFrame**: Deletes a DataFrame from the context.
- **RenameDataFrame**: Renames an existing DataFrame in the context.
- **CopyDataFrame**: Creates a copy of an existing DataFrame under a new name.

### [SQL Transformations](sql.md) 
- **SQLQuery**: Executes a SQL query against one or more DataFrames in the context and stores the result under a specified key.

### [String Transformations](string.md) 
- **RemoveCharacterFromColumn**: Removes all occurrences of a specified character from a string column.
- **RemoveCharactersFromColumn**: Removes all occurrences of a list of characters from a string column.
- **ReplaceStringInColumn**: Replaces occurrences of a specified substring with another string in a column.

### [Variable Transformations](variable.md) 
- **CopyVariable**: Copies the value of an existing variable under a new name.
- **DivideVariable**: Divides a variable’s value by a specified divisor.
- **MultiplyVariable**: Multiplies a variable’s value by a specified factor.
- **IncrementVariable**: Increments a variable’s value by a specified amount.
- **DecrementVariable**: Decrements a variable’s value by a specified amount.
- **CreateVariable**: Creates a new variable with a constant value.
- **UpdateVariable**: Updates an existing variable with a new value.