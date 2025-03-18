"""
Module: aggregation.py

This module implements a suite of transformation classes that compute various statistical metrics on
columns of a DataFrame. Each transformation class extends the base Transformation class and is designed
to operate on a specified DataFrame stored in the Pypeline context. The available transformations include:

    - GetColMean: Computes the mean of a specified column.
    - GetColMedian: Computes the median of a specified column.
    - GetColMode: Computes the mode of a specified column.
    - GetColStd: Computes the standard deviation of a specified column.
    - GetColSum: Computes the sum of a specified column.
    - GetColVariance: Computes the variance of a specified column.
    - GetColQuantile: Computes a given quantile of a specified column.
    - GetColCorrelation: Computes the correlation between two specified columns.
    - GetColCovariance: Computes the covariance between two specified columns.
    - GetColSkew: Computes the skewness of a specified column.

Each class is initialized with the name of the column(s) to be processed, the DataFrame name, an optional
variable name for storing the result (defaulting to a suffix based on the column name), and an error handling
strategy. The transformation is executed by calling its func() method, which retrieves the DataFrame from
the context and computes the desired statistic.
"""

from .transformation import Transformation

class GetColMean(Transformation):
    """
    GetColMean Class

    Computes the mean of a specified column in a DataFrame and returns the result.
    The resulting mean can be stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the mean.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed mean.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColMean",
                 on_error=None):
        """
        Initializes the GetColMean transformation.

        Arguments:
            column (str): The name of the column to compute the mean.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the mean result. Defaults to "<column>_mean".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColMean".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_mean"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColMean transformation.

        Retrieves the DataFrame from the context and computes the mean of the specified column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            float: The computed mean of the column.
        """
        df = context.dataframes[self.dataframe_name]
        mean = self.__get_column_mean(df, self.column)
        return mean

    def __get_column_mean(self, df, column):
        """
        Computes the mean of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the mean is computed.

        Returns:
            float: The mean value of the column.
        """
        return df[column].mean()

class GetColMedian(Transformation):
    """
    GetColMedian Class

    Computes the median of a specified column in a DataFrame and returns the result.
    The resulting median is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the median.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed median.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColMedian",
                 on_error=None):
        """
        Initializes the GetColMedian transformation.

        Arguments:
            column (str): The name of the column to compute the median.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the median result. Defaults to "<column>_median".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColMedian".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_median"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColMedian transformation.

        Retrieves the DataFrame from the context and computes the median of the specified column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            float: The computed median of the column.
        """
        df = context.dataframes[self.dataframe_name]
        median = self.__get_column_median(df, self.column)
        return median

    def __get_column_median(self, df, column):
        """
        Computes the median of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the median is computed.

        Returns:
            float: The median value of the column.
        """
        return df[column].median()

class GetColMode(Transformation):
    """
    GetColMode Class

    Computes the mode of a specified column in a DataFrame and returns the result.
    The resulting mode is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the mode.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed mode.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColMode",
                 on_error=None):
        """
        Initializes the GetColMode transformation.

        Arguments:
            column (str): The name of the column to compute the mode.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the mode result. Defaults to "<column>_mode".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColMode".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_mode"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColMode transformation.

        Retrieves the DataFrame from the context and computes the mode of the specified column.
        If multiple modes exist, the first mode is returned.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The mode value of the specified column.
        """
        df = context.dataframes[self.dataframe_name]
        mode = self.__get_column_mode(df, self.column)
        return mode

    def __get_column_mode(self, df, column):
        """
        Computes the mode of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the mode is computed.

        Returns:
            The mode value of the column (first mode if multiple exist).
        """
        return df[column].mode()[0]

class GetColStd(Transformation):
    """
    GetColStd Class

    Computes the standard deviation of a specified column in a DataFrame and returns the result.
    The resulting standard deviation is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the standard deviation.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed standard deviation.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColStd",
                 on_error=None):
        """
        Initializes the GetColStd transformation.

        Arguments:
            column (str): The name of the column to compute the standard deviation.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the standard deviation result.
                                      Defaults to "<column>_std".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColStd".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_std"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColStd transformation.

        Retrieves the DataFrame from the context and computes the standard deviation of the specified column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            float: The standard deviation of the specified column.
        """
        df = context.dataframes[self.dataframe_name]
        std = self.__get_column_std(df, self.column)
        return std

    def __get_column_std(self, df, column):
        """
        Computes the standard deviation of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the standard deviation is computed.

        Returns:
            float: The standard deviation of the column.
        """
        return df[column].std()

