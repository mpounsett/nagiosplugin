# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.check import Check
import nagiosplugin

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


class FakeSummary(nagiosplugin.Summary):

    def ok(self, results):
        return "I'm feelin' good"

    def problem(self, results):
        return 'Houston, we have a problem'


class R1_MetricDefaultContext(nagiosplugin.Resource):

    def probe(self):
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

    def test_check_should_accept_resource_returning_bare_metric(self):
        class R_ReturnsBareMetric(nagiosplugin.Resource):
            def probe(self):
                return nagiosplugin.Metric('foo', 0, context='default')
        res = R_ReturnsBareMetric()
        c = Check(res)
        c()
        self.assertIn(res, c.resources)

    def test_evaluate_resource_populates_results_perfdata(self):
        c = Check()
        c._evaluate_resource(R1_MetricDefaultContext())
        self.assertEqual(1, len(c.results))
        self.assertEqual('foo', c.results[0].metric.name)
        self.assertEqual(['foo=1'], c.perfdata)

    def test_evaluate_resource_looks_up_context(self):
        class R2_MetricCustomContext(nagiosplugin.Resource):
            def probe(self):
                return [nagiosplugin.Metric('bar', 2)]

        ctx = nagiosplugin.ScalarContext('bar', '1', '1')
        c = Check(ctx)
        c._evaluate_resource(R2_MetricCustomContext())
        self.assertEqual(c.results[0].metric.contextobj, ctx)

    def test_evaluate_resource_catches_checkerror(self):
        class R3_Faulty(nagiosplugin.Resource):
            def probe(self):
                raise nagiosplugin.CheckError('problem')

        c = Check()
        c._evaluate_resource(R3_Faulty())
        result = c.results[0]
        self.assertEqual(nagiosplugin.Unknown, result.state)
        self.assertEqual('problem', result.hint)

    def test_call_evaluates_resources_and_compacts_perfdata(self):
        class R4_NoPerfdata(nagiosplugin.Resource):
            def probe(self):
                return [nagiosplugin.Metric('m4', 4, context='null')]

        c = Check(R1_MetricDefaultContext(), R4_NoPerfdata())
        c()
        self.assertEqual(['foo', 'm4'], [res.metric.name for res in c.results])
        self.assertEqual(['foo=1'], c.perfdata)

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

    def test_default_summary_if_no_results(self):
        c = Check()
        self.assertEqual('no check results', c.summary_str)

    def test_state_if_resource_has_no_metrics(self):
        c = Check(nagiosplugin.Resource())
        c()
        self.assertEqual(nagiosplugin.Unknown, c.state)
        self.assertEqual(3, c.exitcode)

    def test_summary_str_calls_ok_if_state_ok(self):
        c = Check(FakeSummary())
        c._evaluate_resource(R1_MetricDefaultContext())
        self.assertEqual("I'm feelin' good", c.summary_str)

    def test_summary_str_calls_problem_if_state_not_ok(self):
        c = Check(FakeSummary())
        c.results.add(nagiosplugin.Result(nagiosplugin.Critical))
        self.assertEqual('Houston, we have a problem', c.summary_str)

    def test_execute(self):
        def fake_execute(_runtime_obj, verbose, timeout):
            self.assertEqual(2, verbose)
            self.assertEqual(20, timeout)
        r = nagiosplugin.Runtime()
        r.execute = fake_execute
        Check().main(2, 20)

    def test_verbose_str(self):
        self.assertEqual('', Check().verbose_str)
