import pyodbc

class pyodbc_engine():
    def __init__(self):
        self.connection = None
        self.cursor = None