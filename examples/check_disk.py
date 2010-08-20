# Example Nagios plugin to check disk usage.
# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin
import os


class DiskCheck(nagiosplugin.Check):

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.diskusage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         'diskusage', self.diskusage, '%', '0:50', '0:75', 0, 100)]

   def default_message(self):
      return 'root partition is %i%% full' % (self.diskusage)


main = nagiosplugin.Controller(DiskCheck)
if __name__ == '__main__':
   main()
