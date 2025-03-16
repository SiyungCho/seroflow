from .transformation import Transformation

#Need to configure to work with logger
#Need to have save_to_variable property

class DisplayInfo(Transformation):
    def __init__(self, dataframes, step_name="DisplayInfo"):
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            print(f"------------ Info for DataFrame '{dataframe_name}' ------------")
            print(f"Shape: {df.shape}")
            print("Columns and Data Types:")
            print(df.dtypes)
            print("-" * 50)

class DisplayColumns(Transformation):
    def __init__(self, dataframes, step_name="DisplayColumns"):
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            print(f"------------ DataFrame '{dataframe_name}' Columns: ------------")
            print(list(df.columns))
            print("-" * 50)

class DisplayHead(Transformation):
    def __init__(self, dataframes, n=5, step_name="DisplayHead"):
        self.n = n
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            print(f"------------ DataFrame '{dataframe_name}' Head (first {self.n} rows): ------------")
            print(df.head(self.n))
            print("-" * 50)

class DisplayTail(Transformation):
    def __init__(self, dataframes, n=5, step_name="DisplayTail"):
        self.n = n
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)

    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            print(f"------------ DataFrame '{dataframe_name}' Tail (last {self.n} rows): ------------")
            print(df.tail(self.n))
            print("-" * 50)

class DisplayColumnMean(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnMean"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                mean_value = df[col_name].mean()
                print(f"------------ [{dataframe_name}] Mean of column '{col_name}': {mean_value} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnMedian(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnMedian"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                median_value = df[col_name].median()
                print(f"------------ [{dataframe_name}] Median of column '{col_name}': {median_value} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnMode(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnMode"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                mode_series = df[col_name].mode()
                # Convert mode values to a list for clear printing.
                print(f"------------ [{dataframe_name}] Mode of column '{col_name}': {list(mode_series)} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnVariance(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnVariance"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col_name = self.__resolve_column(df)
            if col_name is None or col_name not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                variance_value = df[col_name].var()
                print(f"------------ [{dataframe_name}] Variance of column '{col_name}': {variance_value} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnStdDev(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnStdDev"):
        """
        Args:
            dataframes (dict): Dictionary of DataFrames.
            column (str or int): Column name or index.
        """
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                std_dev = df[col].std()
                print(f"------------ [{dataframe_name}] Standard Deviation of column '{col}': {std_dev} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnSum(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnSum"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                col_sum = df[col].sum()
                print(f"------------ [{dataframe_name}] Sum of column '{col}': {col_sum} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnMin(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnMin"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                col_min = df[col].min()
                print(f"------------ [{dataframe_name}] Minimum of column '{col}': {col_min} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnMax(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnMax"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                col_max = df[col].max()
                print(f"------------ [{dataframe_name}] Maximum of column '{col}': {col_max} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnCount(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnCount"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{df_name}] Column '{self.column}' not found. ------------")
            else:
                count_val = df[col].count()
                print(f"------------ [{df_name}] Count (non-null) for column '{col}': {count_val} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnUnique(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnUnique"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{df_name}] Column '{self.column}' not found. ------------")
            else:
                unique_vals = df[col].unique()
                print(f"------------ [{df_name}] Unique values in column '{col}': {list(unique_vals)} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnNUnique(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnNUnique"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{df_name}] Column '{self.column}' not found. ------------")
            else:
                n_unique = df[col].nunique()
                print(f"------------ [{df_name}] Number of unique values in column '{col}': {n_unique} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayColumnDType(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayColumnDType"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for df_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{df_name}] Column '{self.column}' not found. ------------")
            else:
                dtype_val = df[col].dtype
                print(f"------------ [{df_name}] Data type for column '{col}': {dtype_val} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayStringCount(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayStringItemCount"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                counts = df[col].value_counts()
                print(f"------------ [{dataframe_name}] Value counts for column '{col}': ------------")
                print(counts)

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayMostFrequentString(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayMostFrequentString"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                mode_series = df[col].mode()
                if mode_series.empty:
                    print(f"------------ [{dataframe_name}] No mode found for column '{col}'. ------------")
                else:
                    print(f"------------ [{dataframe_name}] Most frequent item(s) in column '{col}': {list(mode_series)} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplayAllCategories(Transformation):
    def __init__(self, dataframes, column, step_name="DisplayAllCategories"):
        self.column = column
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
        
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                categories = df[col].unique()
                print(f"------------ [{dataframe_name}] Unique categories in column '{col}': {list(categories)} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column
    
class DisplaySubstringOccurrence(Transformation):
    def __init__(self, dataframes, column, substring, step_name="DisplaySubstringOccurrence"):
        self.column = column
        self.substring = substring
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframes)
    
    def func(self, context):
        for dataframe_name, df in context.dataframes.items():
            col = self.__resolve_column(df)
            if col is None or col not in df.columns:
                print(f"------------ [{dataframe_name}] Column '{self.column}' not found. ------------")
            else:
                # Convert entries to strings and count occurrences of the substring per row.
                total_count = df[col].astype(str).apply(lambda x: x.count(self.substring)).sum()
                print(f"------------ [{dataframe_name}] Total occurrences of '{self.substring}' in column '{col}': {total_count} ------------")

    def __resolve_column(self, df):
        if isinstance(self.column, int):
            return df.columns[self.column] if self.column < len(df.columns) else None
        return self.column