# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

import collections


class Range(collections.namedtuple('Range', 'invert start end')):
    """Represents a threshold range.

    The general format is `[@][start:][end]`. `start:` may be omitted if
    start==0. `~:` means that start is negative infinity. If `end` is
    omitted, infinity is assumed. To invert the match condition, prefix
    the range expression with `@`.

    See
    http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
    for details.
    """

    def __new__(cls, spec=''):
        """Create a Range object according to `spec`.

        `spec` may be either a string or another Range object.
        """
        if isinstance(spec, Range):
            return super(cls, Range).__new__(
                cls, spec.invert, spec.start, spec.end)
        return super(cls, Range).__new__(cls, *cls._parse(spec))

    @classmethod
    def _parse(cls, spec):
        invert = False
        spec = spec or ''
        if spec.startswith('@'):
            invert = True
            spec = spec[1:]
        if ':' in spec:
            start, end = spec.split(':')
        else:
            start, end = '', spec
        if start == '~':
            start = float('-inf')
        elif start is not '':
            if '.' in start:
                start = float(start)
            else:
                start = int(start)
        else:
            start = 0
        if end is not '':
            if '.' in end:
                end = float(end)
            else:
                end = int(end)
        else:
            end = float('inf')
        cls._verify(start, end)
        return (invert, start, end)

    @classmethod
    def _verify(cls, start, end):
        """Throw ValueError if the range is not consistent."""
        if start > end:
            raise ValueError('start %s must not be greater than end %s' % (
                             start, end))

    def match(self, value):
        """Decide if `value` is inside/outside the bounds."""
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
        """Return a human-readable range specification."""
        return self._format()

    def __repr__(self):
        """Return a parseable range specification."""
        return 'Range(%r)' % str(self)

    @property
    def violation(self):
        """Human-readable description why a value does not match."""
        return 'outside range {0}'.format(self._format(False))
