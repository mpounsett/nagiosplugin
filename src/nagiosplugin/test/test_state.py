# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
import nagiosplugin.test
from nagiosplugin import state


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
        self.assertEqual(u'first line', s.headline())

    def test_longoutput(self):
        s = state.Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual([u'more lines 1', u'more lines 2'],
                         s.longoutput())

    def test_init_should_box_bare_message(self):
        self.assertEqual([u'bare message'],
                         state.Ok(u'bare message').messages)

    def test_reduce_should_discard_minor_status(self):
        s_crit = state.Critical(u'problem')
        s_ok = state.Ok(u'no problem')
        self.assertEqual(s_crit, state.reduce(s_crit, s_ok))

    def test_reduce_should_not_concant_messages_of_minor_state(self):
        s1 = state.Warning([u'msg 1', u'msg 2'])
        s2 = state.Unknown([u'msg 3', u'msg 4'])
        self.assertEqual([u'msg 3', u'msg 4'], state.reduce(s1, s2).messages)

    def test_reduct_should_concat_messages_of_equal_states(self):
        s1 = state.Warning([u'msg 1', u'msg 2'])
        s2 = state.Warning([u'msg 3', u'msg 4'])
        self.assertEqual([u'msg 1', u'msg 2', u'msg 3', u'msg 4'],
                         state.reduce(s1, s2).messages)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(StateTest)
    return suite

if __name__ == '__main__':
    unittest.main()
