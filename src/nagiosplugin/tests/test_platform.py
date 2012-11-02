# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.platform import with_timeout
from nagiosplugin.error import Timeout
import unittest
import time


class PlatformTest(unittest.TestCase):

    def test_timeout(self):
        with self.assertRaises(Timeout):
            with_timeout(1, time.sleep, 2)
