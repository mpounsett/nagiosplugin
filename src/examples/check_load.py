#!/usr/bin/python3.2

import argparse
import itertools
import logging
import nagiosplugin
import re


class Load(nagiosplugin.Resource):

    def __init__(self, percpu=False):
        self.percpu = percpu

    def cpus(self):
        if not self.percpu:
            return 1
        cpus = 0
        logging.info('counting cpus in /proc/cpuinfo')
        with open('/proc/cpuinfo') as cpuinfo:
            for line in cpuinfo:
                if re.match(r'^processor\s*:\s+\d+$', line):
                    logging.debug('found cpu line match %s', line.strip())
                    cpus += 1
        logging.debug('found %i cpus in total', cpus)
        return cpus

    def survey(self):
        logging.info('reading load from /proc/loadavg')
        with open('/proc/loadavg') as loadavg:
            load = loadavg.readline().split(None, 3)
        del load[3:]
        logging.debug('raw load is %s', load)
        cpus = self.cpus()
        load = [float(l) / cpus for l in load]
        return [nagiosplugin.Metric('load%d' % period, load[i], min=0,
                                    context='load')
                for period, i in zip([1, 5, 15], itertools.count())]


class LoadSummary(nagiosplugin.Summary):

    def __init__(self, percpu):
        self.percpu = percpu

    def ok(self, results):
        qualifier = 'per cpu ' if self.percpu else ''
        return 'loadavg %sis %s' % (qualifier, ', '.join(
            str(results[r].metric) for r in ['load1', 'load5', 'load15']))


@nagiosplugin.managed
def main(runtime):
    argp = argparse.ArgumentParser()
    argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                      help='return warning if load is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                      help='return critical if load is outside RANGE')
    argp.add_argument('-r', '--percpu', action='store_true', default=False)
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase output verbosity (use up to 3 times)')
    args = argp.parse_args()
    check = nagiosplugin.Check(
        Load(args.percpu),
        LoadSummary(args.percpu),
        nagiosplugin.ScalarContext('load', args.warning, args.critical))
    runtime.execute(check, verbose=args.verbose)

if __name__ == '__main__':
    main()
