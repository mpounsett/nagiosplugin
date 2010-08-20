#!/usr/bin/python2.6
# Example Nagios plugin to check disk usage.
# It is kept very basic to serve as tutoral example. For the tutorial, see the
# nagiosplugin documentation.
# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin
import os


class DiskCheck(nagiosplugin.Check):

   name = 'disk tutorial'
   version = '0.1'

   def __init__(self, optparser, logger):
      optparser.description = 'Check disk usage of the root partition'
      optparser.version = '0.1'
      optparser.add_option(
         '-w', '--warning', default='50', metavar='RANGE',
         help='warning threshold (default: %default%)')
      optparser.add_option(
         '-c', '--critical', default='75', metavar='RANGE',
         help='warning threshold (default: %default%)')

   def process_args(self, options, args):
      self.warning = options.warning.rstrip('%')
      self.critical = options.critical.rstrip('%')

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.usage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         '/', self.usage, '%', self.warning, self.critical, 0, 100)]

   def default_message(self):
      return '/ is %i%% full' % (self.usage)


main = nagiosplugin.Controller(DiskCheck)
if __name__ == '__main__':
   main()
