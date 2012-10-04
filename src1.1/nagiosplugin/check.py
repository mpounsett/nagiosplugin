from __future__ import unicode_literals, print_function
from .context import Context
from .resource import Resource
from .text import Text
import collections
import nagiosplugin.state
import functools
import operator
import sys


class Check(object):

    def __init__(self, name, *objects):
        self.name = name
        self.resources = []
        self.texts = []
        self.text_by_metric = {}
        self.contexts = []
        self.context_by_metric = {}
        self.metrics = []
        self.metric_by_importance = collections.defaultdict(list)
        self.overall_state = nagiosplugin.state.Unknown()
        self.performance_data = []
        self._dispatch_check_objects(objects)

    def _dispatch_check_objects(self, objects):
        for obj in objects:
            if isinstance(obj, Resource):
                self.resources.append(obj)
            elif isinstance(obj, Context):
                self.contexts.append(obj)
                self.context_by_metric.update({(m, obj) for m in obj.metrics})
            elif isinstance(obj, Text):
                self.texts.append(obj)
                self.text_by_metric.update({(m, obj) for m in obj.metrics})
            else:
                raise RuntimeError('%r has not an allowed type' % obj)

    def inspect_metrics(self):
        self.metrics = functools.reduce(operator.add, (
            res.inspect() for res in self.resources))

    def evaluate(self):
        for metric in self.metrics:
            metric.context = self.context_by_metric[metric.name]
            metric.evaluate()
            self.metric_by_importance[metric.state].append(metric)

    def run(self):
        self.inspect_metrics()
        self.evaluate()
        self.overall_state = max(self.metric_by_importance.keys())
        self.performance_data = [str(m.performance) for m in self.metrics
                                 if m.performance is not None]

    def describe_failures(self):
        out = []
        for state, metrics in self.metric_by_importance.items():
            if state == nagiosplugin.state.Ok():
                continue
            for m in metrics:
                if m.name in self.text_by_metric:
                    text = self.text_by_metric[m.name].describe_failure(m)
                    if text:
                        out.append('%s: %s\n' % (state, text))
        return out

    def __str__(self):
        out = ['%s %s:\n' % (self.name.upper(), str(self.overall_state).upper())]
        out += self.describe_failures()
        out += ['|'] + self.performance_data
        return ' '.join(out)

    @property
    def exitcode(self):
        return int(self.overall_state)

    def main(self):
        self.run()
        print(self)
        sys.exit(self.exitcode)
