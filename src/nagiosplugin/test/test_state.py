# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
import nagiosplugin.test
from nagiosplugin import state

nagiosplugin.test.path_setup()


class StateTest(unittest.TestCase):

    def test_str(self):
        self.assertEqual(u'OK', str(state.Ok()))

    def test_int(self):
        self.assertEqual(0, int(state.Ok()))

    def test_cmp_less(self):
        self.assertEqual(-1, cmp(state.Warning(), state.Critical()))

    def test_cmp_equal(self):
        self.assertEqual(0, cmp(state.Unknown(), state.Unknown()))

    def test_cmp_greater(self):
        self.assertEqual(1, cmp(state.Warning(), state.Ok()))

    def test_firstline(self):
        s = state.Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual(u'first line', s.mainoutput())

    def test_longoutput(self):
        s = state.Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual([u'more lines 1', u'more lines 2'],
                         s.longoutput())

    def test_init_should_box_bare_message(self):
        self.assertEqual([u'bare message'],
                         state.Ok(u'bare message').messages)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(StateTest)
    return suite

if __name__ == '__main__':
    unittest.main()

