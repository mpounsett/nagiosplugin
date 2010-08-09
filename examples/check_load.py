# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin
import re


class LoadCheck(nagiosplugin.Check):

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

    @property
    def name(self):
        return u'Load average'

    @property
    def version(self):
        return u'0.1'

    def process_args(self, opts, args):
        nagiosplugin.Check.process_args(self, opts, args)
        self.warn = opts.warning.split(u',')
        self.crit = opts.critical.split(u',')
        self.percpu = opts.percpu

    def obtain_data(self):
        with file(self.loadavg) as f:
            line = f.readline()
            self.log.info(u'%s: %s' % (self.loadavg, line.strip()))
        self.load = map(float, line.split(u' ')[0:3])
        if self.percpu:
            cpus = self._count_cpus()
            self.load = [l / cpus for l in self.load]
        if len(self.load) != 3:
            raise ValueError(u'Cannot parse loadavg: %s' % line)
        self.data = nagiosplugin.Measure.array(
                [u'load1', u'load5', u'load15'], self.load,
                warnings=self.warn, criticals=self.crit, minimums=[0])
        self.log.info(u'measures: %r' % self.data)

    def _count_cpus(self):
        cpus = 0
        r_processor_start = re.compile(r'^processor\s*:\s*[0-9]+$')
        with file(self.cpuinfo) as f:
            for line in f:
                if r_processor_start.match(line):
                    cpus += 1
                self.log.debug(u'%s (cpus=%i): %s' % (
                    self.cpuinfo, cpus, line.strip()))
        if cpus == 0:
            raise ValueError(u'cannot parse /proc/cpuinfo contents: '
                             u'no processors found')
        self.log.info(u'%s: %i cpus' % (self.cpuinfo, cpus))
        return cpus

    def performances(self):
        return [m.performance() for m in self.data]

    def states(self):
        states = [m.state() for m in self.data]
        self.log.warning(u'states: %r' % states)
        return states

    def default_message(self):
        return u'system load average is %.2f %.2f %.2f' % tuple(self.load)


main = nagiosplugin.Controller(LoadCheck)
if __name__ == '__main__':
    main()
