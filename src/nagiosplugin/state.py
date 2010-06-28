# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt


def reduce(state1, state2):
    pass


class State(object):
    """Represents the logical outcome of checks.

    A State has a numeric state code and a status word denoting the result. In
    addition a state carries one or more message lines. The first message line
    goes into Nagios' main status message and the remaining lines go into
    Nagios' long output (introduced with Nagios 3).
    """

    code = None
    word = None

    def __init__(self, messages=[]):
        if not isinstance(messages, list):
            messages = [messages]
        self.messages = messages

    def __str__(self):
        """Numeric status code."""
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.word

    def __int__(self):
        """Textual status code."""
        if self.code is None or self.word is None:
            raise NotImplementedError
        return self.code

    def __cmp__(self, other):
        return self.code.__cmp__(other.code)

    def mainoutput(self):
        """Main status message (the only one supported with Nagios 1 and 2)."""
        return self.messages[0]

    def longoutput(self):
        """Additional status messages."""
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
