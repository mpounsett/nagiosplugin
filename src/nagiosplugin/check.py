from .context import Context
from .resource import Resource
from .result import ResultSet, InternalWarning, InternalError
from .state import Ok
from .summary import Summary
import functools
import io
import logging
import numbers
import operator
import sys
import traceback


class Check(object):

    def __init__(self, *objects, name=None):
        self.resources = []
        self.contexts = []
        self.context_by_metric = {}
        self.metrics = []
        self.summaries = []
        self.performance_data = []
        self.results = ResultSet()
        self.add(*objects)
        self.name = name or self.resources[0].__class__.__name__

    def add(self, *objects):
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
            try:
                metric.context = self.context_by_metric[metric.name]
            except KeyError:
                pass
            self.results.add(metric.evaluate())
        if not self.results:
            self.results.add(InternalWarning(
                'check did not produce any results'))

    def __call__(self):
        try:
            self.evaluate()
            self.performance_data = sorted([str(m.performance() or '')
                                            for m in self.metrics])
        except Exception:
            exc_type, value, tb = sys.exc_info()
            filename, lineno = traceback.extract_tb(tb)[-1][0:2]
            self.results.add(InternalError('%s (%s:%d)' % (
                traceback.format_exception_only(exc_type, value)[0].strip(),
                filename, lineno)))
            logging.warning(''.join(traceback.format_tb(tb)))

    @property
    def summary(self):
        if not self.summaries:
            self.summaries = [Summary()]
        if self.results.worst_state == Ok:
            return '; '.join(s.ok(self.results) for s in self.summaries)
        return '; '.join(s.problem(self.results) for s in self.summaries)

    def __str__(self):
        out = ['%s %s: %s' % (
            self.name.upper(), str(self.results.worst_state).upper(),
            self.summary)]
        out += ['| ' + ' '.join(self.performance_data)]
        return '\n'.join(elem for elem in out if elem)

    @property
    def exitcode(self):
        return int(self.results.worst_state)
