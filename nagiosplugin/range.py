import collections
import math


class Range(collections.namedtuple('Range', 'invert start end')):
    """Represents a threshold range.

    The general format is "[@][start:][end]". "start:" may be omitted if
    start==0. "~:" means that start is negative infinity. If `end` is
    omitted, infinity is assumed. To invert the match condition, prefix
    the range expression with "@".

    An empty range specification (or `None`) is unbounded in both
    directions, like "~:", and so matches every value. Use it for a
    threshold that should never trigger.

    See https://nagios-plugins.org/doc/guidelines.html#thresholds for details.
    """

    def __new__(cls, spec=''):
        """Creates a Range object according to `spec`.

        :param spec: may be either a string, an int, a float, or another
            Range object. `None` is treated the same as the empty string.
        """
        if spec is None:
            spec = ''
        if isinstance(spec, Range):
            return super().__new__(
                cls, spec.invert, spec.start, spec.end)
        elif isinstance(spec, bool):
            raise TypeError(
                'bool is not a valid range spec; use None or "" for no range')
        elif isinstance(spec, (int, float)):
            start, end, invert = 0, spec, False
        else:
            start, end, invert = cls._parse(str(spec))
        cls._verify(start, end)
        return super().__new__(cls, invert, start, end)

    @classmethod
    def _parse(cls, spec):
        invert = False
        if spec.startswith('@'):
            invert = True
            spec = spec[1:]
        if spec == '':
            return float('-inf'), float('inf'), invert
        if ':' in spec:
            start, end = spec.split(':')
        else:
            start, end = '', spec
        if start == '~':
            start = float('-inf')
        else:
            start = cls._parse_atom(start, 0)
        end = cls._parse_atom(end, float('inf'))
        return start, end, invert

    @staticmethod
    def _parse_atom(atom, default):
        if atom == '':
            return default
        if '.' in atom:
            return float(atom)
        return int(atom)

    @staticmethod
    def _verify(start, end):
        """Throws ValueError if the range is not consistent."""
        if math.isnan(start) or math.isnan(end):
            raise ValueError('range bounds must not be NaN')
        if start > end:
            raise ValueError('start %s must not be greater than end %s' % (
                             start, end))

    def match(self, value):
        """Decides if `value` is inside/outside the threshold.

        :returns: `True` if value is inside the bounds for non-inverted
            Ranges.

        Also available as `in` operator.
        """
        if value < self.start:
            return False ^ self.invert
        if value > self.end:
            return False ^ self.invert
        return True ^ self.invert

    def __contains__(self, value):
        return self.match(value)

    def _format(self, omit_zero_start=True):
        # The unbounded range "~:" is rendered as "" so that performance data
        # shows no threshold at all. A zero start may only be omitted when
        # there is an end, since "0:" and "" are different ranges.
        unbounded_end = self.end == float('inf')
        result = []
        if self.invert:
            result.append('@')
        if self.start == float('-inf'):
            if not unbounded_end or not omit_zero_start:
                result.append('~:')
        elif not omit_zero_start or self.start != 0 or unbounded_end:
            result.append('%s:' % self.start)
        if not unbounded_end:
            result.append('%s' % self.end)
        return ''.join(result)

    def __str__(self):
        """Human-readable range specification."""
        return self._format()

    def __repr__(self):
        """Parseable range specification."""
        return 'Range(%r)' % str(self)

    @property
    def violation(self):
        """Human-readable description why a value does not match."""
        return f'outside range {self._format(False)}'
