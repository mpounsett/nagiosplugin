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
            start = None
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
            end = None
        cls._verify(start, end)
        return (invert, start, end)

    @classmethod
    def _verify(cls, start, end):
        """Throw ValueError if the range is not consistent."""
        if (start is not None and end is not None and start > end):
            raise ValueError('start %s must not be greater than end %s' % (
                             start, end))

    def match(self, value):
        """Decide if `value` is inside/outside the bounds."""
        if self.start is not None and value < self.start:
            return False ^ self.invert
        if self.end is not None and value > self.end:
            return False ^ self.invert
        return True ^ self.invert

    def __contains__(self, value):
        return self.match(value)

    def __str__(self):
        """Return a human-readable range specification."""
        result = []
        if self.invert:
            result.append('@')
        if self.start is None:
            result.append('~:')
        elif self.start != 0:
            result.append(('%s:' % self.start))
        if self.end is not None:
            result.append(('%s' % self.end))
        return ''.join(result)

    def __repr__(self):
        """Return a parseable range specification."""
        return 'Range(%r)' % str(self)

    @property
    def violation(self):
        """Human-readable description why a value does not match."""
        if self.start:
            return 'outside {}'.format(self)
        return 'greater than {}'.format(self)
