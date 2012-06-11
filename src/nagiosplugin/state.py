# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt


def dominantstate(state1, state2):
    """Select the dominant state from two states.

    If both states are the same, the messages will be concatenated.
    Otherwise, the message from the non-dominant state will be
    discarded.
    """
    if state1 == state2:
        state1.messages.extend(state2.messages)
        return state1
    elif state1 > state2:
        return state1
    return state2


class State(object):
    """Represents the logical outcome of checks.

    A State has a numeric state code and a status word denoting the result. In
    addition a state carries one or more message lines. The first message line
    goes into Nagios' main status message and the remaining lines go into
    Nagios' long output (introduced with Nagios 3).
    """

    code = None
    word = None

    def __init__(self, messages=None):
        if not messages:
            self.messages = []
        elif not isinstance(messages, list):
            self.messages = [messages]
        else:
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
        """Numerical status code comparision."""
        return self.code.__cmp__(other.code)

    def headline(self):
        """Main status message (the only one supported with Nagios 1 and 2)."""
        if self.messages:
            return self.messages[0]

    def longoutput(self):
        """Additional status messages."""
        return self.messages[1:]

    def __repr__(self):
        return u'%s(%r)' % (self.__class__.__name__, self.messages)


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
