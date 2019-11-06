# -*- coding: utf-8 -*-
"""Classes  to represent check outcomes.

This module defines :class:`ServiceState` which is the abstract base
class for check outcomes. class for check outcomes. class for check
outcomes. The four states defined by the :term:`Nagios plugin API` are
represented as singleton subclasses.

Note that the *warning* state is defined by the :class:`Warn` class. The
class has not been named `Warning` to avoid being confused with the
built-in Python exception of the same name.
"""

import collections
import functools


def worst(states):
    """Reduce list of *states* to the most significant state."""
    return functools.reduce(lambda a, b: a if a > b else b, states, Ok)


class ServiceState(collections.namedtuple('ServiceState', 'code text')):
    """Abstract base class for all states.

    Each state has two constant attributes: :attr:`text` is the short
    text representation which is printed for example at the beginning of
    the summary line. :attr:`code` is the corresponding exit code.
    """

    def __str__(self):
        """Plugin-API compliant text representation."""
        return self.text

    def __int__(self):
        """Plugin API compliant exit code."""
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
