# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import nagiosplugin.check
import nagiosplugin.state
import nagiosplugin.test
import unittest
from nagiosplugin import controller


class MockCheck(nagiosplugin.check.Check):

    def obtain_data(self, opts, args):
        self.data = 4

class StatePerformanceCheck(MockCheck):

    def states(self):
        return [nagiosplugin.state.Warning([u'yellow', u'long1', u'long2'])]

    def performances(self):
        return [u'perf=4']


class ControllerTest(unittest.TestCase):

    def test_init_creates_check_object(self):
        c = controller.Controller(MockCheck)
        self.assert_(isinstance(c.check, MockCheck),
                     u'%r is not an instance of MockCheck' % c.check)

    def test_dominant_state_is_created_from_dormant_check(self):
        c = controller.Controller(MockCheck)
        self.assert_(isinstance(c.dominant_state, nagiosplugin.state.Unknown))


    def test_format_with_default_message(self):
        class DefaultMessageCheck(MockCheck):
            @property
            def default_message(self):
                return u'default message'
        c = controller.Controller(DefaultMessageCheck)
        self.assertEqual(u'CHECK OK - default message\n', c.format())

    def test_controller_should_call_obtain_data(self):
        c = controller.Controller(MockCheck)
        self.assertEqual(c.check.data, 4)

    def test_controller_should_call_states_and_performances(self):
        c = controller.Controller(StatePerformanceCheck)
        self.assert_(isinstance(c.states[0], nagiosplugin.state.Warning))
        self.assertEqual(u'perf=4', c.performances[0])

    def test_format(self):
        c = controller.Controller(StatePerformanceCheck)
        self.assertEqual(u'CHECK WARNING - yellow | perf=4\nlong1\nlong2\n',
                         c.format())


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ControllerTest)
    return suite

if __name__ == '__main__':
    unittest.main()
