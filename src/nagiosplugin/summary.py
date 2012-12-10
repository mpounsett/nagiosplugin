# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Base class to derive custom summary classes."""

from .state import Ok


class Summary(object):
    """Constructs status line from set of results.

    The status line is probably the most important piece of text
    returned from a check. It must lead directly to the problem in the
    most concise way. To do so, :class:`Summary` has methods for
    status output in different situations which may be overriden
    individuall by plugin authors. This base class takes no parameters
    in its constructor, but subclasses may provide more elaborate
    constructures to represent global plugin state for example.
    """

    def ok(self, results):
        """Format status line when overall state is ok.

        The default implementation returns a string representation of
        the first result. Thin usually corresponds with the first metric
        returned.

        :param results: :class:`~nagiosplugin.result.Results` container.
        :returns: single-line string.
        """

        return str(results[0])

    def problem(self, results):
        """Format status line when overall state is not ok.

        The default implementation returns a string representation of te
        first significant result, i.e. the result with the "worst"
        state.

        :param results: :class:`~nagiosplugin.result.Results` container.
        :returns: single-line string.
        """

        try:
            return str(results.first_significant)
        except IndexError:
            return 'no check results'

    def verbose(self, results):
        """Extra lines if verbose plugin execution is requested.

        The default implementation returns a list of all non-ok states,
        one a line.

        :param results: :class:`~nagiosplugin.result.Results` container.
        :returns: list of strings.
        """

        msgs = []
        for result in results:
            if result.state == Ok:
                continue
            msgs.append('{}: {}'.format(result.state, result))
        return msgs
