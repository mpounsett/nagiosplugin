#!python
"""haproxy log check for request time and error rate.

This check shows an advanced programming technique: we allow the user to
define the thresholds dynamically. You can specify a list of conditions
like:

* the N1th percentile of t_tot must match range R1
* the N2th percentile of t_tot must match range R2

Implementation-wise, the command line parameter "percentiles" is used to
compute both metric and context names. The default is to check for the
50th and 95th percentile. The `MultiArg` class is used to specify sets
of thresholds. It has the nice property to fill up missing values so the
user is free in how many thresholds he specifies.
"""

import argparse
import itertools
import nagiosplugin
import numpy
import re


class HAProxyLog(nagiosplugin.Resource):
    """haproxy.log parser.

    Goes through a haproxy log file and extracts total request time
    (t_tot) and error status for each request. The error status is used
    to compute the error rate.
    """

    r_logline = re.compile(
        r'haproxy.*: [0-9.:]+ \[\S+\] .* \d+/\d+/\d+/\d+/(\d+) (\d\d\d) ')

    def __init__(self, logfile, statefile, percentiles):
        self.logfile = logfile
        self.statefile = statefile
        self.percentiles = percentiles

    def parse_log(self):
        """Yields ttot and error status for each log line."""
        cookie = nagiosplugin.Cookie(self.statefile)
        with nagiosplugin.LogTail(self.logfile, cookie) as lf:
            for line in lf:
                match = self.r_logline.search(line.decode())
                if not match:
                    continue
                ttot, stat = match.groups()
                err = not (stat.startswith('2') or stat.startswith('3'))
                yield int(ttot), err

    def probe(self):
        """Computes error rate and t_tot percentiles."""
        d = numpy.fromiter(self.parse_log(), dtype=[
            ('ttot', numpy.int32), ('err', numpy.uint16)])
        requests = len(d['err'])
        metrics = []
        if requests:
            for pct in self.percentiles:
                metrics.append(nagiosplugin.Metric(
                    'ttot%s' % pct, numpy.percentile(
                        d['ttot'], int(pct)) / 1000.0, 's', 0))
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
    argp.add_argument('-p', '--percentiles', metavar='N,N,...',
                      default='50,95', help='check Nth percentiles of '
                      'total time (default: %(default)s)')
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
