#!/usr/bin/python3.2

from nagiosplugin import Check, Resource, Metric, ScalarContext, Summary
from nagiosplugin.state import Ok
import argparse


class Load(Resource):

    def __init__(self, procfile='/proc/loadavg'):
        self.procfile = procfile

    def __call__(self):
        with open(self.procfile) as loadavg:
            load1, load5, load15, _rest = loadavg.readline().split(None, 3)
        return [
            Metric('load1', float(load1), minimum=0,
                   description='1min loadavg'),
            Metric('load5', float(load5), minimum=0,
                   description='5min loadavg'),
            Metric('load15', float(load15), minimum=0,
                   description='15min loadavg'),
        ]


class LoadSummary(Summary):

    def brief(self, results):
        if results.worst_state == Ok():
            return 'loadavg is %s' % ', '.join(
                str(results[r].metric) for r in ['load1', 'load5', 'load15'])
        return super(LoadSummary, self).brief(results)


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-w', '--warning')
    argp.add_argument('-c', '--critical')
    args = argp.parse_args()
    c = Check(Load(),
              ScalarContext(['load1', 'load5', 'load15'],
                            args.warning, args.critical),
              LoadSummary())
    c.main()

if __name__ == '__main__':
    main()
