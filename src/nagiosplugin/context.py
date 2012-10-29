# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .performance import Performance
from .range import Range
from .result import Result, ScalarResult
from .state import Ok, Warn, Critical


class Context:

    def __init__(self, name, fmt_metric=None, result_cls=Result):
        self.name = name
        self.fmt_metric = fmt_metric or '{name} is {valueunit}'
        self.result_cls = result_cls

    def evaluate(self, metric, resource):
        return self.result_cls(Ok, metric=metric)

    def performance(self, metric, resource):
        return None

    def describe(self, metric):
        try:
            return self.fmt_metric(metric, self)
        except TypeError:
            return self.fmt_metric.format(
                name=metric.name, value=metric.value, uom=metric.uom,
                valueunit=metric.valueunit, min=metric.min, max=metric.max)


class ScalarContext(Context):

    def __init__(self, name, warning, critical, fmt_metric=None,
                 result_cls=ScalarResult):
        super(ScalarContext, self).__init__(name, fmt_metric, result_cls)
        self.warning = Range(warning)
        self.critical = Range(critical)

    def evaluate(self, metric, resource):
        if not self.critical.match(metric.value):
            return self.result_cls(Critical, self.critical, metric)
        elif not self.warning.match(metric.value):
            return self.result_cls(Warn, self.warning, metric)
        else:
            return self.result_cls(Ok, None, metric)

    def performance(self, metric, resource):
        return Performance(metric.name, metric.value, metric.uom,
                           self.warning, self.critical,
                           metric.min, metric.max)


class Contexts:

    def __init__(self):
        self.by_name = dict(
            default=ScalarContext('default', '', ''),
            null=Context('null'))

    def add(self, context):
        self.by_name[context.name] = context

    def __getitem__(self, context_name):
        try:
            return self.by_name[context_name]
        except KeyError:
            raise KeyError('cannot find context', context_name,
                           'known contexts: {}'.format(
                               ', '.join(self.by_name.keys())))

    def __contains__(self, context_name):
        return context_name in self.by_name

    def __iter__(self):
        return iter(self.by_name)
