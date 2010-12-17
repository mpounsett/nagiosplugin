#!/usr/bin/python
# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin
import subprocess


class UsersCheck(nagiosplugin.Check):
    """Very simple Nagios check plugin to demonstrate basic library usage."""

    name = u'users'
    version = u'0.1'

    def __init__(self, optp, logger):
        """Set up options."""
        optp.description = u'Check number of users logged into the system.'
        optp.add_option(u'-w', u'--warning', metavar=u'RANGE',
                        help=u'set WARNING status if number of logged in users '
                        u'does not match RANGE',
                        default=u'')
        optp.add_option(u'-c', u'--critical', metavar=u'RANGE',
                        help=u'set CRITICAL status if number of logged in users '
                        u'does not match RANGE',
                        default=u'')

    def process_args(self, options, arguments):
        """Pull in parsed options and arguments with optional checking."""
        (self.warn, self.crit) = (options.warning, options.critical)

    def obtain_data(self):
        cmd = 'who -q'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env={})
        (stdout, stderr) = p.communicate()
        if stderr or p.returncode > 0:
            raise RuntimeError(u'command "%s" failed: %s' % (cmd, stderr))
        firstline = stdout.split(u'\n')[0]
        self.count = len(firstline.split())
        self.measures = [nagiosplugin.Measure(
            u'users', self.count, warning=self.warn, critical=self.crit,
            minimum=0)]

    def default_message(self):
        return u'%i users' % self.count


main = nagiosplugin.Controller(UsersCheck)
if __name__ == '__main__':
    main()
