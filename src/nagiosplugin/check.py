# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import optparse


class Check(object):

    name = u'check'

    def __init__(self, optparser):
        raise NotImplementedError

    def verify_arguments(self, opts, args):
        if args:
            raise optparse.OptParseError(u'superfluous arguments: %s' % args)

    def measure(self, opts, args):
        raise NotImplementedError

    @property
    def default_message(self):
        return None

    @property
    def shortname(self):
        return self.name.split()[0].upper()
