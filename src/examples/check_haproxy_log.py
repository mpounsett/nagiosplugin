#!/usr/bin/python3.2

import argparse
import pprint
import collections
import itertools
import logging
import nagiosplugin
import numpy
import re


class HAProxyLog(nagiosplugin.Resource):

    r_logline = re.compile(
        r'haproxy.*: [0-9.:]+ \[\S+\] .* \d+/\d+/\d+/\d+/'
        r'(\d+) (\d\d\d) \d+ .* \d+/\d+/\d+/\d+/\d+ \d+/(\d+) ')

    def __init__(self, logfile, percentiles):
        self.logfile = logfile
        self.percentiles = percentiles

    def parse(self):
        with open(self.logfile) as lf:
            for line in lf:
                match = self.r_logline.search(line)
                if not match:
                    continue
                tt, stat, ql = match.groups()
                err = not (stat.startswith('2') or stat.startswith('3'))
                yield int(tt), err, int(ql)

    def __call__(self):
        d = numpy.fromiter(self.parse(),
                           dtype=[('tt', numpy.int32), ('err', numpy.uint16),
                                  ('qlen', numpy.uint16)]
                          )
        requests = len(d['err'])
        error_rate = (100.0 * numpy.sum(d['err'] / requests)
                      if requests else 0.0)
        metrics = [nagiosplugin.Metric('request count', requests, min=0),
                   nagiosplugin.Metric('error_rate', error_rate, '%', 0, 100)]
        for pct in self.percentiles:
            metrics.append(nagiosplugin.Metric(
                'ttot%d' % pct, numpy.percentile(d['tt'], pct) / 1000, 's', 0,
                description='total request time (%d.percentile)' % pct))
            metrics.append(nagiosplugin.Metric(
                'qlen%d' % pct, numpy.percentile(d['qlen'], pct), min=0,
                description=('queue length (%d.percentile)' % pct)))
        return metrics


def parse_args():
    argp = argparse.ArgumentParser()
    argp.add_argument('logfile')
    argp.add_argument('--ew', '--error-warning', metavar='RANGE', default='')
    argp.add_argument('--ec', '--error-critical', metavar='RANGE', default='')
    argp.add_argument('--tw', '--ttot-warning', metavar='RANGE',
                      type=nagiosplugin.MultiArg, default='')
    argp.add_argument('--tc', '--ttot-critical', metavar='RANGE',
                      type=nagiosplugin.MultiArg, default='')
    argp.add_argument('--qw', '--qlen-warning', metavar='RANGE',
                      type=nagiosplugin.MultiArg, default='')
    argp.add_argument('--qc', '--qlen-critical', metavar='RANGE',
                      type=nagiosplugin.MultiArg, default='')
    argp.add_argument('-p', '--percentiles', default='50,95')
    argp.add_argument('-v', '--verbose', action='append_const', const='v',
                      help='increase output verbosity (use up to 3 times)')
    return argp.parse_args()


@nagiosplugin.managed
def main(runtime):
    args = parse_args()
    runtime.verbose = args.verbose
    percentiles = list(map(int, args.percentiles.split(',')))
    check = nagiosplugin.Check(
        HAProxyLog(args.logfile, percentiles),
        nagiosplugin.ScalarContext(['error_rate'], args.ew, args.ec),
        nagiosplugin.ScalarContext(['request count']))
    for pct, i in zip(percentiles, itertools.count()):
        check.add(nagiosplugin.ScalarContext(
            ['ttot%d' % pct], args.tw[i], args.tc[i]))
        check.add(nagiosplugin.ScalarContext(
            ['qlen%d' % pct], args.qw[i], args.qc[i]))
    runtime.execute(check)

if __name__ == '__main__':
    main()
