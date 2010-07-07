# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.check
import nagiosplugin.measure
import nagiosplugin.state
import nagiosplugin.test
import unittest
from nagiosplugin import controller


class MockCheck(nagiosplugin.check.Check):

    def obtain_data(self, opts, args):
        pass


class ControllerTest(unittest.TestCase):

    def test_init_creates_check_object(self):
        c = controller.Controller(MockCheck)
        self.assert_(isinstance(c.check, MockCheck),
                     u'%r is not an instance of MockCheck' % c.check)

    def test_format_with_default_message(self):
        class DefaultMessageCheck(MockCheck):
            @property
            def default_message(self):
                return u'default message'
        c = controller.Controller(DefaultMessageCheck)
        self.assertEqual(u'CHECK OK - default message\n', c.stdout)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ControllerTest)
    return suite

if __name__ == '__main__':
    unittest.main()
