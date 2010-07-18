# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import functools
import nagiosplugin.range
import nagiosplugin.state


def _fill(elements, x):
    """Return array of `x` that has at least `elements` elements."""
    if not isinstance(x, list):
        x = [x]
    if len(x) < elements:
        x.extend((elements - len(x)) * x[-1:])
    return x


def _silent_str(value):
    """Return `value` as string but u'' if `value` is None."""
    if value is None:
        return u''
    return str(value)


class Measure(object):

    def __init__(self, name, value, uom=None, warning=None, critical=None,
                 min=None, max=None):
        """Create Measure instance.

        name - short name that identifies this measure
        value - measured value
        uom - unit of measure, used mainly for graphing
        warning - textual representation of warning range
        critical - textual representation of critical range
        min - minimal allowed value
        max - maximal allowed value
        """
        (self.name, self.value, self.uom) = (name, value, uom)
        (self.warning, self.critical) = map(nagiosplugin.range.Range,
                                            (warning, critical))
        (self.min, self.max) =  (min, max)

    @classmethod
    def array(cls, num, names, values, uoms=None, warnings=None, criticals=None,
            mins=None, maxs=None):
        """Create array of `num` measures.

        The usual Measure init parameters need to be given as arrays. If these
        arrays have less than `num` elements, they are filled up with the last
        specified value.
        """
        fill = functools.partial(_fill, num)
        (names, values, uoms, warnings, criticals, mins, maxs) = map(
                fill, (names, values, uoms, warnings, criticals, mins, maxs))
        return [cls(names[i], values[i], uoms[i], warnings[i], criticals[i],
            mins[i], maxs[i]) for i in range(0, num)]

    def state(self):
        """Return the state according to value, warning, and critical."""
        uom = self.uom or u''
        if not self.critical.match(self.value):
            return nagiosplugin.state.Critical([
                    u'%s value %s%s exceeds critical range %s' % (
                    self.name, self.value, uom, self.critical)])
        if not self.warning.match(self.value):
            return nagiosplugin.state.Warning([
                    u'%s value %s%s exceeds warning range %s' % (
                    self.name, self.value, uom, self.warning)])
        return nagiosplugin.state.Ok()

    def performance(self):
        """Return performance data string."""
        p = [u'%s=%s%s' % (self.name, self.value, _silent_str(self.uom)),
             str(self.warning), str(self.critical),
             _silent_str(self.min), _silent_str(self.max)]
        return u';'.join(p).rstrip(u';')

    def __repr__(self):
        return u'Measure(%r, %g, %r, %r, %r, %r, %r)' % (
            self.name, self.value, self.uom, self.warning, self.critical,
            self.min, self.max)

    def __eq__(self, other):
        """Determine equality by comparing all attributes."""
        return self.__dict__ == other.__dict__

    def __neq__(self, other):
        return self.__dict__ != other.__dict__
