# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
import nagiosplugin.test
from nagiosplugin import measure

nagiosplugin.test.path_setup()


class MeasureTest(unittest.TestCase):

    def test_ok(self):
        m = measure.Measure(u'm1', 8, warning=u'8', critical=u'9.4')
        self.assertEqual(u'OK', str(m.state()))

    def test_warn(self):
        m = measure.Measure(u'm1', 9, u's', warning=u'8', critical=u'9.4')
        s = m.state()
        self.assertEqual(u'WARNING', str(s))
        self.assertEqual(u'm1 value 9s exceeds warning range 8',
                         s.headline())

    def test_crit(self):
        m = measure.Measure(u'm1', 9.5, u's', warning=u'8', critical=u'9.4')
        s = m.state()
        self.assertEqual(u'CRITICAL', str(s))
        self.assertEqual(u'm1 value 9.5s exceeds critical range 9.4',
                         s.headline())

    def test_performance(self):
        m = measure.Measure(u'm2', 75, u'MB', warning=u'33:80',
                            critical=u'31:82', min=10, max=100)
        self.assertEqual(u'm2=75MB;33:80;31:82;10;100',
                         m.performance())

    def test_short_performance(self):
        m = measure.Measure(u'm3', 4)
        self.assertEqual(u'm3=4', m.performance())

    def test_performance_show_zero_min(self):
        m = measure.Measure(u'm4', 15, u's', min=0)
        self.assertEqual(u'm4=15s;;;0', m.performance())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(MeasureTest)
    return suite

if __name__ == '__main__':
    unittest.main()
