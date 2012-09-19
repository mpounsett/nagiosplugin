#!/usr/bin/python3.2

from nagiosplugin import Check, Resource, Metric, ScalarContext
import argparse


class Load(Resource):

    def __init__(self, procfile='/proc/loadavg'):
        self.procfile = procfile

    def inspect(self):
        with open(self.procfile) as loadavg:
            load1, load5, load15, _rest = loadavg.readline().split(None, 3)
        return [
            Metric('load1', float(load1), minimum=0),
            Metric('load5', float(load5), minimum=0),
            Metric('load15', float(load15), minimum=0),
        ]


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('-w', '--warning')
    argp.add_argument('-c', '--critical')
    args = argp.parse_args()
    c = Check(Load(),
              ScalarContext(['load1', 'load5', 'load15'],
                            args.warning, args.critical),
             )
    c.main()

if __name__ == '__main__':
    main()
