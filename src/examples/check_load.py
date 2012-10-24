#!/usr/bin/python3.2
# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Nagios/Icinga plugin to check system load."""

import argparse
import itertools
import logging
import nagiosplugin
import re
import subprocess


class Load(nagiosplugin.Resource):
    """Domain model: system load.

    Determines the system load parameters and (optionally) cpu count.
    The `probe` method returns the three standard load average numbers.
    If `percpu` is true, the load average will be normalized.
    """

    def __init__(self, percpu=False):
        self.percpu = percpu

    def cpus(self):
        logging.info('counting cpus with "nproc"')
        cpus = int(subprocess.check_output(['nproc']))
        logging.debug('found %i cpus in total', cpus)
        return cpus

    def probe(self):
        logging.info('reading load from /proc/loadavg')
        with open('/proc/loadavg') as loadavg:
            load = loadavg.readline().split(None, 3)[0:3]
        logging.debug('raw load is %s', load)
        cpus = self.cpus() if self.percpu else 1
        load = [float(l) / cpus for l in load]
        return [nagiosplugin.Metric('load%d' % period, load[i], min=0,
                                    context='load')
                for period, i in zip([1, 5, 15], itertools.count())]


class LoadSummary(nagiosplugin.Summary):
    """Status line conveying load information.

    We specialize the `ok` method to present all three figures in one
    handy tagline. In case of problems, the single-load texts from the
    contexts work well.
    """

    def __init__(self, percpu):
        self.percpu = percpu

    def ok(self, results):
        qualifier = 'per cpu ' if self.percpu else ''
        return 'loadavg %sis %s' % (qualifier, ', '.join(
            str(results[r].metric) for r in ['load1', 'load5', 'load15']))


@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
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
        nagiosplugin.ScalarContext('load', args.warning, args.critical),
        LoadSummary(args.percpu))
    check.main(verbose=args.verbose)

if __name__ == '__main__':
    main()
