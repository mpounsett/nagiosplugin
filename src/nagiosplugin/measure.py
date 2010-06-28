# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.state


class Measure(object):

    def __init__(self, name, value, uom=None, warning=None, critical=None,
                 min=None, max=None):
        (self.name, self.value, self.uom) = (name, value, uom)
        (self.warning, self.critical) = (warning, critical)
        (self.min, self.max) =  (min, max)

    def state(self):
        return None

    def performance(self):
        return None
