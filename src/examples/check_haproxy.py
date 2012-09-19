#!/usr/bin/python3.2

from __future__ import print_function, unicode_literals
from nagiosplugin import Resource, Metric, Check, ScalarContext
import re
import argparse
import numpy


class HAProxy(Resource):

    r_logline = re.compile(r'haproxy.*: [0-9.:]+ \[\S+\] .* \d+/\d+/\d+/\d+/'
                           '(\d+) (\d\d\d) \d+ .* \d+/\d+/\d+/\d+/\d+ \d+/(\d+) ')

    def __init__(self, logfile):
        self.logfile = logfile

    def parse(self):
        with open(self.logfile) as lf:
            for line in lf:
                match = self.r_logline.search(line)
                if not match:
                    continue
                tt, stat, ql = match.groups()
                err = not (stat.startswith('2') or stat.startswith('3'))
                yield int(tt), err, int(ql)

    def inspect(self):
        d = numpy.fromiter(self.parse(),
                           dtype=[('tt', numpy.int32), ('err', numpy.uint16),
                                  ('qlen', numpy.uint16)]
                          )
        requests = len(d['err'])
        error_rate = requests and float(numpy.sum(d['err'])) / requests or 0.0
        return [
            Metric('ttot mean', numpy.mean(d['tt']), 's', 0),
            Metric('ttot std', numpy.std(d['tt']), 's', minimum=0),
            Metric('requests', requests, minimum=0),
            Metric('error rate', error_rate, minimum=0),
            Metric('qlen mean', numpy.mean(d['qlen']), minimum=0),
            Metric('qlen std', numpy.std(d['qlen']), minimum=0)]


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('logfile')
    argp.add_argument('--tw', '--ttot-warning', metavar='RANGE')
    argp.add_argument('--tc', '--ttot-critical', metavar='RANGE')
    argp.add_argument('--ew', '--errors-warning', metavar='RANGE')
    argp.add_argument('--ec', '--errors-critical', metavar='RANGE')
    argp.add_argument('--qw', '--qlen-warning', metavar='RANGE')
    argp.add_argument('--qc', '--qlen-critical', metavar='RANGE')
    args = argp.parse_args()
    c = Check(HAProxy(args.logfile),
              ScalarContext(['ttot mean'], args.tw, args.tc),
              ScalarContext(['error rate'], args.ew, args.ec),
              ScalarContext(['qlen mean'], args.qw, args.qc),
              ScalarContext(['ttot std', 'requests', 'qlen std']))
    c.main()

if __name__ == '__main__':
    main()
