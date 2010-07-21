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
        self.error_message = None

    def exit(self, status=0, msg=None):
        """Overridden to do nothing."""
        pass

    def _print_stderr(self, msg):
        """Append `msg` to self.stderr. Add newline if necessary."""
        if not msg.endswith(u'\n'):
            msg += u'\n'
        self.stderr += msg

    def error(self, msg):
        """Overridden to append `msg` to self.stderr."""
        self.print_usage()
        self._print_stderr(u'%s: error: %s' % (self.get_prog_name(), msg))
        self.error_message = msg

    def print_usage(self, file=None):
        """Overridden to append usage to self.stderr."""
        if self.usage:
            self._print_stderr(self.get_usage())

    def print_version(self, file=None):
        """Overridden to append version to self.stderr."""
        if self.version:
            self._print_stderr(self.get_version())

    def print_help(self, file=None):
        self._print_stderr(self.format_help())
