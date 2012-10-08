#!/usr/bin/python3.2

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
        users = []
        for line in subprocess.check_output([self.who_cmd]).splitlines():
            users.append(line.split()[0].decode())
        return users

    def __call__(self):
        self.users = self.list_users()
        self.unique_users = set(self.users)
        return [nagiosplugin.Metric('total', len(self.users), min=0,
                                    description='total user count'),
                nagiosplugin.Metric('unique', len(self.unique_users), min=0,
                                    description='unique user count')]


class UsersSummary(nagiosplugin.Summary):

    def ok(self, results):
        return '%s users total (%s unique)' % (
            results['total'].value, results['unique'].value)

    def verbose(self, results):
        return 'users: ' + ', '.join(
            str(u) for u in results['total'].resource.users)


@nagiosplugin.managed
def main(runtime):
    argp = argparse.ArgumentParser()
    argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                      help='warning if total user count is outside RANGE'),
    argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                      help='critical is total user count is outside RANGE')
    argp.add_argument('-W', '--warning-unique', metavar='RANGE', default='',
                      help='warning if unique user count is outside RANGE')
    argp.add_argument('-C', '--critical-unique', metavar='RANGE', default='',
                      help='critical if unique user count is outside RANGE')
    argp.add_argument('-v', '--verbose', action='append_const', const='v',
                      help='increase output verbosity (use up to 3 times)')
    args = argp.parse_args()
    runtime.execute(nagiosplugin.Check(
        Users(), UsersSummary(),
        nagiosplugin.ScalarContext(['total'], args.warning, args.critical),
        nagiosplugin.ScalarContext(['unique'], args.warning_unique,
                                   args.critical_unique)),
        verbose=args.verbose)

if __name__ == '__main__':
    main()
