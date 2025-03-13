from .transformation import Transformation

class AddDataFrame(Transformation):
    """
    Adds a new dataframe to the context.
    """
    def __init__(self, dataframe_name, dataframe, step_name="AddDataFrame"):
        self.dataframe_name = dataframe_name
        self.dataframe = dataframe
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        context.set_dataframe(self.dataframe_name, self.dataframe)
        return context

class DeleteDataFrame(Transformation):
    """
    Deletes a dataframe from the context.
    """
    def __init__(self, dataframe_name, step_name="DeleteDataFrame"):
        self.dataframe_name = dataframe_name
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        if self.dataframe_name in context.dataframes:
            del context.dataframes[self.dataframe_name]
        return context

class RenameDataFrame(Transformation):
    """
    Renames a dataframe within the context.
    """
    def __init__(self, old_name, new_name, step_name="RenameDataFrame"):
        self.old_name = old_name
        self.new_name = new_name
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        if self.old_name in context.dataframes:
            df = context.dataframes.pop(self.old_name)
            context.set_dataframe(self.new_name, df)
        return context

class CopyDataFrame(Transformation):
    """
    Creates a copy of an existing dataframe under a new name.
    """
    def __init__(self, source_dataframe_name, target_dataframe_name, step_name="CopyDataFrame"):
        self.source_dataframe_name = source_dataframe_name
        self.target_dataframe_name = target_dataframe_name
        super().__init__(step_name=step_name, func=self.func)

    def func(self, context):
        df = context.dataframes[self.source_dataframe_name].copy()
        context.set_dataframe(self.target_dataframe_name, df)
        return context
