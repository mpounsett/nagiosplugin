# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

class Range(object):
    """Represents a threshold range.

    The general format is `[@][start:][end]`. `start:` may be omitted if
    start==0. `~:` means that start is negative infinity. If `end` is omitted,
    infinity is assumed. To invert the match condition, prefix the range
    expression with `@`.

    See http://nagiosplug.sourceforge.net/developer-guidelines.html#THRESHOLDFORMAT
    for details.
    """

    def __init__(self, spec=None):
        """Create a Range object according to `spec`."""
        self.spec = spec = (spec or u'')
        if spec.startswith(u'@'):
            self.invert = True
            spec = spec[1:]
        else:
            self.invert = False
        if spec.find(u':') < 0:
            spec = ':' + spec
        (start, end) = spec.split(u':')
        if start == u'~':
            self.start = None
        elif start:
            self.start = float(start)
        else:
            self.start = 0
        if len(end):
            self.end = float(end)
        else:
            self.end = None
        self.verify()

    def verify(self):
        """Throw ValueError if the range is not consistent."""
        if (self.start is not None and self.end is not None and
            self.start > self.end):
            raise ValueError(u'start %f must not be greater than end %f' % (
                             self.start, self.end))

    def match(self, value):
        """Decide if `value` is inside/outside the bounds."""
        if self.start is not None and value < self.start:
            return False ^ self.invert
        if self.end is not None and value > self.end:
            return False ^ self.invert
        return True ^ self.invert

    def __str__(self):
        """Return a human-readable range specification."""
        result = []
        if self.invert:
            result.append(u'@')
        if self.start is None:
            result.append(u'~:')
        elif self.start != 0:
            result.append((u'%g:' % self.start))
        if self.end is not None:
            result.append((u'%g' % self.end))
        return u''.join(result)

    def __repr__(self):
        """Return a parseable range specification."""
        return u'Range(%r)' % str(self)

    def __eq__(self, other):
        """True if both objects represent the same value range."""
        return all(map(lambda a: getattr(self, a) == getattr(other, a),
                       self.__dict__.keys()))

    def __ne__(self, other):
        """True if the value ranges of both objects differ."""
        return any(map(lambda a: getattr(self, a) != getattr(other, a),
                       self.__dict__.keys()))
