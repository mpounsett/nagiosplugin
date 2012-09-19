from .context import Context


class Metric(object):

    def __init__(self, name, value, unit=None, minimum=None, maximum=None,
                 description=None):
        self.name = name
        self.value = value
        self.unit = unit
        self.minimum = minimum
        self.maximum = maximum
        self.description = description or name
        self.context = Context([])
        self.state = None
        self.annotations = []

    def __repr__(self):
        return 'Metric(%r)' % self.__dict__

    def evaluate(self):
        self.state, *self.annotations = self.context.evaluate(self)

    @property
    def performance(self):
        return self.context.performance(self)
