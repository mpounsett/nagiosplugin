from .performance import Performance
from .range import Range
from .state import Ok, Warning, Critical


class Context(object):

    def __init__(self, metrics):
        self.metrics = metrics

    def evaluate(self, metric):
        return (Ok(),)

    def performance(self, metric):
        return None


class ScalarContext(Context):

    def __init__(self, metrics, warning='', critical=''):
        super(ScalarContext, self).__init__(metrics)
        self.warning = Range(warning)
        self.critical = Range(critical)

    def evaluate(self, metric):
        if not self.critical.match(metric.value):
            return Critical(), self.critical
        elif not self.warning.match(metric.value):
            return Warning(), self.warning
        else:
            return (Ok(),)

    def performance(self, metric):
        return Performance(metric.name, metric.value, metric.unit,
                           self.warning, self.critical,
                           metric.minimum, metric.maximum)
