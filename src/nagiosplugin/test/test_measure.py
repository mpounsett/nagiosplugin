# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
import nagiosplugin.test
import nagiosplugin.measure
from nagiosplugin.measure import Measure


class MeasureTest(unittest.TestCase):

    def test_value_outside_minmax(self):
        self.assertRaises(ValueError, Measure,
                u'm1', 10, minimum=20)
        self.assertRaises(ValueError, Measure,
                u'm2', 10, maximum=0)

    def test_ok(self):
        m = Measure(u'm1', 8, warning=u'8', critical=u'9.4')
        self.assertEqual(u'OK', str(m.state()))

    def test_warn(self):
        m = Measure(u'm1', 9, u's', warning=u'8', critical=u'9.4')
        s = m.state()
        self.assertEqual(u'WARNING', str(s))
        self.assertEqual(u'm1 value 9s exceeds warning range 8',
                         s.headline())

    def test_crit(self):
        m = Measure(u'm1', 9.5, u's', warning=u'8', critical=u'9.4')
        s = m.state()
        self.assertEqual(u'CRITICAL', str(s))
        self.assertEqual(u'm1 value 9.5s exceeds critical range 9.4',
                         s.headline())

    def test_performance(self):
        m = Measure(u'm2', 75, u'MB', warning=u'33:80',
                            critical=u'31:82', minimum=10, maximum=100)
        self.assertEqual(u'm2=75MB;33:80;31:82;10;100',
                         m.performance())

    def test_short_performance(self):
        m = Measure(u'm3', 4)
        self.assertEqual(u'm3=4', m.performance())

    def test_performance_show_zero_min(self):
        m = Measure(u'm4', 15, u's', minimum=0)
        self.assertEqual(u'm4=15s;;;0', m.performance())

    def test_repr(self):
        m = Measure(u'm5', 16.1, u'kB', '10:16', '32', 0, 4096)
        self.assertEqual(u"Measure(u'm5', 16.1, u'kB', Range('10:16'), "
                         u"Range('32'), 0, 4096)",
                         repr(m))

    def test_eq(self):
        self.assert_(
                Measure(u'name', 42, u'unit', u'0:100', u'0:200', 0, 200) ==
                Measure(u'name', 42, u'unit', u'0:100', u'0:200', 0, 200),
                u'Two Measures with same values should be equal')

    def test_fill1(self):
        self.assertEqual([1], nagiosplugin.measure._fill(1, [1]))

    def test_fill4(self):
        self.assertEqual([2, 3, 3, 3], nagiosplugin.measure._fill(4, [2, 3]))

    def test_fill_already_larger(self):
        self.assertEqual([1, 2, 3], nagiosplugin.measure._fill(2, [1, 2, 3]))

    def test_array(self):
        m = Measure.array(
                2, [u'm1', u'm2'], [1, 2], [u'u1', u'u2'], [u'0:1', u'0:2'],
                [u'0:2', u'0:3'], [0, 0], [10, 20])
        self.assertEqual([
            Measure(u'm1', 1, u'u1', u'0:1', u'0:2', 0, 10),
            Measure(u'm2', 2, u'u2', u'0:2', u'0:3', 0, 20)], m)

    def test_array_expand(self):
        m = Measure.array(
                2, [u'name'], [21], [u'uom'], [u'-10:10'], [u'-20:20'], [-50])
        self.assertEqual([
            Measure(u'name', 21, u'uom', u'-10:10', u'-20:20', -50),
            Measure(u'name', 21, u'uom', u'-10:10', u'-20:20', -50)], m)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(MeasureTest)
    return suite

if __name__ == '__main__':
    unittest.main()
