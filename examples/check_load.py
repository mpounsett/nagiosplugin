# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin


class LoadCheck(nagiosplugin.Check):

    name = u'Load average'

    def __init__(self, op):
        op.description = 'Check the current system load average.'
        op.add_option(u'-w', u'--warning', metavar=u'RANGES', default=u'1',
                help=u'warning if load<n> is out of RANGE<n> '
                u'(default: %default)')
        op.add_option(u'-c', u'--critical', metavar=u'RANGES', default=u'2',
                help=u'critical if load<n> is out of RANGE<n> '
                u'(default: %default)')
        op.add_option(u'-r', u'--percpu', action='store_true',
                help=u'divide the load averages by the number of CPUs')
        op.epilog = u"""\
For --warning and --critical, either three comma separated range specifications
(1, 5, 15 minutes) or one range specification covering all are accepted."""

    def obtain_load(self):
        with file('/proc/loadavg') as f:
            line = f.readline()
        return map(float, line.split(u' ')[0:3])

    def measure(self, opts, args):
        warn = opts.warning.split(u',')
        if len(warn) < 3:
            warn.extend([warn[-1], warn[-1]])
        crit = opts.critical.split(u',')
        if len(crit) < 3:
            crit.extend([crit[-1], crit[-1]])
        self.load = self.obtain_load()
        return [nagiosplugin.Measure(u'load%i' % t,
                                     self.load[i], warn[i], crit[i])
                for (i, t) in [(0, 1), (1, 5), (2, 15)]]

    @property
    def default_message(self):
        return u'system load average is %.2f %.2f %.2f' % tuple(self.load)


if __name__ == '__main__':
    c = nagiosplugin.Controller(LoadCheck)
    c.output()
