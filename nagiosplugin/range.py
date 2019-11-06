# -*- coding: utf-8 -*-
import collections


class Range(collections.namedtuple('Range', 'invert start end')):
    """Represents a threshold range.

    The general format is "[@][start:][end]". "start:" may be omitted if
    start==0. "~:" means that start is negative infinity. If `end` is
    omitted, infinity is assumed. To invert the match condition, prefix
    the range expression with "@".

    See
    http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
    for details.
    """

    def __new__(cls, spec=''):
        """Creates a Range object according to `spec`.

        :param spec: may be either a string, an int, or another
            Range object.
        """
        spec = spec or ''
        if isinstance(spec, Range):
            return super(cls, Range).__new__(
                cls, spec.invert, spec.start, spec.end)
        elif (isinstance(spec, int) or isinstance(spec, float)):
            start, end, invert = 0, spec, False
        start, end, invert = cls._parse(str(spec))
        cls._verify(start, end)
        return super(cls, Range).__new__(cls, invert, start, end)

    @classmethod
    def _parse(cls, spec):
        invert = False
        if spec.startswith('@'):
            invert = True
            spec = spec[1:]
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
        result = []
        if self.invert:
            result.append('@')
        if self.start == float('-inf'):
            result.append('~:')
        elif not omit_zero_start or self.start != 0:
            result.append(('%s:' % self.start))
        if self.end != float('inf'):
            result.append(('%s' % self.end))
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
        return 'outside range {0}'.format(self._format(False))
