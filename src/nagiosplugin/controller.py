# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .platform import with_timeout
from .errors import TimeoutError
import StringIO
import logging
import nagiosplugin.state
import nagiosplugin.pluginoptparse
import sys
import traceback


class Controller(object):

    def __init__(self, check_cls, argv=None):
        """Initialize controller and check instance.

        The check instance is given as class `check_cls` and called with the
        pre-populated option parser and a logger instance.
        """
        self.prepare()
        self.check = check_cls(self.optparser, self.logger)
        self.stderr = u''
        self.exitcode = None
        self.states = []
        self.performances = []
        self.dominant_state = nagiosplugin.state.Unknown()
        (self.opts, self.args) = self.optparser.parse_args(argv)
        if self.optparser.get_stdout():
            self.format = lambda *args: self.optparser.get_stdout()
            self.exitcode = 3
        if self.optparser.get_stderr():
            self.stderr = self.optparser.get_stderr()
            self.exitcode = 3
            self.dominant_state = nagiosplugin.state.Unknown(
                self.optparser.error_message)

    def prepare(self):
        """Prepare ancillary objects: option parser and logger."""
        self.optparser = nagiosplugin.pluginoptparse.PluginOptionParser()
        self.optparser.add_option('-V', '--version', action='version',
                help=u'print version and exit')
        self.optparser.add_option('-v', '--verbose', action='count',
                default=0, help=u'increase output verbosity (up to 3 times)')
        self.optparser.add_option('-t', '--timeout', metavar='TIMEOUT',
                default=15, type='int',
                help=u'abort execution after TIMEOUT seconds '
                     u'(default: %default)')
        self.logger = logging.getLogger('nagiosplugin')
        self.logger.setLevel(logging.DEBUG)
        self.logstream = StringIO.StringIO()
        handler = logging.StreamHandler(self.logstream)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def __call__(self):
        if self.exitcode is None:
            self.run()
        self.print_output()

    def run(self):
        """Run, but interrupt check if it takes longer than the timeout."""
        loglevel = max((40 - self.opts.verbose * 10, 10))
        self.logger.setLevel(loglevel)
        self.states = []
        self.performances = []
        try:
            with_timeout(self.opts.timeout, self.run_inner)
        except TimeoutError:
            self.states.append(nagiosplugin.state.Unknown(
                u'timeout of %is exceeded' % self.opts.timeout))
        except Exception:
            e = sys.exc_info()[1]
            self.states.append(nagiosplugin.state.Unknown(str(e)))
            if self.opts.verbose > 0:
                self.stderr += traceback.format_exc()
        try:
            self.dominant_state = reduce(
                nagiosplugin.state.reduce, self.states)
        except TypeError:
            pass
        self.exitcode = self.dominant_state.code
        return self

    def run_inner(self):
        """Perform check action."""
        msg = self.check.process_args(self.opts, self.args)
        if msg:
            raise RuntimeError(msg)
        self.check.obtain_data()
        self.states = self.check.states()
        self.performances = self.check.performances()
        if self.check.default_message():
            self.states.append(nagiosplugin.state.Ok(
                self.check.default_message()))

    def format(self):
        """Compile and format output according to Nagios 3 plugin API."""
        (first, p_processed) = self.firstline()
        long = self.longoutput().rstrip(u'\n')
        longperf = self.longperformance(p_processed)
        if longperf:
            long += u' | ' + longperf
        out = first + u'\n' + long.strip()
        if not out.endswith(u'\n'):
            out += u'\n'
        return out

    def firstline(self):
        """Return check status and performance data."""
        out = u'%s %s' % (self.check.shortname, str(self.dominant_state))
        if self.dominant_state.headline():
            out += u' - ' + self.dominant_state.headline()
        p = 0
        length = len(out) + 3
        while p < len(self.performances):
            length += len(self.performances[p]) + 1
            if length > 80:
                break
            p += 1
        if p == 0:
            return (out, 0)
        perf = u' '.join(self.performances[0:p])
        return (out + u' | ' + perf, p)

    def longoutput(self):
        """Accumulate additional output and performance lines."""
        out = self.dominant_state.longoutput()
        if self.logstream.getvalue():
            out.append(self.logstream.getvalue())
        return u'\n'.join(out)

    def longperformance(self, min_p):
        return u'\n'.join(self.performances[min_p:])

    def print_output(self, stdout=sys.stdout, stderr=sys.stderr, exit=True):
        """Emit cumulated output to `stdout` and `stderr`, and exit."""
        stdout.write(self.format())
        stderr.write(self.stderr)
        if exit:
            sys.exit(self.exitcode)
