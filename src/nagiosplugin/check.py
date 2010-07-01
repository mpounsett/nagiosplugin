# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import optparse


class Check(object):

    name = u'check'

    def __init__(self, optparser):
        u"""Create new check plugin instance.

        Call the usual optparse methods (like `add_option`) on `optparser` to
        define custom options.
        """
        pass

    def verify_arguments(self, opts, args):
        if args:
            raise optparse.OptParseError(u'superfluous arguments: %s' % args)

    def measure(self, opts, args):
        """Return array of Measure objects to create plugin output."""
        raise NotImplementedError

    @property
    def shortname(self):
        """Short check name for the headline. Override if necessary."""
        return self.name.split()[0].upper()

    @property
    def default_message(self):
        """Fallback OK message string if nothing special happened."""
        return None
