# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import numbers
import collections


class Metric(collections.namedtuple('Metric', 'name value uom min max fmt')):

    def __new__(cls, name, value, uom=None, min=None, max=None,
                fmt='{name} is {valueunit}'):
        return super(cls, Metric).__new__(cls, name, value, uom, min, max, fmt)

    def __str__(self):
        return self.valueunit

    @property
    def description(self):
        return self.fmt.format(
            name=self.name, value=self.value, uom=self.uom,
            valueunit=self.valueunit, min=self.min, max=self.max)

    @property
    def valueunit(self):
        return '%s%s' % (format_numeric(self.value), self.uom or '')


def format_numeric(value):
    """Special-case real numbers output."""
    if isinstance(value, numbers.Real):
        return '%.4g' % value
    return str(value)
