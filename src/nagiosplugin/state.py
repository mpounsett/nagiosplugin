# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt


class State(object):
    code = None
    word = None

    def __init__(self, messages=[]):
        if not isinstance(messages, list):
            messages = [messages]
        self.messages = messages

    def __str__(self):
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.word

    def __int__(self):
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.code

    def __cmp__(self, other):
        return self.code.__cmp__(other.code)

    def firstline(self):
        return self.messages[0]

    def longoutput(self):
        return self.messages[1:]


class Ok(State):
    code = 0
    word = u'OK'


class Warning(State):
    code = 1
    word = u'WARNING'


class Critical(State):
    code = 2
    word = u'CRITICAL'


class Unknown(State):
    code = 3
    word = u'UNKNOWN'
