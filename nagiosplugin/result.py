# -*- coding: utf-8 -*-
"""Outcomes from evaluating metrics in contexts.

The :class:`Result` class is the base class for all evaluation results.
The :class:`Results` class (plural form) provides a result container with
access functions and iterators.

Plugin authors may create their own :class:`Result` subclass to
accomodate for special needs. :class:`~.context.Context` constructors
accept custom Result subclasses in the `result_cls` parameter.
"""

from __future__ import unicode_literals
import collections
import numbers
import warnings


class Result(collections.namedtuple('Result', 'state hint metric')):
    """Evaluation outcome consisting of state and explanation.

    A Result object is typically emitted by a
    :class:`~nagiosplugin.context.Context` object and represents the
    outcome of an evaluation. It contains a
    :class:`~nagiosplugin.state.ServiceState` as well as an explanation.
    Plugin authors may subclass Result to implement specific features.
    """

    def __new__(cls, state, hint=None, metric=None):
        """Creates a Result object.

        :param state: state object
        :param hint: reason why this result arose
        :param metric: reference to the
            :class:`~nagiosplugin.metric.Metric` from which this result
            was derived
        """
        return tuple.__new__(cls, (state, hint, metric))

    def __str__(self):
        """Textual result explanation.

        The result explanation is taken from :attr:`metric.description`
        (if a metric has been passed to the constructur), followed
        optionally by the value of :attr:`hint`. This method's output
        should consist only of a text for the reason but not for the
        result's state. The latter is rendered independently.

        :returns: result explanation or empty string
        """
        if self.metric and self.metric.description:
            desc = self.metric.description
        else:
            desc = None
        if self.hint and desc:
            return '{0} ({1})'.format(desc, self.hint)
        elif self.hint:
            return self.hint
        elif desc:
            return desc
        else:
            return ''

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


class ScalarResult(Result):  # pragma: no cover
    """Special-case result for evaluation in a ScalarContext.

    DEPRECATED: use Result instead.
    """

    def __new__(cls, state, hint, metric):
        warnings.warn('ScalarResult is deprecated, use Result instead!',
                      DeprecationWarning)
        return tuple.__new__(cls, (state, hint, metric))


class Results:
    """Container for result sets.

    Basically, this class manages a set of results and provides
    convenient access methods by index, name, or result state. It is
    meant to make queries in :class:`~.summary.Summary`
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

        :raises ValueError: if `result` is not a :class:`Result` object
        """
        for result in results:
            if not isinstance(result, Result):
                raise ValueError(
                    'trying to add non-Result to Results container', result)
            self.results.append(result)
            self.by_state[result.state].append(result)
            try:
                self.by_name[result.metric.name] = result
            except AttributeError:
                pass
        return self

    def __iter__(self):
        """Iterates over all results.

        The iterator is sorted in order of decreasing state
        significance (unknown > critical > warning > ok).

        :returns: result object iterator
        """
        for state in reversed(sorted(self.by_state)):
            for result in self.by_state[state]:
                yield result

    def __len__(self):
        """Number of results in this container."""
        return len(self.results)

    def __getitem__(self, item):
        """Access result by index or name.

        If *item* is an integer, the itemth element in the
        container is returned. If *item* is a string, it is used to
        look up a result with the given name.

        :returns: :class:`Result` object
        :raises KeyError: if no matching result is found
        """
        if isinstance(item, numbers.Number):
            return self.results[item]
        return self.by_name[item]

    def __contains__(self, name):
        """Tests if a result with given name is present.

        :returns: boolean
        """
        return name in self.by_name

    @property
    def most_significant_state(self):
        """The "worst" state found in all results.

        :returns: :obj:`~nagiosplugin.state.ServiceState` object
        :raises ValueError: if no results are present
        """
        return max(self.by_state.keys())

    @property
    def most_significant(self):
        """Returns list of results with most significant state.

        From all results present, a subset with the "worst" state is
        selected.

        :returns: list of :class:`Result` objects or empty list if no
            results are present
        """
        try:
            return self.by_state[self.most_significant_state]
        except ValueError:
            return []

    @property
    def first_significant(self):
        """Selects one of the results with most significant state.

        :returns: :class:`Result` object
        :raises IndexError: if no results are present
        """
        return self.most_significant[0]
