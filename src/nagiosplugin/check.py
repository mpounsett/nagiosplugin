from .context import Context, Contexts
from .error import CheckError
from .resource import Resource
from .result import Result, Results
from .state import Ok, Unknown
from .summary import Summary
import logging


class Check(object):

    def __init__(self, *objects):
        self.resources = []
        self.contexts = Contexts()
        self.summary = Summary()
        self.perfdata = []
        self.results = Results()
        self.add(*objects)
        self.runtime = None

    @property
    def name(self):
        try:
            return self.resources[0].name
        except IndexError:
            return ''

    def add(self, *objects):
        for obj in objects:
            if isinstance(obj, Resource):
                self.resources.append(obj)
            elif isinstance(obj, Context):
                self.contexts.add(obj)
            elif isinstance(obj, Summary):
                self.summary = obj
            else:
                raise RuntimeError('%r has not an allowed type' % obj)

    def evaluate_metric(self, resource, metric):
        context = self.contexts.match_metric(metric.name)
        self.results.add(context.evaluate(metric, resource))
        self.perfdata.append(str(context.performance(metric, resource) or ''))

    def evaluate_resource(self, resource):
        try:
            metric = None
            metrics = resource.survey()
            if not metrics:
                logging.warn('resource %s did not produce any metric',
                             resource.name)
            for metric in metrics:
                self.evaluate_metric(resource, metric)
        except CheckError as e:
            self.results.add(Result(Unknown, str(e), metric, resource))

    def __call__(self, runtime):
        self.runtime = runtime
        for resource in self.resources:
            self.evaluate_resource(resource)
        self.perfdata = sorted([p for p in self.perfdata if p])

    @property
    def state(self):
        return self.results.most_significant_state

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
