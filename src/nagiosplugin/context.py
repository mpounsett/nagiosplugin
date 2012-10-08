from .performance import Performance
from .range import Range
from .result import Result, ScalarResult
from .state import Ok, Warn, Critical


class Context(object):

    def __init__(self, metrics):
        self.metrics = metrics

    def evaluate(self, metric):
        return Result(metric, Ok)

    def performance(self, metric):
        return None


class ScalarContext(Context):

    def __init__(self, metrics, warning='', critical='',
                 result_cls=ScalarResult):
        super(ScalarContext, self).__init__(metrics)
        self.warning = Range(warning)
        self.critical = Range(critical)
        self.result_cls = result_cls

    def evaluate(self, metric):
        if not self.critical.match(metric.value):
            return self.result_cls(Critical, self.critical, metric)
        elif not self.warning.match(metric.value):
            return self.result_cls(Warn, self.warning, metric)
        else:
            return self.result_cls(Ok, None, metric)

    def performance(self, metric):
        return Performance(metric.name, metric.value, metric.uom,
                           self.warning, self.critical,
                           metric.minimum, metric.maximum)
