#!/usr/bin/python3.2
# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import argparse
import itertools
import nagiosplugin
import numpy
import re


class HAProxyLog(nagiosplugin.Resource):

    r_logline = re.compile(
        r'haproxy.*: [0-9.:]+ \[\S+\] .* \d+/\d+/\d+/\d+/(\d+) (\d\d\d) ')

    def __init__(self, logfile, statefile, percentiles):
        self.logfile = logfile
        self.statefile = statefile
        self.percentiles = percentiles

    def parse_log(self):
        cookie = nagiosplugin.Cookie(self.statefile)
        with nagiosplugin.LogTail(self.logfile, cookie) as lf:
            for line in lf:
                match = self.r_logline.search(line)
                if not match:
                    continue
                tt, stat = match.groups()
                err = not (stat.startswith('2') or stat.startswith('3'))
                yield int(tt), err

    def probe(self):
        d = numpy.fromiter(self.parse_log(),
                           dtype=[('tt', numpy.int32), ('err', numpy.uint16)])
        requests = len(d['err'])
        metrics = []
        if requests:
            for pct in self.percentiles:
                metrics.append(nagiosplugin.Metric(
                    'ttot%s' % pct, numpy.percentile(
                        d['tt'], int(pct)) / 1000.0, 's', 0))
        error_rate = (100 * numpy.sum(d['err'] / requests)
                      if requests else 0)
        metrics += [nagiosplugin.Metric('error_rate', error_rate, '%', 0, 100),
                    nagiosplugin.Metric('request_total', requests, min=0,
                                        context='default')]
        return metrics


def parse_args():
    argp = argparse.ArgumentParser()
    argp.add_argument('logfile')
    argp.add_argument('--ew', '--error-warning', metavar='RANGE', default='')
    argp.add_argument('--ec', '--error-critical', metavar='RANGE', default='')
    argp.add_argument('--tw', '--ttot-warning', metavar='RANGE[,RANGE,...]',
                      type=nagiosplugin.MultiArg, default='')
    argp.add_argument('--tc', '--ttot-critical', metavar='RANGE[,RANGE,...]',
                      type=nagiosplugin.MultiArg, default='')
    argp.add_argument('-p', '--percentiles', metavar='N,N,...', default='50,95',
                      help='check Nth percentiles of total time '
                      '(default: %(default)s)')
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase output verbosity (use up to 3 times)')
    argp.add_argument('-t', '--timeout', default=30,
                      help='abort execution after TIMEOUT seconds')
    argp.add_argument('-s', '--state-file', default='check_haproxy_log.state',
                      help='cookie file to save last log file position '
                      '(default: "%(default)s")')
    return argp.parse_args()


@nagiosplugin.guarded
def main():
    args = parse_args()
    percentiles = args.percentiles.split(',')
    check = nagiosplugin.Check(
        HAProxyLog(args.logfile, args.state_file, percentiles),
        nagiosplugin.ScalarContext('error_rate', args.ew, args.ec))
    for pct, i in zip(percentiles, itertools.count()):
        check.add(nagiosplugin.ScalarContext(
            'ttot%s' % pct, args.tw[i], args.tc[i],
            'total time (%s.pct) is {valueunit}' % pct))
    check.main(args.verbose, args.timeout)

if __name__ == '__main__':
    main()
