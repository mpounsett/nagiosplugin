# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.context import Context, Contexts
import nagiosplugin
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

    def test_fmt_template(self):
        m1 = nagiosplugin.Metric('foo', 1, 's', min=0)
        c = Context('describe_template', '{name} is {valueunit} (min {min})')
        self.assertEqual('foo is 1s (min 0)', c.describe(m1))

    def test_fmt_callable(self):
        def format_metric(metric, context):
            return '{} formatted by {}'.format(metric.name, context.name)

        m1 = nagiosplugin.Metric('foo', 1, 's', min=0)
        c = Context('describe_callable', fmt_metric=format_metric)
        self.assertEqual('foo formatted by describe_callable', c.describe(m1))
