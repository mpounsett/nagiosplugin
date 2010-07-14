# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import optparse


class PluginOptionParser(optparse.OptionParser):
    """OptionParser variant adapted to Plugin call conventions.

    PluginOptionParser never exits or writes output to stderr. Instead, the new
    attribute `stderr` contains any output. If `stderr` is non-empty after
    `parse_args` invocation, the application should print `stderr` and exit.
    """

    def __init__(self, *args, **kwargs):
        optparse.OptionParser.__init__(self, *args, **kwargs)
        self.stderr = u''

    def exit(self, status=0, msg=None):
        """Override exit() to do nothing."""
        pass

    def error(self, msg):
        """Override error() to append `msg` to self.stderr."""
        self.stderr += msg
        if not self.stderr.endswith(u'\n'):
            self.stderr += u'\n'
