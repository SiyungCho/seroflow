from .transformation import Transformation

# class SetVariableIfNull(Transformation):
# class CopyVariable(Transformation):
# class DivideVariable(Transformation):
# class MultiplyVariable(Transformation):
# class IncrementVariable(Transformation):
# class PrependToVariable(Transformation):
# class AppendToVariable(Transformation):
# class DeleteVariable(Transformation):
# class RenameVariable(Transformation):

class CreateVariable(Transformation):
    def __init__(self, var_name, value, step_name="CreateVariable"):
        self.var_name = var_name
        self.value = value
        super().__init__(step_name=step_name, func=self.func)
        self.return_list = [self.var_name]

    def func(self):
        return self.value
    
class UpdateVariable(Transformation):
    def __init__(self, var_name, new_value, step_name="UpdateVariable"):
        self.var_name = var_name
        self.new_value = new_value
        super().__init__(step_name=step_name, func=self.func)
        self.return_list = [self.var_name]

    def func(self):
        return self.new_value