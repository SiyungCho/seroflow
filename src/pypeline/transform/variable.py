from .transformation import Transformation

# class DeleteVariable(Transformation):
# class RenameVariable(Transformation): # do a copy then delete

class CopyVariable(Transformation):
    def __init__(self, variable, new_variable, step_name="CopyVariable"):
        self.variable = variable
        self.new_variable = new_variable
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        return kwargs[self.variable]
    
class DivideVariable(Transformation):
    def __init__(self, variable, divide_by=1, step_name="DivideVariable"):
        self.variable = variable
        self.divide_by = divide_by
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        return kwargs[self.variable] / self.divide_by
    
class MultiplyVariable(Transformation):
    def __init__(self, variable, multiply_by=1, step_name="MultiplyVariable"):
        self.variable = variable
        self.multiply_by = multiply_by
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        return kwargs[self.variable] * self.multiply_by

class IncrementVariable(Transformation):
    def __init__(self, variable, increment_by=1, step_name="IncrementVariable"):
        self.variable = variable
        self.increment_by = increment_by
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        return kwargs[self.variable] + self.increment_by

class DecrementVariable(Transformation):
    def __init__(self, variable, decrement_by=1, step_name="DecrementVariable"):
        self.variable = variable
        self.decrement_by = decrement_by
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)
        self.update_params_list(self.variable)

    def func(self, **kwargs):
        return kwargs[self.variable] + self.decrement_by

class CreateVariable(Transformation):
    def __init__(self, variable, value, step_name="CreateVariable"):
        self.variable = variable
        self.value = value
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)

    def func(self):
        return self.value
    
class UpdateVariable(Transformation):
    def __init__(self, variable, value, step_name="UpdateVariable"):
        self.variable = variable
        self.value = value
        super().__init__(step_name=step_name, func=self.func)
        self.update_return_list(self.variable)

    def func(self):
        return self.value