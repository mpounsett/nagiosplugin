from .range import Range
from .state import Ok, Unknown
import collections
import functools
import operator


class Result:

    def __init__(self, metric, state, failinfo=None):
        self.metric = metric
        self.state = state
        self.failinfo = failinfo

    def __str__(self):
        if self.state == Ok():
            return '%s is %s' % (self.metric.description, self.metric)
        if isinstance(self.failinfo, Range) and self.failinfo.start:
            return '%s %s is outside range %s' % (
                self.metric.description, self.metric, self.failinfo)
        return '%s %s is over %s' % (
            self.metric.description, self.metric, self.failinfo)


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
            return Unknown()

    @property
    def worst_category(self):
        try:
            return self.by_state[self.worst_state]
        except KeyError:
            return []

    def __iter__(self):
        return iter(functools.reduce(operator.add, self.by_state.values()))
