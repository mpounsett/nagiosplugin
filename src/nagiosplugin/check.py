from .context import Context, Contexts
from .error import CheckError
from .resource import Resource
from .result import Result, Results
from .runtime import Runtime
from .state import Ok, Unknown
from .summary import Summary
import logging


class Check(object):

    def __init__(self, *objects):
        self.resources = []
        self.contexts = Contexts()
        self.summary = Summary()
        self.results = Results()
        self.perfdata = []
        self.name = ''
        self.add(*objects)

    def add(self, *objects):
        for obj in objects:
            if isinstance(obj, Resource):
                self.resources.append(obj)
                if not self.name:
                    self.name = self.resources[0].name
            elif isinstance(obj, Context):
                self.contexts.add(obj)
            elif isinstance(obj, Summary):
                self.summary = obj
            elif isinstance(obj, Results):
                self.results = obj
            else:
                raise TypeError('cannot add type {} to check'.format(
                    type(obj)), obj)
        return self

    def evaluate_resource(self, resource):
        try:
            metric = None
            metrics = resource.probe()
            if not metrics:
                logging.warn('resource %s did not produce any metric',
                             resource.name)
            for metric in metrics:
                context = self.contexts[metric.context]
                metric = metric.replace(contextobj=context, resource=resource)
                self.results.add(metric.evaluate())
                self.perfdata.append(str(metric.performance() or ''))
        except CheckError as e:
            self.results.add(Result(Unknown, str(e), metric))

    def __call__(self):
        for resource in self.resources:
            self.evaluate_resource(resource)
        self.perfdata = sorted([p for p in self.perfdata if p])

    def main(self, verbose=1, timeout=10):
        runtime = Runtime()
        runtime.execute(self, verbose, timeout)

    @property
    def state(self):
        try:
            return self.results.most_significant_state
        except ValueError:
            return Unknown

    @property
    def summary_str(self):
        if self.state == Ok:
            return self.summary.ok(self.results) or ''
        return self.summary.problem(self.results) or ''

    @property
    def verbose_str(self):
        return self.summary.verbose(self.results) or ''

    @property
    def exitcode(self):
        return int(self.results.most_significant_state)
