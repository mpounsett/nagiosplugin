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
        m = measure.Measure(u'm1', 9, warning=u'8', critical=u'9.4')
        s = m.state()
        self.assertEqual(u'WARNING', str(s))
        self.assertEqual(u'm1 value 9 is out of warning range 8', s.mainoutput())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(MeasureTest)
    return suite

if __name__ == '__main__':
    unittest.main()
