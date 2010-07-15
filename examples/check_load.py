# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin


class LoadCheck(nagiosplugin.Check):

    name = u'Load average'
    version = u'0.1'
    loadavg = '/proc/loadavg'
    cpuinfo = '/proc/cpuinfo'

    def __init__(self, op, log):
        op.description = 'Check the current system load average.'
        op.version = self.version
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
        self.log = log

    def obtain_data(self, opts, args):
        warn = opts.warning.split(u',')
        if len(warn) < 3:
            warn.extend([warn[-1], warn[-1]][0:3-len(warn)])
            self.log.info(u'extending warn thresholds=%s' % u' '.join(warn))
        crit = opts.critical.split(u',')
        if len(crit) < 3:
            crit.extend([crit[-1], crit[-1]])
            self.log.info(u'extending crit thresholds=%s' % u' '.join(crit))
        with file(self.loadavg) as f:
            line = f.readline()
            self.log.info(u'reading %s: %s' % (self.loadavg, line.strip()))
        self.load = map(float, line.split(u' ')[0:3])
        if len(self.load) != 3:
            raise ValueError(u'Cannot parse loadavg: %s' % line)
        self.data = [nagiosplugin.Measure(u'load%i' % t, self.load[i],
                                          warning=warn[i], critical=crit[i],
                                          min=0)
                     for (i, t) in [(0, 1), (1, 5), (2, 15)]]
        self.log.info(u'resulting measures: %r' % self.data)

    def performances(self):
        return [m.performance() for m in self.data]

    def states(self):
        states = [m.state() for m in self.data]
        self.log.warning(u'states: %r' % states)
        return states

    @property
    def default_message(self):
        return u'system load average is %.2f %.2f %.2f' % tuple(self.load)


if __name__ == '__main__':
    c = nagiosplugin.Controller(LoadCheck)
    c.output()
