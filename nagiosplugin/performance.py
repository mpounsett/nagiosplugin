# -*- coding: utf-8 -*-
"""Performance data (perfdata) representation.

:term:`Performance data` are created during metric evaluation in a
context and are written into the *perfdata* section of the plugin's
output. :class:`Performance` allows to create value objects that are
passed between other nagiosplugin objects.

For sake of consistency, performance data should represent their values
in their respective base unit, so `Performance('size', 10000, 'B')` is
better than `Performance('size', 10, 'kB')`.
"""

import collections
import itertools
import re


def zap_none(val):
    if val is None:
        return ''
    return val


def quote(label):
    if re.match(r'^\w+$', label):
        return label
    return "'%s'" % label


class Performance(collections.namedtuple('Performance', [
        'label', 'value', 'uom', 'warn', 'crit', 'min', 'max'])):

    def __new__(cls, label, value, uom='', warn='', crit='', min='', max=''):
        """Create new performance data object.

        :param label: short identifier, results in graph
            titles for example (20 chars or less recommended)
        :param value: measured value (usually an int, float, or bool)
        :param uom: unit of measure -- use base units whereever possible
        :param warn: warning range
        :param crit: critical range
        :param min: known value minimum (None for no minimum)
        :param max: known value maximum (None for no maximum)
        """
        if "'" in label or "=" in label:
            raise RuntimeError('label contains illegal characters', label)
        return super(cls, Performance).__new__(
            cls, label, value, zap_none(uom), zap_none(warn), zap_none(crit),
            zap_none(min), zap_none(max))

    def __str__(self):
        """String representation conforming to the plugin API.

        Labels containing spaces or special characters will be quoted.
        """
        out = ['%s=%s%s' % (quote(self.label), self.value, self.uom),
               str(self.warn), str(self.crit), str(self.min), str(self.max)]
        out = reversed(list(
            itertools.dropwhile(lambda x: x == '', reversed(out))))
        return ';'.join(out)
