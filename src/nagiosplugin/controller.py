# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import cStringIO
import nagiosplugin.state
import optparse
import sys
import traceback


class Controller(object):

    def __init__(self, check_cls, argv=None):
        self.stdout = u''
        self.stderr = u''
        self.exitcode = 0
        self.optparser = optparse.OptionParser(add_help_option=False)
        self.optparser.add_option(u'-h', u'--help', action='store_true',
                help='show this help message and exit')
        self.check = check_cls(self.optparser)
        # XXX: subclass OptionParser and handle help, version and error
        # differently
        (self.opts, self.args) = self.optparser.parse_args(argv)
        # XXX: this should go into the OptionParser subclass
        if self.opts.help:
            io = cStringIO.StringIO()
            self.optparser.print_help(io)
            self.stderr = io.getvalue()
        else:
            self.run()

    def run(self):
        self.states = []
        self.performances = []
        try:
            self.check.obtain_data(self.opts, self.args)
            self.states = self.check.states()
            self.performances = self.check.performances()
            if self.check.default_message:
                self.states.append(nagiosplugin.state.Ok(
                    self.check.default_message))
        except Exception as e:
            self.states.append(nagiosplugin.state.Unknown(str(e)))
            self.stderr += traceback.format_exc() + u'\n'
        try:
            self.dominant_state = reduce(nagiosplugin.state.reduce, self.states)
        except TypeError:
            self.dominant_state = nagiosplugin.state.Unknown(u'no output')
        self.exitcode = self.dominant_state.code
        self.format()

    def format(self):
        (first, p_processed) = self.firstline()
        long = u' | '.join(filter(bool, (
            self.longoutput(), self.longperformance(p_processed))))
        self.stdout += first + u'\n' + long
        if not self.stdout.endswith(u'\n'):
            self.stdout += u'\n'

    def firstline(self):
        out = u'%s %s' % (self.check.shortname, str(self.dominant_state))
        if self.dominant_state.headline():
            out += u' - ' + self.dominant_state.headline()
        p = 0
        length = len(out) + 3
        while p < len(self.performances) and length <= 80:
            length += len(self.performances) + 1
            p += 1
        if p == 0:
            return (out, p)
        perf = u' '.join(self.performances[0:p])
        return (out + u' | ' + perf, p)

    def longoutput(self):
        # XXX: insufficient
        return ''

    def longperformance(self, min_p):
        return u'\n'.join(self.performances[min_p:])

    def output(self, stdout=sys.stdout, stderr=sys.stderr, exit=True):
        stdout.write(self.stdout)
        stderr.write(self.stderr)
        if exit:
            sys.exit(self.exitcode)
        return self.exitcode
