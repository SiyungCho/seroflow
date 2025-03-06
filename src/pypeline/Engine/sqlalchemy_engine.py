import sqlalchemy

class sqlalchemy_engine():
    def __init__(self):
        self.engine = None
        self.connection = None
        self.metadata = None
        self.session = None
        self.transaction = None