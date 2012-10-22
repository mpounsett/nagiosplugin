# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import numbers
import collections


class Metric(collections.namedtuple(
        'Metric', 'name value uom min max context contextobj resource')):

    def __new__(cls, name, value, uom=None, min=None, max=None, context=None,
                contextobj=None, resource=None):
        return tuple. __new__(cls, (
            name, value, uom, min, max, context or name, contextobj, resource))

    def __str__(self):
        return self.valueunit

    def replace(self, **kw):
        return self._replace(**kw)

    @property
    def description(self):
        if self.contextobj:
            return self.contextobj.describe(self)
        return str(self)

    @property
    def valueunit(self):
        return '%s%s' % (self.human_readable_value, self.uom or '')

    @property
    def human_readable_value(self):
        """Limit number of digits for floats."""
        if isinstance(self.value, numbers.Real):
            return '%.4g' % self.value
        return str(self.value)

    def evaluate(self):
        if not self.contextobj:
            raise RuntimeError('no context set for metric', self.name)
        return self.contextobj.evaluate(self, self.resource)

    def performance(self):
        if not self.contextobj:
            raise RuntimeError('no context set for metric', self.name)
        return self.contextobj.performance(self, self.resource)
