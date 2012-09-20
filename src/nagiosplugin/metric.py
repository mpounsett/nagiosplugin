from .context import Context
import numbers


class Metric(object):

    def __init__(self, name, value, uom=None, minimum=None, maximum=None,
                 description=None):
        self.name = name
        self.value = value
        self.uom = uom
        self.minimum = minimum
        self.maximum = maximum
        self.description = description or name
        self.context = Context([])
        self.state = None
        self.failure_criterion = None

    def __repr__(self):
        return 'Metric(%r)' % self.__dict__

    def __str__(self):
        return '%s%s' % (format_numeric(self.value), self.uom or '')

    def evaluate(self):
        return self.context.evaluate(self)

    def performance(self):
        return self.context.performance(self)


def format_numeric(value):
    """Special-case real numbers output."""
    if isinstance(value, numbers.Real):
        return '%.4g' % value
    return str(value)
