# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

class Range(object):

    def __init__(self, spec=u''):
        self.spec = spec
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
        if (self.start is not None and self.end is not None and
            self.start > self.end):
            raise ValueError(u'start %f must not be greater than end %f' % (
                             self.start, self.end))

    def match(self, value):
        if self.start is not None and value < self.start:
            return False ^ self.invert
        if self.end is not None and value > self.end:
            return False ^ self.invert
        return True ^ self.invert

    def __str__(self):
        result = []
        if self.invert:
            result.append(u'@')
        if self.start is None:
            result.append(u'~:')
        elif self.start != 0:
            result.append((u'%.20g:' % self.start).strip())
        if self.end is not None:
            result.append((u'%20g' % self.end).strip())
        return u''.join(result)
