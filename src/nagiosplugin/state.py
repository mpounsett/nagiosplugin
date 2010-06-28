# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt


class State(object):
    code = None
    text = None

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.code is None or self.text is None:
            raise NotImplementedError
        if self.message:
            return u'%s - %s' % (self.text, self.message)
        return self.text

    def __int__(self):
        if self.code is None or self.text is None:
            raise NotImplementedError
        return self.code

    def __cmp__(self, other):
        return self.code.__cmp__(other.code)


class Ok(State):
    code = 0
    text = u'OK'


class Warning(State):
    code = 1
    text = u'WARNING'


class Critical(State):
    code = 2
    text = u'CRITICAL'


class Unknown(State):
    code = 3
    text = u'UNKNOWN'