class GetColSum(Transformation):
    """
    GetColSum Class

    Computes the sum of a specified column in a DataFrame and returns the result.
    The resulting sum is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the sum.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed sum.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColSum",
                 on_error=None):
        """
        Initializes the GetColSum transformation.

        Arguments:
            column (str): The name of the column to compute the sum.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the sum result.
                                      Defaults to "<column>_sum".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColSum".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_sum"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColSum transformation.

        Retrieves the DataFrame from the context and computes the sum of the specified column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The sum of the specified column.
        """
        df = context.dataframes[self.dataframe_name]
        sum_value = self.__get_column_sum(df, self.column)
        return sum_value

    def __get_column_sum(self, df, column):
        """
        Computes the sum of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the sum is computed.

        Returns:
            The sum of the column.
        """
        return df[column].sum()

class GetColVariance(Transformation):
    """
    GetColVariance Class

    Computes the variance of a specified column in a DataFrame and returns the result.
    The computed variance is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the variance.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed variance.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColVariance",
                 on_error=None):
        """
        Initializes the GetColVariance transformation.

        Arguments:
            column (str): The name of the column to compute the variance.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the variance result.
                                      Defaults to "<column>_variance".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColVariance".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_variance"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColVariance transformation.

        Retrieves the DataFrame from the context and computes the variance of the specified column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The variance of the specified column.
        """
        df = context.dataframes[self.dataframe_name]
        variance = self.__get_column_variance(df, self.column)
        return variance

    def __get_column_variance(self, df, column):
        """
        Computes the variance of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the variance is computed.

        Returns:
            The variance of the column.
        """
        return df[column].var()

class GetColQuantile(Transformation):
    """
    GetColQuantile Class

    Computes a specified quantile of a column in a DataFrame and returns the result.
    The computed quantile is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column for which the quantile is computed.
        quantile (float): The quantile to compute (e.g., 0.5 for the median).
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed quantile.
    """
    def __init__(self,
                 column,
                 dataframe,
                 quantile,
                 variable=None,
                 step_name="GetColQuantile",
                 on_error=None):
        """
        Initializes the GetColQuantile transformation.

        Arguments:
            column (str): The name of the column for which the quantile will be computed.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            quantile (float): The quantile value to compute.
            variable (str, optional): The variable name to store the quantile result.
                                      Defaults to "<column>_quantile_<quantile>".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColQuantile".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.quantile = quantile
        self.variable = variable if variable else column + "_quantile_" + str(quantile)
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColQuantile transformation.

        Retrieves the DataFrame from the context and computes the specified quantile of the given column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The computed quantile of the specified column.
        """
        df = context.dataframes[self.dataframe_name]
        quantile_value = self.__get_column_quantile(df, self.column, self.quantile)
        return quantile_value

    def __get_column_quantile(self, df, column, quantile):
        """
        Computes the specified quantile of the given column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which the quantile is computed.
            quantile (float): The quantile to compute.

        Returns:
            The computed quantile value.
        """
        return df[column].quantile(quantile)

