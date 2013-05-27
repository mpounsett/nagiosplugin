# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.platform import with_timeout
import nagiosplugin
import time

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class PlatformTest(unittest.TestCase):

    def test_timeout(self):
        with self.assertRaises(nagiosplugin.Timeout):
            with_timeout(1, time.sleep, 2)
