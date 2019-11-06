# -*- coding: utf-8 -*-
"""Create status line from results.

This module contains the :class:`Summary` class which serves as base
class to get a status line from the check's :class:`~.result.Results`. A
Summary object is used by :class:`~.check.Check` to obtain a suitable data
:term:`presentation` depending on the check's overall state.

Plugin authors may either stick to the default implementation  or subclass it
to adapt it to the check's domain. The status line is probably the most
important piece of text returned from a check: It must lead directly to the
problem in the most concise way. So while the default implementation is quite
usable, plugin authors should consider subclassing to provide a specific
implementation that gets the output to the point.
"""

from __future__ import unicode_literals
from .state import Ok


class Summary(object):
    """Creates a summary formtter object.

    This base class takes no parameters in its constructor, but subclasses may
    provide more elaborate constructors that accept parameters to influence
    output creation.
    """

    def ok(self, results):
        """Formats status line when overall state is ok.

        The default implementation returns a string representation of
        the first result.

        :param results: :class:`~nagiosplugin.result.Results` container
        :returns: status line
        """
        return '{0}'.format(results[0])

    def problem(self, results):
        """Formats status line when overall state is not ok.

        The default implementation returns a string representation of te
        first significant result, i.e. the result with the "worst"
        state.

        :param results: :class:`~.result.Results` container
        :returns: status line
        """
        return '{0}'.format(results.first_significant)

    def verbose(self, results):
        """Provides extra lines if verbose plugin execution is requested.

        The default implementation returns a list of all resources that are in
        a non-ok state.

        :param results: :class:`~.result.Results` container
        :returns: list of strings
        """
        msgs = []
        for result in results:
            if result.state == Ok:
                continue
            msgs.append('{0}: {1}'.format(result.state, result))
        return msgs

    def empty(self):
        """Formats status line when the result set is empty.

        :returns: status line
        """
        return 'no check results'
