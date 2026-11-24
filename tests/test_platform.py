import time

import nagiosplugin
from nagiosplugin.platform import with_timeout

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class PlatformTest(unittest.TestCase):

    def test_timeout(self):
        with self.assertRaises(nagiosplugin.Timeout):
            with_timeout(1, time.sleep, 2)
