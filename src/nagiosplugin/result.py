# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import collections
import numbers


class Result(collections.namedtuple('Result', 'state reason metric')):

    def __new__(cls, state, reason=None, metric=None):
        return tuple.__new__(cls, (state, reason, metric))

    def __str__(self):
        return self.reason

    @property
    def resource(self):
        if self.metric:
            return self.metric.resource

    @property
    def context(self):
        if self.metric:
            return self.metric.contextobj


class ScalarResult(Result):

    def __new__(cls, state, reason, metric):
        if not metric:
            raise RuntimeError('ScalarResult always needs metric')
        return tuple.__new__(cls, (state, reason, metric))

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

    def add(self, *results):
        for result in results:
            self.results.append(result)
            self.by_state[result.state].append(result)
            try:
                self.by_name[result.metric.name] = result
            except AttributeError:
                pass
        return self

    def __iter__(self):
        for state in reversed(sorted(self.by_state)):
            for result in self.by_state[state]:
                yield result

    def __len__(self):
        return len(self.results)

    def __getitem__(self, value):
        if isinstance(value, numbers.Number):
            return self.results[value]
        return self.by_name[value]

    def __contains__(self, item):
        return item in self.by_name

    @property
    def most_significant_state(self):
        return max(self.by_state.keys())

    @property
    def most_significant(self):
        try:
            return self.by_state[self.most_significant_state]
        except ValueError:
            return []

    @property
    def first_significant(self):
        return self.most_significant[0]
