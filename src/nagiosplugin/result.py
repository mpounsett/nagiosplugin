from .range import Range
from .state import Ok, Unknown
import collections
import functools
import operator


class Result:

    def __init__(self, state, reason):
        self.state = state
        self.reason = reason
        self.resource = None

    def __str__(self):
        return self.reason


class ScalarResult(Result):

    def __init__(self, state, reason, metric):
        super(ScalarResult, self).__init__(state, reason)
        self.metric = metric

    def __str__(self):
        if self.state == Ok:
            return '%s is %s' % (self.metric.description, self.metric)
        if isinstance(self.reason, Range) and self.reason.start:
            return '%s %s is outside range %s' % (
                self.metric.description, self.metric, self.reason)
        return '%s %s is greater than %s' % (
            self.metric.description, self.metric, self.reason)

    @property
    def name(self):
        return self.metric.name

    @property
    def value(self):
        return self.metric.value

    @property
    def uom(self):
        return self.metric.uom


class ResultSet:

    def __init__(self):
        self.by_state = collections.defaultdict(list)
        self.by_name = {}
        self.by_resource = collections.defaultdict(list)

    def add(self, result, resource=None):
        if resource:
            result.resource = resource
            self.by_resource[resource] = result.name
        self.by_state[result.state].append(result)
        try:
            self.by_name[result.metric.name] = result
        except AttributeError:
            pass

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
