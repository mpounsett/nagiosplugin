# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Structured representation for data points."""

import numbers
import collections


class Metric(collections.namedtuple(
        'Metric', 'name value uom min max context contextobj resource')):
    """Single measured value.

    The value should be expressed in terms of base units, so
    Metric('swap', 10240, 'B') is better than Metric('swap', 10, 'kiB').

    :param name: short internal identifier for the value -- appears also
        in the performance data
    :param value: data point, usually has a boolen or numeric type,
        but other types are also possible
    :param uom: :term:`unit of measure`, preferrably as ISO abbreviation like
        "s"
    :param min: minimum value or None if there is no known minimum
    :param max: maximum value or None if there is no known maximum
    :param context: name of the associated context
    :param contextobj: reference to the associated context object (set
        automatically by :class:`Check`)
    :param resource: reference to the originating :class:`Resource` (set
        automatically by :class:`Check`)
    """

    def __new__(cls, name, value, uom=None, min=None, max=None, context=None,
                contextobj=None, resource=None):
        return tuple. __new__(cls, (
            name, value, uom, min, max, context or name, contextobj, resource))

    def __str__(self):
        """:attr:`valueunit` string representation."""
        return self.valueunit

    def replace(self, **attr):
        """Creates new instance with updated attributes."""
        return self._replace(**attr)

    @property
    def description(self):
        """Human-readable, detailed string representation.

        Delegates to the context to format the value. Returns compact
        :attr:`valueunit` representation if no context has been
        associated yet.
        """
        if self.contextobj:
            return self.contextobj.describe(self)
        return str(self)

    @property
    def valueunit(self):
        """Compact string representation.

        This is just the value and the unit. If the value is a real
        number, express the value with a limited number of digits to
        improve readability.
        """
        return '%s%s' % (self._human_readable_value, self.uom or '')

    @property
    def _human_readable_value(self):
        """Limit number of digits for floats."""
        if isinstance(self.value, numbers.Real):
            return '%.4g' % self.value
        return str(self.value)

    def evaluate(self):
        """Evaluates this instance according to the context.

        :return: :class:`Result` object
        :raise RuntimeError: if no context has been associated yet
        """
        if not self.contextobj:
            raise RuntimeError('no context set for metric', self.name)
        return self.contextobj.evaluate(self, self.resource)

    def performance(self):
        """Generates performance data according to the context.

        :return: :class:`Performance` object
        :raise RuntimeError: if no context has been associated yet
        """
        if not self.contextobj:
            raise RuntimeError('no context set for metric', self.name)
        return self.contextobj.performance(self, self.resource)
