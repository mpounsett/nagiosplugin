from __future__ import unicode_literals, print_function
from .context import Context
from .resource import Resource
from .result import ResultSet
import nagiosplugin.state
import functools
import operator
import sys


class Check(object):

    def __init__(self, *objects, name=None):
        self.resources = []
        self.contexts = []
        self.context_by_metric = {}
        self.metrics = []
        self.overall_state = nagiosplugin.state.Unknown()
        self.performance_data = []
        self.results = ResultSet()
        self._dispatch_check_objects(objects)
        self.name = name or self.resources[0].__class__.__name__

    def _dispatch_check_objects(self, objects):
        for obj in objects:
            if isinstance(obj, Resource):
                self.resources.append(obj)
            elif isinstance(obj, Context):
                self.contexts.append(obj)
                self.context_by_metric.update({(m, obj) for m in obj.metrics})
            else:
                raise RuntimeError('%r has not an allowed type' % obj)

    def inspect_metrics(self):
        self.metrics = functools.reduce(operator.add, (
            res.inspect() for res in self.resources))

    def evaluate(self):
        for metric in self.metrics:
            metric.context = self.context_by_metric[metric.name]
            self.results.add(metric.evaluate())

    def run(self):
        self.inspect_metrics()
        self.evaluate()
        self.performance_data = [str(m.performance() or '')
                                 for m in self.metrics]

    def __str__(self):
        # XXX summary function
        out = ['%s %s: %s\n' % (
            self.name.upper(), str(self.results.worst_state).upper(),
            '; '.join(str(result) for result in self.results))]
        out += ['|'] + self.performance_data
        return ' '.join(out)

    @property
    def exitcode(self):
        return int(self.overall_state)

    def main(self):
        self.run()
        print(self)
        sys.exit(self.exitcode)
