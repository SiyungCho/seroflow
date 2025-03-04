class base_exception(Exception):
    def __init__(self, message):
        self.message = message