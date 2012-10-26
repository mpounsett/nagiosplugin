# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.context import Context, Contexts
import unittest


class ContextsTest(unittest.TestCase):

    def test_keyerror(self):
        ctx = Contexts()
        ctx.add(Context('foo'))
        with self.assertRaises(KeyError):
            ctx['bar']

    def test_contains(self):
        ctx = Contexts()
        ctx.add(Context('foo'))
        self.assertTrue('foo' in ctx)
        self.assertFalse('bar' in ctx)
