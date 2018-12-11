#!python
"""Nagios plugin to check number of logged in users."""

import argparse
import logging
import nagiosplugin
import subprocess

_log = logging.getLogger('nagiosplugin')


class Users(nagiosplugin.Resource):
    """Domain model: system logins.

    The `Users` class is a model of system aspects relevant for this
    check. It determines the logged in users and counts them.
    """

    who_cmd = 'who'

    def __init__(self):
        self.users = []
        self.unique_users = set()

    def list_users(self):
        """Return list of logged in users.

        The user list is determined by invoking an external command
        defined in `who_cmd` (default: who) and parsing its output. The
        command is expected to produce one line per user with the user
        name at the beginning.
        """
        _log.info('querying users with "%s" command', self.who_cmd)
        users = []
        try:
            p = subprocess.Popen([self.who_cmd], stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            for line in p.communicate()[0].splitlines():
                _log.debug('who output: %s', line.strip())
                users.append(line.split()[0].decode())
        except OSError:
            raise nagiosplugin.CheckError(
                'cannot determine number of users ({0} failed)'.format(
                    self.who_cmd))
        return users

    def probe(self):
        """Create check metric for user counts.

        This method returns two metrics: `total` is total number of user
        logins including users with multiple logins. `unique` counts
        only unique user id. This means that users with multiple logins
        are only counted once.
        """
        self.users = self.list_users()
        self.unique_users = set(self.users)
        return [nagiosplugin.Metric('total', len(self.users), min=0),
                nagiosplugin.Metric('unique', len(self.unique_users), min=0)]


class UsersSummary(nagiosplugin.Summary):
    """Create status line and long output.

    For the status line, the text snippets created by the contexts work
    quite well, so leave `ok` and `problem` with their default
    implementations. For the long output (-v) we wish to display *which*
    users are actually logged in. Note how we use the `resource`
    attribute in the resuls object to grab this piece of information
    from the domain model object.
    """

    def verbose(self, results):
        super(UsersSummary, self).verbose(results)
        if 'total' in results:
            return 'users: ' + ', '.join(results['total'].resource.users)


@nagiosplugin.guarded
def main():
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
    check = nagiosplugin.Check(
        Users(),
        nagiosplugin.ScalarContext('total', args.warning, args.critical,
                                   fmt_metric='{value} users logged in'),
        nagiosplugin.ScalarContext(
            'unique', args.warning_unique, args.critical_unique,
            fmt_metric='{value} unique users logged in'),
        UsersSummary())
    check.main(args.verbose, args.timeout)


if __name__ == '__main__':
    main()
