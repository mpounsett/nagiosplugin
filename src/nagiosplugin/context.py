# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .performance import Performance
from .range import Range
from .result import Result, ScalarResult
from .state import Ok, Warn, Critical


class Context(object):

    def __init__(self, metrics):
        self.metrics = metrics

    def evaluate(self, metric, resource):
        return Result(Ok, metric=metric, resource=resource)

    def performance(self, metric, resource):
        return None


class ScalarContext(Context):

    def __init__(self, metrics, warning='', critical='',
                 result_cls=ScalarResult):
        super(ScalarContext, self).__init__(metrics)
        self.warning = Range(warning)
        self.critical = Range(critical)
        self.result_cls = result_cls

    def evaluate(self, metric, resource):
        if not self.critical.match(metric.value):
            return self.result_cls(Critical, self.critical, metric, resource)
        elif not self.warning.match(metric.value):
            return self.result_cls(Warn, self.warning, metric, resource)
        else:
            return self.result_cls(Ok, None, metric, resource)

    def performance(self, metric, resource):
        return Performance(metric.name, metric.value, metric.uom,
                           self.warning, self.critical,
                           metric.min, metric.max)


class Contexts:

    def __init__(self):
        self.contexts = []
        self.by_metric = {}

    def add(self, context):
        self.contexts.append(context)
        for metric_name in context.metrics:
            if metric_name in self.by_metric:
                raise RuntimeError('more than one context is in charge for',
                                   metric_name, context)
            self.by_metric[metric_name] = context

    def __getitem__(self, metric_name):
        return self.match_metric(metric_name)

    def match_metric(self, metric_name):
        return self.by_metric[metric_name]
