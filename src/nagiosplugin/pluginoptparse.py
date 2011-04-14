# Copyright (c) 2010-2011 gocept gmbh & co. kg
# See also LICENSE.txt

import cStringIO
import optparse
import sys


class PluginOptionParser(optparse.OptionParser):
    """OptionParser variant adapted to Plugin call conventions.

    PluginOptionParser never exits or writes output to stderr. Instead, the new
    attribute `stderr` contains any output. If `stderr` is non-empty after
    `parse_args` invocation, the application should print `stderr` and exit.
    """

    def __init__(self, *args, **kwargs):
        optparse.OptionParser.__init__(self, *args, **kwargs)
        self.stderr = cStringIO.StringIO()
        self.stdout = cStringIO.StringIO()
        self.error_message = None

    def parse_args(self, args=None, values=None):
        ret = (None, None)
        try:
            ret = optparse.OptionParser.parse_args(self, args, values)
        except UnboundLocalError:
            e = sys.exc_info()[1]
            self._print(u'invalid option (internal error: %s)' % e)
        return ret

    def exit(self, status=0, msg=None):
        """Overridden to do nothing."""
        pass

    def _print(self, msg, channel=None):
        """Append `msg` to string buffer `channel`. Add newline if necessary."""
        if channel is None:
            channel = self.stderr
        print >>channel, msg

    def error(self, msg):
        """Overridden to append error message `msg` to self.stderr."""
        self.print_usage()
        self._print(u'%s: error: %s' % (self.get_prog_name(), msg))
        self.error_message = msg

    def print_usage(self, file=None):
        """Overridden to append usage to self.stderr."""
        if self.usage:
            self._print(self.get_usage())

    def print_version(self, file=None):
        """Overridden to append version to self.stderr."""
        if self.version:
            msg = self.get_prog_name() + u' ' + self.get_version()
            self._print(msg, self.stdout)

    def print_help(self, file=None):
        self._print(self.format_help(), self.stdout)

    def get_stdout(self):
        return self.stdout.getvalue()

    def get_stderr(self):
        return self.stderr.getvalue()
