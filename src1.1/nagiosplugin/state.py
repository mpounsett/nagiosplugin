import collections
import functools
import operator


class ServiceState(collections.namedtuple('ServiceState', 'code text')):

    def __str__(self):
        return self.text

    def __int__(self):
        return self.code


class Ok(ServiceState):

    def __new__(cls):
        return super(cls, Ok).__new__(cls, 0, 'ok')


class Warning(ServiceState):

    def __new__(cls):
        return super(cls, Warning).__new__(cls, 1, 'warning')


class Critical(ServiceState):

    def __new__(cls):
        return super(cls, Critical).__new__(cls, 2, 'critical')


class Unknown(ServiceState):

    def __new__(cls):
        return super(cls, Unknown).__new__(cls, 3, 'unknown')


def worst(states):
    return functools.reduce(operator.gt, states, Ok())
