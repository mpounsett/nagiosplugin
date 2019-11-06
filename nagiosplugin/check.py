# -*- coding: utf-8 -*-
"""Controller logic for check execution.

This module contains the :class:`Check` class which orchestrates the
the various stages of check execution. Interfacing with the
outside system is done via a separate :class:`Runtime` object.

When a check is called (using :meth:`Check.main` or
:meth:`Check.__call__`), it probes all resources and evaluates the
returned metrics to results and performance data. A typical usage
pattern would be to populate a check with domain objects and then
delegate control to it.
"""

from .context import Context, Contexts
from .error import CheckError
from .metric import Metric
from .resource import Resource
from .result import Result, Results
from .runtime import Runtime
from .state import Ok, Unknown, ServiceState
from .summary import Summary
import logging

_log = logging.getLogger(__name__)


class Check(object):

    def __init__(self, *objects):
        """Creates and configures a check.

        Specialized *objects* representing resources, contexts,
        summary, or results are passed to the the :meth:`add` method.
        Alternatively, objects can be added later manually.
        """
        self.resources = []
        self.contexts = Contexts()
        self.summary = Summary()
        self.results = Results()
        self.perfdata = []
        self.name = ''
        self.add(*objects)

    def add(self, *objects):
        """Adds domain objects to a check.

        :param objects: one or more objects that are descendants from
            :class:`~nagiosplugin.resource.Resource`,
            :class:`~nagiosplugin.context.Context`,
            :class:`~nagiosplugin.summary.Summary`, or
            :class:`~nagiosplugin.result.Results`.
        """
        for obj in objects:
            if isinstance(obj, Resource):
                self.resources.append(obj)
                if self.name == '':
                    self.name = self.resources[0].name
            elif isinstance(obj, Context):
                self.contexts.add(obj)
            elif isinstance(obj, Summary):
                self.summary = obj
            elif isinstance(obj, Results):
                self.results = obj
            else:
                raise TypeError('cannot add type {0} to check'.format(
                    type(obj)), obj)
        return self

    def _evaluate_resource(self, resource):
        try:
            metric = None
            metrics = resource.probe()
            if not metrics:
                _log.warning('resource %s did not produce any metric',
                             resource.name)
            if isinstance(metrics, Metric):
                # resource returned a bare metric instead of list/generator
                metrics = [metrics]
            for metric in metrics:
                context = self.contexts[metric.context]
                metric = metric.replace(contextobj=context, resource=resource)
                result = metric.evaluate()
                if isinstance(result, Result):
                    self.results.add(result)
                elif isinstance(result, ServiceState):
                    self.results.add(Result(result, metric=metric))
                else:
                    raise ValueError(
                        'evaluate() returned neither Result nor ServiceState '
                        'object', metric.name, result)
                self.perfdata.append(str(metric.performance() or ''))
        except CheckError as e:
            self.results.add(Result(Unknown, str(e), metric))

    def __call__(self):
        """Actually run the check.

        After a check has been called, the :attr:`results` and
        :attr:`perfdata` attributes are populated with the outcomes. In
        most cases, you should not use __call__ directly but invoke
        :meth:`main`, which delegates check execution to the
        :class:`Runtime` environment.
        """
        for resource in self.resources:
            self._evaluate_resource(resource)
        self.perfdata = sorted([p for p in self.perfdata if p])

    def main(self, verbose=None, timeout=None):
        """All-in-one control delegation to the runtime environment.

        Get a :class:`~nagiosplugin.runtime.Runtime` instance and
        perform all phases: run the check (via :meth:`__call__`), print
        results and exit the program with an appropriate status code.

        :param verbose: output verbosity level between 0 and 3
        :param timeout: abort check execution with a :exc:`Timeout`
            exception after so many seconds (use 0 for no timeout)
        """
        runtime = Runtime()
        runtime.execute(self, verbose, timeout)

    @property
    def state(self):
        """Overall check state.

        The most significant (=worst) state seen in :attr:`results` to
        far. :obj:`~nagiosplugin.state.Unknown` if no results have been
        collected yet. Corresponds with :attr:`exitcode`. Read-only
        property.
        """
        try:
            return self.results.most_significant_state
        except ValueError:
            return Unknown

    @property
    def summary_str(self):
        """Status line summary string.

        The first line of output that summarizes that situation as
        perceived by the check. The string is usually queried from a
        :class:`Summary` object. Read-only property.
        """
        if not self.results:
            return self.summary.empty() or ''
        elif self.state == Ok:
            return self.summary.ok(self.results) or ''
        return self.summary.problem(self.results) or ''

    @property
    def verbose_str(self):
        """Additional lines of output.

        Long text output if check runs in verbose mode. Also queried
        from :class:`~nagiosplugin.summary.Summary`. Read-only property.
        """
        return self.summary.verbose(self.results) or ''

    @property
    def exitcode(self):
        """Overall check exit code according to the Nagios API.

        Corresponds with :attr:`state`. Read-only property.
        """
        try:
            return int(self.results.most_significant_state)
        except ValueError:
            return 3
