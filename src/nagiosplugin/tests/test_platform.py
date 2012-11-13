# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.platform import with_timeout
import nagiosplugin
import unittest
import time


class PlatformTest(unittest.TestCase):

    def test_timeout(self):
        with self.assertRaises(nagiosplugin.Timeout):
            with_timeout(1, time.sleep, 2)
