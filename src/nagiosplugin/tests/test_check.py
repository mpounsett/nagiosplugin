# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.check import Check
import nagiosplugin
import unittest


class FakeSummary(nagiosplugin.Summary):

    def ok(self, results):
        return "I'm feelin' good"

    def problem(self, results):
        return 'Houston, we have a problem'


class R1_MetricDefaultContext(nagiosplugin.Resource):

    def survey(self):
        return [nagiosplugin.Metric('foo', 1, context='default')]


class CheckTest(unittest.TestCase):

    def test_add_resource(self):
        c = Check()
        r1 = nagiosplugin.Resource()
        r2 = nagiosplugin.Resource()
        c.add(r1, r2)
        self.assertEqual([r1, r2], c.resources)

    def test_add_context(self):
        ctx = nagiosplugin.ScalarContext('ctx1', '', '')
        c = Check(ctx)
        self.assertIn(ctx.name, c.contexts)

    def test_add_summary(self):
        s = nagiosplugin.Summary()
        c = Check(s)
        self.assertEqual(s, c.summary)

    def test_add_results(self):
        r = nagiosplugin.Results()
        c = Check(r)
        self.assertEqual(r, c.results)

    def test_add_unknown_type_should_raise_typeerror(self):
        with self.assertRaises(TypeError):
            Check(object())

    def test_evaluate_resource_populates_results_perfdata(self):
        c = Check()
        c.evaluate_resource(R1_MetricDefaultContext())
        self.assertEqual(1, len(c.results))
        self.assertEqual('foo', c.results[0].metric.name)
        self.assertEqual(['foo=1'], c.perfdata)

    def test_evaluate_resource_looks_up_context(self):
        class R2_MetricCustomContext(nagiosplugin.Resource):
            def survey(self):
                return [nagiosplugin.Metric('bar', 2)]

        ctx = nagiosplugin.ScalarContext('bar', '1', '1')
        c = Check(ctx)
        c.evaluate_resource(R2_MetricCustomContext())
        self.assertEqual(c.results[0].metric.context, ctx)

    def test_evaluate_resource_catches_checkerror(self):
        class R3_Faulty(nagiosplugin.Resource):
            def survey(self):
                raise nagiosplugin.CheckError('problem')

        c = Check()
        c.evaluate_resource(R3_Faulty())
        result = c.results[0]
        self.assertEqual(nagiosplugin.Unknown, result.state)
        self.assertEqual('problem', result.reason)

    def test_first_resource_sets_name(self):
        class MyResource(nagiosplugin.Resource):
            pass

        c = Check()
        self.assertEqual('', c.name)
        c.add(MyResource())
        self.assertEqual('MyResource', c.name)

    def test_set_explicit_name(self):
        c = Check()
        c.name = 'mycheck'
        c.add(nagiosplugin.Resource())
        self.assertEqual('mycheck', c.name)

    def test_check_without_results_is_unkown(self):
        self.assertEqual(nagiosplugin.Unknown, Check().state)

    def test_summary_str_should_be_ok_if_state_ok(self):
        c = Check()
        c.evaluate_resource(R1_MetricDefaultContext())
        self.assertEqual("I'm feelin' good", c.summary_str)
