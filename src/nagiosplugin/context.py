from .performance import Performance
from .range import Range
from .result import Result
from .state import Ok, Warn, Critical


class Context(object):

    def __init__(self, metrics):
        self.metrics = metrics

    def evaluate(self, metric):
        return Result(metric, Ok)

    def performance(self, metric):
        return None


class ScalarContext(Context):

    def __init__(self, metrics, warning='', critical='', result_cls=Result):
        super(ScalarContext, self).__init__(metrics)
        self.warning = Range(warning)
        self.critical = Range(critical)
        self.result_cls = result_cls

    def evaluate(self, metric):
        if not self.critical.match(metric.value):
            return self.result_cls(metric, Critical, self.critical)
        elif not self.warning.match(metric.value):
            return self.result_cls(metric, Warn, self.warning)
        else:
            return self.result_cls(metric, Ok)

    def performance(self, metric):
        return Performance(metric.name, metric.value, metric.uom,
                           self.warning, self.critical,
                           metric.minimum, metric.maximum)
