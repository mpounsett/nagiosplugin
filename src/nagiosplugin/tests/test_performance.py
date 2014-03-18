# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.performance import Performance

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class PerformanceTest(unittest.TestCase):

    def test_normal_label(self):
        self.assertEqual('d=10', str(Performance('d', 10)))

    def test_label_quoted(self):
        self.assertEqual("'d d'=10", str(Performance('d d', 10)))

    def test_label_must_not_contain_quotes(self):
        with self.assertRaises(RuntimeError):
            str(Performance("d'", 10))

    def test_label_must_not_contain_equals(self):
        with self.assertRaises(RuntimeError):
            str(Performance("d=", 10))
