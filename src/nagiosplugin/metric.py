# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import numbers


class Metric:

    def __init__(self, name, value, uom=None, min=None, max=None,
                 context=None):
        self.name = name
        self.value = value
        self.uom = uom
        self.min = min
        self.max = max
        self.context_name = context or name
        self.context = None
        self.resource = None

    def __str__(self):
        return self.valueunit

    @property
    def description(self):
        if self.context:
            return self.context.describe(self)
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
        if not self.context:
            raise RuntimeError('no context set for metric', self.name)
        return self.context.evaluate(self, self.resource)

    def performance(self):
        if not self.context:
            raise RuntimeError('no context set for metric', self.name)
        return self.context.performance(self, self.resource)
