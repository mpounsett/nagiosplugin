from .context import Context
from .resource import Resource
from .result import ResultSet
from .summary import Summary
import functools
import io
import logging
import numbers
import operator
import sys


class Check(object):

    def __init__(self, *objects, name=None, verbose=None):
        self.resources = []
        self.contexts = []
        self.context_by_metric = {}
        self.metrics = []
        self.summaries = []
        self.performance_data = []
        self.results = ResultSet()
        self._dispatch_check_objects(objects)
        self.name = name or self.resources[0].__class__.__name__
        if isinstance(verbose, numbers.Number):
            self.init_logging(verbose)
        else:
            self.init_logging(len(verbose or []))

    def init_logging(self, verbose):
        self.logoutput = io.StringIO()
        rootlogger = logging.getLogger()
        rootlogger.setLevel(logging.DEBUG)
        chan = logging.StreamHandler(self.logoutput)
        chan.setFormatter(logging.Formatter(
            '%(filename)s:%(lineno)d: %(message)s'))
        if verbose >= 3:
            chan.setLevel(logging.DEBUG)
        elif verbose == 2:
            chan.setLevel(logging.INFO)
        else:
            chan.setLevel(logging.WARNING)
        rootlogger.addHandler(chan)

    def _dispatch_check_objects(self, objects):
        for obj in objects:
            if isinstance(obj, Resource):
                self.resources.append(obj)
            elif isinstance(obj, Context):
                self.contexts.append(obj)
                self.context_by_metric.update({(m, obj) for m in obj.metrics})
            elif isinstance(obj, Summary):
                self.summaries.append(obj)
            else:
                raise RuntimeError('%r has not an allowed type' % obj)

    def evaluate(self):
        self.metrics = functools.reduce(operator.add, (
            res() for res in self.resources))
        for metric in self.metrics:
            metric.context = self.context_by_metric[metric.name]
            self.results.add(metric.evaluate())

    def run(self):
        self.evaluate()
        self.performance_data = [str(m.performance() or '')
                                 for m in self.metrics]

    @property
    def summary(self):
        if not self.summaries:
            self.summaries = [Summary()]
        return '; '.join(s.brief(self.results) for s in self.summaries)

    def __str__(self):
        out = ['%s %s: %s' % (
            self.name.upper(), str(self.results.worst_state).upper(),
            self.summary)]
        out += ['| ' + ' '.join(self.performance_data)]
        out.append(self.logoutput.getvalue())
        return '\n'.join(elem for elem in out if elem)

    @property
    def exitcode(self):
        return int(self.results.worst_state)

    def main(self):
        self.run()
        print(self)
        sys.exit(self.exitcode)
