# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.multiarg import MultiArg
import unittest


class MultiargTest(unittest.TestCase):

    def test_len(self):
        m = MultiArg(['a', 'b'])
        self.assertEqual(2, len(m))

    def test_iter(self):
        m = MultiArg(['a', 'b'])
        self.assertEqual(['a', 'b'], list(m))

    def test_split(self):
        m = MultiArg('a,b')
        self.assertEqual(['a', 'b'], list(m))

    def test_explicit_fill_element(self):
        m = MultiArg(['0', '1'], fill='extra')
        self.assertEqual('1', m[1])
        self.assertEqual('extra', m[2])

    def test_fill_with_last_element(self):
        m = MultiArg(['0', '1'])
        self.assertEqual('1', m[1])
        self.assertEqual('1', m[2])

    def test_fill_empty_multiarg_returns_none(self):
        self.assertEqual(None, MultiArg([])[0])