class GetColCorrelation(Transformation):
    """
    GetColCorrelation Class

    Computes the correlation between two specified columns in a DataFrame and returns the result.
    The computed correlation is stored in the pypeline context under a designated variable name.

    Attributes:
        column1 (str): Name of the first column.
        column2 (str): Name of the second column.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed correlation.
    """
    def __init__(self,
                 column1,
                 column2,
                 dataframe,
                 variable=None,
                 step_name="GetColCorrelation",
                 on_error=None):
        """
        Initializes the GetColCorrelation transformation.

        Arguments:
            column1 (str): The name of the first column.
            column2 (str): The name of the second column.
            dataframe (str): The name of the DataFrame containing the columns.
            variable (str, optional): The variable name to store the correlation result.
                                      Defaults to "<column1>_<column2>_correlation".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColCorrelation".
            on_error (str, optional): The error handling strategy.
        """
        self.column1 = column1
        self.column2 = column2
        self.variable = variable if variable else column1 + "_" + column2 + "_correlation"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColCorrelation transformation.

        Retrieves the DataFrame from the context and computes the correlation between the two specified columns.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The correlation value between the two columns.
        """
        df = context.dataframes[self.dataframe_name]
        correlation = self.__get_column_correlation(df, self.column1, self.column2)
        return correlation

    def __get_column_correlation(self, df, column1, column2):
        """
        Computes the correlation between two specified columns.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column1 (str): The first column.
            column2 (str): The second column.

        Returns:
            The correlation value between the two columns.
        """
        return df[column1].corr(df[column2])

class GetColCovariance(Transformation):
    """
    GetColCovariance Class

    Computes the covariance between two specified columns in a DataFrame and returns the result.
    The computed covariance is stored in the pypeline context under a designated variable name.

    Attributes:
        column1 (str): Name of the first column.
        column2 (str): Name of the second column.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed covariance.
    """
    def __init__(self,
                 column1,
                 column2,
                 dataframe,
                 variable=None,
                 step_name="GetColCovariance",
                 on_error=None):
        """
        Initializes the GetColCovariance transformation.

        Arguments:
            column1 (str): The name of the first column.
            column2 (str): The name of the second column.
            dataframe (str): The name of the DataFrame containing the columns.
            variable (str, optional): The variable name to store the covariance result.
                                      Defaults to "<column1>_<column2>_covariance".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColCovariance".
            on_error (str, optional): The error handling strategy.
        """
        self.column1 = column1
        self.column2 = column2
        self.variable = variable if variable else column1 + "_" + column2 + "_covariance"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColCovariance transformation.

        Retrieves the DataFrame from the context and computes the covariance between the two specified columns.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The covariance value between the two columns.
        """
        df = context.dataframes[self.dataframe_name]
        covariance = self.__get_column_covariance(df, self.column1, self.column2)
        return covariance

    def __get_column_covariance(self, df, column1, column2):
        """
        Computes the covariance between two specified columns.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column1 (str): The first column.
            column2 (str): The second column.

        Returns:
            The covariance value between the two columns.
        """
        return df[column1].cov(df[column2])

class GetColSkew(Transformation):
    """
    GetColSkew Class

    Computes the skewness of a specified column in a DataFrame and returns the result.
    The computed skewness is stored in the pypeline context under a designated variable name.

    Attributes:
        column (str): Name of the column to compute the skewness.
        dataframe_name (str): Name of the DataFrame in the context.
        variable (str): Variable name for storing the computed skewness.
    """
    def __init__(self,
                 column,
                 dataframe,
                 variable=None,
                 step_name="GetColSkew",
                 on_error=None):
        """
        Initializes the GetColSkew transformation.

        Arguments:
            column (str): The name of the column for which skewness will be computed.
            dataframe (str): The name of the DataFrame from which the column is extracted.
            variable (str, optional): The variable name to store the skewness result.
                                      Defaults to "<column>_skew".
            step_name (str, optional): The name of this transformation step. Defaults to "GetColSkew".
            on_error (str, optional): The error handling strategy.
        """
        self.column = column
        self.variable = variable if variable else column + "_skew"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name,
                         func=self.func,
                         dataframes=dataframe,
                         on_error=on_error)
        self.override_return_list(self.variable)

    def func(self, context):
        """
        Executes the GetColSkew transformation.

        Retrieves the DataFrame from the context and computes the skewness of the specified column.

        Arguments:
            context (Context): The context object containing the DataFrame.

        Returns:
            The skewness value of the specified column.
        """
        df = context.dataframes[self.dataframe_name]
        skew = self.__get_column_skew(df, self.column)
        return skew

    def __get_column_skew(self, df, column):
        """
        Computes the skewness of the specified column.

        Arguments:
            df (DataFrame): The DataFrame containing the data.
            column (str): The column for which skewness is computed.

        Returns:
            The skewness value of the column.
        """
        return df[column].skew()
