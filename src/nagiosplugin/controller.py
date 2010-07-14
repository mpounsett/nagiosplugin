# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import cStringIO
import logging
import nagiosplugin.state
import optparse
import os
import signal
import sys
import traceback


class TimeoutError(RuntimeError):
    pass


class Controller(object):

    def __init__(self, check_cls, argv=None):
        """Initialize controller and check instance.

        The check instance is given as class `check_cls` and called with the
        pre-populated option parser and a logger instance.
        """
        self.prepare()
        self.check = check_cls(self.optparser, self.logger)
        self.stderr = u''
        self.exitcode = 0
        self.states = []
        self.performances = []
        self.dominant_state = nagiosplugin.state.Unknown(u'no output')
        # XXX: subclass OptionParser and handle help, version and error
        # differently
        (self.opts, self.args) = self.optparser.parse_args(argv)
        # XXX: this should go into the OptionParser subclass
        if self.opts.help:
            io = cStringIO.StringIO()
            self.optparser.print_help(io)
            self.stderr = io.getvalue()
        else:
            self.setup_logger()
            self.run_with_timeout()

    def prepare(self):
        """Prepare ancillary objects: option parser and logger."""
        self.optparser = optparse.OptionParser(add_help_option=False)
        self.optparser.add_option(u'-h', u'--help', action='store_true',
                help='show this help message and exit')
        self.optparser.add_option(u'-v', u'--verbose', action='count',
                default=0, help='increase output verbosity (up to 3 times)')
        self.optparser.add_option(u'-t', u'--timeout', metavar=u'TIMEOUT',
                default=15, type='int',
                help=u'abort execution after TIMEOUT seconds '
                '(default: %default)')
        self.logger = logging.getLogger(u'nagiosplugin')
        self.logger.setLevel(logging.DEBUG)
        self.logstream = cStringIO.StringIO()
        handler = logging.StreamHandler(self.logstream)
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def setup_logger(self):
        """Adjust logging level according to verbose option."""
        level = max((40 - self.opts.verbose * 10, 10))
        self.logger.setLevel(level)

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutError(u'timeout exceeded')

    def run_with_timeout(self):
        """Interrupt check action if it runs longer than the timeout."""
        self.states = []
        self.performances = []
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(self.opts.timeout)
            self.run()
            signal.alarm(0)
        except TimeoutError:
            self.states.append(nagiosplugin.state.Unknown(
                u'timeout of %is exceeded' % self.opts.timeout))
        except Exception as e:
            self.states.append(nagiosplugin.state.Unknown(str(e)))
            self.stderr += traceback.format_exc() + u'\n'
        try:
            self.dominant_state = reduce(nagiosplugin.state.reduce, self.states)
        except TypeError:
            pass
        self.exitcode = self.dominant_state.code

    def run(self):
        """Perform check action."""
        error = self.check.check_args(self.opts, self.args)
        if error:
            self.optparser.error(error)
        self.check.obtain_data(self.opts, self.args)
        self.states = self.check.states()
        self.performances = self.check.performances()
        if self.check.default_message:
            self.states.append(nagiosplugin.state.Ok(
                self.check.default_message))

    def format(self):
        (first, p_processed) = self.firstline()
        long = self.longoutput().rstrip(u'\n')
        longperf = self.longperformance(p_processed)
        if longperf:
            long += u' | ' + longperf
        out = first + u'\n' + long.strip()
        if not out.endswith(u'\n'):
            out += u'\n'
        return out

    def output(self, stdout=sys.stdout, stderr=sys.stderr, exit=True):
        stdout.write(self.format())
        stderr.write(self.stderr)
        if exit:
            sys.exit(self.exitcode)
        return self.exitcode

    def firstline(self):
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
        out = self.dominant_state.longoutput()
        if self.logstream.getvalue():
            out.append(self.logstream.getvalue())
        return u'\n'.join(out)

    def longperformance(self, min_p):
        return u'\n'.join(self.performances[min_p:])
