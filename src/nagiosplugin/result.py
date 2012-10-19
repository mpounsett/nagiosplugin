# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .state import Unknown
import collections
import numbers
import functools
import operator


class Result:

    def __init__(self, state, reason=None, metric=None):
        self.state = state
        self.reason = reason
        self.metric = metric

    def __str__(self):
        return self.reason

    @property
    def resource(self):
        if self.metric:
            return self.metric.resource

    @property
    def context(self):
        if self.metric:
            return self.metric.context


class ScalarResult(Result):

    def __init__(self, state, reason, metric):
        super(ScalarResult, self).__init__(state, reason, metric)
        if not self.metric:
            raise RuntimeError('ScalarResult always needs metric', self)

    def __str__(self):
        if self.reason:
            hint = (self.reason.violation if hasattr(self.reason, 'violation')
                    else self.reason)
            return '{} ({})'.format(self.metric.description, hint)
        return str(self.metric.description)


class Results:

    def __init__(self):
        self.results = []
        self.by_state = collections.defaultdict(list)
        self.by_name = {}

    def add(self, result):
        self.results.append(result)
        self.by_state[result.state].append(result)
        try:
            self.by_name[result.metric.name] = result
        except AttributeError:
            pass

    def __iter__(self):
        return iter(functools.reduce(operator.add, self.by_state.values()))

    def __getitem__(self, value):
        if isinstance(value, numbers.Number):
            return self.results[value]
        return self.by_name[value]

    @property
    def most_significant_state(self):
        try:
            return max(self.by_state.keys())
        except TypeError:
            return Unknown

    @property
    def most_significant_results(self):
        try:
            return self.by_state[self.most_significant_state]
        except KeyError:
            return []

    def first_significant(self):
        return self.most_significant_results[0]
