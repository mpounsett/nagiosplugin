#!/usr/bin/python3.2
# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import argparse
import logging
import nagiosplugin
import subprocess


class Users(nagiosplugin.Resource):

    def __init__(self, who_cmd='who'):
        self.who_cmd = who_cmd
        self.users = []
        self.unique_users = set()

    def list_users(self):
        logging.info('querying users with "%s" command', self.who_cmd)
        users = []
        try:
            for line in subprocess.check_output([self.who_cmd]).splitlines():
                logging.debug('who output: %s', line.strip())
                users.append(line.split()[0].decode())
        except OSError:
            raise nagiosplugin.CheckError(
                'cannot determine number of users ({} failed)'.format(
                    self.who_cmd))
        return users

    def survey(self):
        self.users = self.list_users()
        self.unique_users = set(self.users)
        return [nagiosplugin.Metric('total', len(self.users), min=0,
                                    fmt='{value} users logged in'),
                nagiosplugin.Metric('unique', len(self.unique_users), min=0,
                                    fmt='{value} unique users logged in')]


class UsersSummary(nagiosplugin.Summary):

    def verbose(self, results):
        return 'users: ' + ', '.join(results['total'].resource.users)


@nagiosplugin.managed
def main(runtime):
    argp = argparse.ArgumentParser()
    argp.add_argument('-w', '--warning', metavar='RANGE',
                      help='warning if total user count is outside RANGE'),
    argp.add_argument('-c', '--critical', metavar='RANGE',
                      help='critical is total user count is outside RANGE')
    argp.add_argument('-W', '--warning-unique', metavar='RANGE',
                      help='warning if unique user count is outside RANGE')
    argp.add_argument('-C', '--critical-unique', metavar='RANGE',
                      help='critical if unique user count is outside RANGE')
    argp.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase output verbosity (use up to 3 times)')
    argp.add_argument('-t', '--timeout', default=10,
                      help='abort execution after TIMEOUT seconds')
    args = argp.parse_args()
    runtime.execute(nagiosplugin.Check(
        Users(), UsersSummary(),
        nagiosplugin.ScalarContext(['total'], args.warning, args.critical),
        nagiosplugin.ScalarContext(['unique'], args.warning_unique,
                                   args.critical_unique)),
        verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()
