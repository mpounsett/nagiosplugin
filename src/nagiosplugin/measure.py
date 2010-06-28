# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.range
import nagiosplugin.state


class Measure(object):

    def __init__(self, name, value, uom=None, warning=None, critical=None,
                 min=None, max=None):
        (self.name, self.value, self.uom) = (name, value, uom)
        (self.warning, self.critical) = map(nagiosplugin.range.Range,
                                            (warning, critical))
        (self.min, self.max) =  (min, max)

    def state(self):
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
        return None
