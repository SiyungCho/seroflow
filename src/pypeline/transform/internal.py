from .transformation import Transformation

class AddDataFrame(Transformation):
    """
    Adds a new dataframe to the context.
    """
    def __init__(self, dataframe, name, step_name="AddDataFrame", on_error=None):
        self.dataframe = dataframe
        self.name = name
        super().__init__(step_name=step_name, func=self.func, on_error=on_error)

    def func(self, context):
        context.add_dataframe(self.name, self.dataframe)
        return context

class DeleteDataFrame(Transformation):
    """
    Deletes a dataframe from the context.
    """
    def __init__(self, dataframe, step_name="DeleteDataFrame", on_error=None):
        self.dataframe = dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=dataframe, on_error=on_error)

    def func(self, context):
        del context.dataframes[self.dataframe]
        return context

class RenameDataFrame(Transformation):
    """
    Renames a dataframe within the context.
    """
    def __init__(self, old_name, new_name, step_name="RenameDataFrame", on_error=None):
        self.old_name = old_name
        self.new_name = new_name
        super().__init__(step_name=step_name, func=self.func, dataframes=old_name, on_error=on_error)

    def func(self, context):
        if self.old_name in context.dataframes:
            df = context.dataframes.pop(self.old_name)
            context.set_dataframe(self.new_name, df)
        return context

class CopyDataFrame(Transformation):
    """
    Creates a copy of an existing dataframe under a new name.
    """
    def __init__(self, source_dataframe, target_dataframe, step_name="CopyDataFrame", on_error=None):
        self.source_dataframe = source_dataframe
        self.target_dataframe = target_dataframe
        super().__init__(step_name=step_name, func=self.func, dataframes=source_dataframe, on_error=on_error)

    def func(self, context):
        df = context.dataframes[self.source_dataframe].copy()
        context.set_dataframe(self.target_dataframe, df)
        return context
