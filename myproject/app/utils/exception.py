class UserException(Exception):
    def __init__(self, name):
        self.name = name

class NormalException(Exception):
    def __init__(self,name):
        self.name = name