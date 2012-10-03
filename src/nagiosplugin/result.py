from .metric import Metric
from .range import Range
from .state import Ok, Warn, Unknown
import collections
import functools
import operator


class Result:

    def __init__(self, metric, state, info=None):
        self.metric = metric
        self.state = state
        self.info = info

    def __str__(self):
        if self.state == Ok:
            return '%s is %s' % (self.metric.description, self.metric)
        if isinstance(self.info, Range) and self.info.start:
            return '%s %s is outside range %s' % (
                self.metric.description, self.metric, self.info)
        return '%s %s is over %s' % (
            self.metric.description, self.metric, self.info)


class FrameworkWarning(Result):

    def __init__(self, info):
        self.metric = Metric('framework warning', None)
        # XXX make the state for FrameworkWarnings configurable
        self.state = Warn
        self.info = info

    def __str__(self):
        return self.info


class FrameworkError(Result):

    def __init__(self, info):
        self.metric = Metric('framework error', None)
        self.state = Unknown
        self.info = info

    def __str__(self):
        return self.info


class ResultSet:

    def __init__(self):
        self.by_state = collections.defaultdict(list)
        self.by_name = {}

    def add(self, result):
        self.by_state[result.state].append(result)
        self.by_name[result.metric.name] = result

    def __getitem__(self, value):
        return self.by_name[value]

    @property
    def worst_state(self):
        try:
            return max(self.by_state.keys())
        except TypeError:
            return Unknown

    @property
    def worst_category(self):
        try:
            return self.by_state[self.worst_state]
        except KeyError:
            return []

    def __iter__(self):
        return iter(functools.reduce(operator.add, self.by_state.values()))

    def first_significant(self):
        return self.worst_category[0]
