# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Performace data (perfdata) representation and associated functions. """

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
    """Performance(label, value[, uom[, warn[, crit[, min[, max]]]]])

    Performance data record created from a metric in a context
    (usually a :class:`nagiosplugin.context.ScalarContext`).

    :param label: short identifier (20 chars max), results in graph titles for
        example
    :param value: measured value (usually an int, float, or bool)
    :param uom: unit of measure -- use base units whereever possible
    :param warn: warning range
    :param crit: critical range
    :param min: known value minimum (None for no minimum)
    :param max: known value maximum (None for no maximum)
    """

    def __new__(cls, label, value, uom='', warn='', crit='', min='', max=''):
        if len(label) > 20:
            raise RuntimeError('label is too long (20 chars max)', label)
        if "'" in label:
            raise RuntimeError('label contains illegal character "\'"',
                               label)
        return super(cls, Performance).__new__(
            cls, label, value, zap_none(uom), zap_none(warn), zap_none(crit),
            zap_none(min), zap_none(max))

    def __str__(self):
        """String representation conforming to the plugin API."""
        out = ['%s=%s%s' % (quote(self.label), self.value, self.uom),
               str(self.warn), str(self.crit), str(self.min), str(self.max)]
        out = reversed(list(
            itertools.dropwhile(lambda x: x == '', reversed(out))))
        return ';'.join(out)
