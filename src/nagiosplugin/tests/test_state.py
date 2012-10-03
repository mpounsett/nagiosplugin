# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
from nagiosplugin.state import Ok, Warn, Unknown, Critical, dominantstate


class StateTest(unittest.TestCase):

    def test_str(self):
        self.assertEqual(u'OK', str(Ok))

    def test_int(self):
        self.assertEqual(0, int(Ok))

    def test_cmp_less(self):
        self.assertEqual(-1, cmp(Warn, Critical))

    def test_cmp_equal(self):
        self.assertEqual(0, cmp(Unknown, Unknown))

    def test_cmp_greater(self):
        self.assertEqual(1, cmp(Warn, Ok))

    def test_firstline(self):
        s = Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual(u'first line', s.headline())

    def test_longoutput(self):
        s = Ok([u'first line', u'more lines 1', u'more lines 2'])
        self.assertEqual([u'more lines 1', u'more lines 2'],
                         s.longoutput())

    def test_init_should_box_bare_message(self):
        self.assertEqual([u'bare message'],
                         Ok(u'bare message').messages)

    def test_reduce_should_discard_minor_status(self):
        s_crit = Critical(u'problem')
        s_ok = Ok(u'no problem')
        self.assertEqual(s_crit, dominantstate(s_crit, s_ok))
