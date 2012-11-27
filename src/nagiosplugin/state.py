# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Classes (with singletons) to represent check outcomes."""

import collections
import functools


def worst(states):
    return functools.reduce(lambda a, b: a if a > b else b, states, Ok)


class ServiceState(collections.namedtuple('ServiceState', 'code text')):
    """Abstract base class for all states.

    Each state has two constant attributes: :attr:`text` is the short text
    representation which is printed for example at the beginning of the summary
    line. :attr:`code` is the corresponding exit code.
    """

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
