# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

"""Outcomes from evaluating metrics in contexts.

This module contains the :class:`Result` base class which is the base
class for all evaluation results together with its common special case
:class:`ScalarResult` which occurs from evaluating a
:class:`~nagiosplugin.context.ScalarContext`.

The :class:`Results` class provides a result container together with
convenient access functions.
"""

import collections
import numbers


class Result(collections.namedtuple('Result', 'state hint metric')):
    """Check result value.

    A Result object is
    typically emitted by a :class:`~nagiosplugin.context.Context` object
    and represents the outcome of an evaluation. It contains a
    :class:`~nagiosplugin.state.State` as well as an explanation. Plugin
    authors may subclass Result to implement specific features.
    """

    def __new__(cls, state, hint=None, metric=None):
        """Create new Result object.

        :param state: state object
        :param hint: reason why this result arose
        :param metric: reference to the
            :class:`~nagiosplugin.metric.Metric` this result was derived
            from
        """
        return tuple.__new__(cls, (state, hint, metric))

    def __str__(self):
        """Textual result explanation.

        This method's output should return only a text for the reason
        but not the result's state. The latter is rendered
        independently.
        """
        return self.hint or ''

    @property
    def resource(self):
        """Reference to the resource used to generate this result."""
        if self.metric:
            return self.metric.resource

    @property
    def context(self):
        """Reference to the metric used to generate this result."""
        if self.metric:
            return self.metric.contextobj


class ScalarResult(Result):
    """Special-case result for evaluation in a ScalarContext.

    A ScalarResult differs from Result in two ways: First, when the
    :class:`~nagiosplugin.range.Range` object which led to its creation
    is passed as hint, it constructs an explanation automatically.
    Second, it always expects a metric to be present.
    """

    def __new__(cls, state, hint, metric):
        if not metric:
            raise RuntimeError('ScalarResult always needs metric')
        return tuple.__new__(cls, (state, hint, metric))

    def __str__(self):
        if self.hint:
            hint = (self.hint.violation if hasattr(self.hint, 'violation')
                    else self.hint)
            return '{} ({})'.format(self.metric.description, hint)
        return str(self.metric.description)


class Results:
    """Result container.

    Basically, this class manages a set of results and provides
    convenient access methods by index, name, or result state. It is
    meant to make queries in :class:`~nagiosplugin.summary.Summary`
    implementations compact and readable.

    The constructor accepts an arbitrary number of result objects and
    adds them to the container.
    """

    def __init__(self, *results):
        self.results = []
        self.by_state = collections.defaultdict(list)
        self.by_name = {}
        if results:
            self.add(*results)

    def add(self, *results):
        """Adds more results to the container.

        Besides passing :class:`Result` objects in the constructor,
        additional results may be added after creating the container.
        """
        for result in results:
            self.results.append(result)
            self.by_state[result.state].append(result)
            try:
                self.by_name[result.metric.name] = result
            except AttributeError:
                pass
        return self

    def __iter__(self):
        """Iterates over results in order of decreasing state significance."""
        for state in reversed(sorted(self.by_state)):
            for result in self.by_state[state]:
                yield result

    def __len__(self):
        """Number of results in this container."""
        return len(self.results)

    def __getitem__(self, value):
        """Access result by index or name.

        If *value* is an integer, the *value*th element in the container
        is returned. If *value* is a string, it is used to look up a
        result with the giiven name.

        :raises KeyError: if no matching result is found
        """
        if isinstance(value, numbers.Number):
            return self.results[value]
        return self.by_name[value]

    def __contains__(self, name):
        """Tests if a result with given name is present."""
        return name in self.by_name

    @property
    def most_significant_state(self):
        """Returns the "worst" of all states present in the results."""
        return max(self.by_state.keys())

    @property
    def most_significant(self):
        """Returns list of results with the most significant state.

        From all results present, a subset with the "worst" state is
        selected.
        """
        try:
            return self.by_state[self.most_significant_state]
        except ValueError:
            return []

    @property
    def first_significant(self):
        """Returns one of the results with the most significant state."""
        return self.most_significant[0]
