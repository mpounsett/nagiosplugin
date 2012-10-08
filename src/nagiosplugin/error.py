from .result import Result
from .state import Warn, Unknown


class InternalError(Result):

    def __init__(self, reason):
        self.state = Unknown
        self.reason = reason


class InternalWarning(Result):

    def __init__(self, reason):
        self.state = Warn
        self.reason = reason
