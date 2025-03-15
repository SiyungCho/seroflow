from .transformation import Transformation

class GetColMean(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColMean"):
        self.column = column
        self.variable = variable if variable else column + "_mean"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)

    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        mean = self.__get_column_mean(df, self.column)
        return mean
    
    def __get_column_mean(self, df, column):
        return df[column].mean()
    
class GetColMedian(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColMedian"):
        self.column = column
        self.variable = variable if variable else column + "_median"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        median = self.__get_column_median(df, self.column)
        return median
    
    def __get_column_median(self, df, column):
        return df[column].median()
    
class GetColMode(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColMode"):
        self.column = column
        self.variable = variable if variable else column + "_mode"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        mode = self.__get_column_mode(df, self.column)
        return mode
    
    def __get_column_mode(self, df, column):
        return df[column].mode()[0]
    
class GetColStd(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColStd"):
        self.column = column
        self.variable = variable if variable else column + "_std"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        std = self.__get_column_std(df, self.column)
        return std
    
    def __get_column_std(self, df, column):
        return df[column].std()
    
class GetColSum(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColSum"):
        self.column = column
        self.variable = variable if variable else column + "_sum"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        sum = self.__get_column_sum(df, self.column)
        return sum
    
    def __get_column_sum(self, df, column):
        return df[column].sum()
    
class GetColVariance(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColVariance"):
        self.column = column
        self.variable = variable if variable else column + "_variance"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        variance = self.__get_column_variance(df, self.column)
        return variance
    
    def __get_column_variance(self, df, column):
        return df[column].var()
    
class GetColQuantile(Transformation):
    def __init__(self, column, dataframe, quantile, variable=None, step_name="GetColQuantile"):
        self.column = column
        self.quantile = quantile
        self.variable = variable if variable else column + "_quantile_" + str(quantile)
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        quantile = self.__get_column_quantile(df, self.column, self.quantile)
        return quantile
    
    def __get_column_quantile(self, df, column, quantile):
        return df[column].quantile(quantile)
    
class GetColCorrelation(Transformation):
    def __init__(self, column1, column2, dataframe, variable=None, step_name="GetColCorrelation"):
        self.column1 = column1
        self.column2 = column2
        self.variable = variable if variable else column1 + "_" + column2 + "_correlation"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        correlation = self.__get_column_correlation(df, self.column1, self.column2)
        return correlation
    
    def __get_column_correlation(self, df, column1, column2):
        return df[column1].corr(df[column2])
    
class GetColCovariance(Transformation):
    def __init__(self, column1, column2, dataframe, variable=None, step_name="GetColCovariance"):
        self.column1 = column1
        self.column2 = column2
        self.variable = variable if variable else column1 + "_" + column2 + "_covariance"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        covariance = self.__get_column_covariance(df, self.column1, self.column2)
        return covariance
    
    def __get_column_covariance(self, df, column1, column2):
        return df[column1].cov(df[column2])
    
class GetColSkew(Transformation):
    def __init__(self, column, dataframe, variable=None, step_name="GetColSkew"):
        self.column = column
        self.variable = variable if variable else column + "_skew"
        self.dataframe_name = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe)
        self.override_return_list(self.variable)
    
    def func(self, context):
        df = context.dataframes[self.dataframe_name]
        skew = self.__get_column_skew(df, self.column)
        return skew
    
    def __get_column_skew(self, df, column):
        return df[column].skew()
    
