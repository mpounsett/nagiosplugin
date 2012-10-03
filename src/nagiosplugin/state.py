import collections
import functools
import operator


def worst(states):
    return functools.reduce(operator.gt, states, Ok)


class ServiceState(collections.namedtuple('ServiceState', 'code text')):

    def __str__(self):
        return self.text

    def __int__(self):
        return self.code


class Ok(ServiceState):

    def __new__(cls):
        return super(cls, Ok).__new__(cls, 0, 'ok')

Ok = Ok()


class Warn(ServiceState):

    def __new__(cls):
        return super(cls, Warn).__new__(cls, 1, 'warning')

Warn = Warn()


class Critical(ServiceState):

    def __new__(cls):
        return super(cls, Critical).__new__(cls, 2, 'critical')

Critical = Critical()


class Unknown(ServiceState):

    def __new__(cls):
        return super(cls, Unknown).__new__(cls, 3, 'unknown')

Unknown = Unknown()
