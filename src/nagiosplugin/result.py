# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .range import Range
from .state import Unknown
import collections


class Result:

    def __init__(self, state, reason=None, metric=None, resource=None):
        self.state = state
        self.reason = reason
        self.metric = metric
        self.resource = resource

    def __str__(self):
        return self.reason


class ScalarResult(Result):

    def __init__(self, state, reason, metric, resource=None):
        super(ScalarResult, self).__init__(state, reason, metric, resource)
        if not self.metric:
            raise RuntimeError('ScalarResult always needs metric', self)

    def __str__(self):
        if isinstance(self.reason, Range):
            return '{} ({})'.format(self.metric.description,
                                    self.reason.violation)
        if self.reason:
            return '{} ({})'.format(self.metric.description, self.reason)
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
        return iter(self.results)

    def __getitem__(self, value):
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
