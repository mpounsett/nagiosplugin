#!/usr/bin/python3.2

from nagiosplugin import Check, Resource, Metric, ScalarContext, Summary
from nagiosplugin.state import Ok
import argparse
import re


class Load(Resource):

    def __init__(self, percpu=False):
        self.percpu = percpu
        if percpu:
            self.cpus = self.count_cpus()
        else:
            self.cpus = 1

    def count_cpus(self):
        cpus = 0
        with open('/proc/cpuinfo') as cpuinfo:
            for line in cpuinfo:
                if re.match(r'^processor\s*:\s+\d+$', line):
                    cpus += 1
        return cpus

    def __call__(self):
        with open('/proc/loadavg') as loadavg:
            load = loadavg.readline().split(None, 3)
            del load[3:]
        load = [float(l) / self.cpus for l in load]
        return [
            Metric('load1', load[0], minimum=0,
                   description='1min loadavg'),
            Metric('load5', load[1], minimum=0,
                   description='5min loadavg'),
            Metric('load15', load[2], minimum=0,
                   description='15min loadavg'),
        ]


class LoadSummary(Summary):

    def __init__(self, percpu=False):
        self.percpu = percpu

    def brief(self, results):
        if results.worst_state == Ok():
            qualifier = 'per cpu ' if self.percpu else ''
            return 'loadavg %sis %s' % (
                qualifier, ', '.join(
                str(results[r].metric) for r in ['load1', 'load5', 'load15']))
        return super(LoadSummary, self).brief(results)


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-w', '--warning')
    argp.add_argument('-c', '--critical')
    argp.add_argument('-r', '--percpu', action='store_true', default=False)
    args = argp.parse_args()
    c = Check(Load(args.percpu),
              ScalarContext(['load1', 'load5', 'load15'],
                            args.warning, args.critical),
              LoadSummary(args.percpu))
    c.main()

if __name__ == '__main__':
    main()
