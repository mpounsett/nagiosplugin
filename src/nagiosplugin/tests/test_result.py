# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.result import Result, ScalarResult, Results
from nagiosplugin.state import Ok, Warn, Critical, Unknown
import nagiosplugin
import unittest


class ResultTest(unittest.TestCase):

    def test_resorce_should_be_none_for_resourceless_metric(self):
        self.assertIsNone(Result(Ok).resource)

    def test_metric_resorce(self):
        m = nagiosplugin.Metric('foo', 1)
        r = m.resource = object()
        self.assertEqual(Result(Ok, metric=m).resource, r)

    def test_context_should_be_none_for_contextless_metric(self):
        self.assertIsNone(Result(Ok).context)

    def test_metric_context(self):
        m = nagiosplugin.Metric('foo', 1)
        c = m.context = object()
        self.assertEqual(Result(Ok, metric=m).context, c)


class ScalarResultTest(unittest.TestCase):

    def test_new_should_fail_without_metric(self):
        with self.assertRaises(RuntimeError):
            ScalarResult(nagiosplugin.Unknown, None, None)

    def test_str_gives_range_violation_hint(self):
        self.assertEqual(
            '2 (greater than 1)',
            str(ScalarResult(Warn, nagiosplugin.Range('1'),
                             nagiosplugin.Metric('foo', 2))))

    def test_str_gives_plain_reason(self):
        self.assertEqual(
            '2 (bad day)',
            str(ScalarResult(Warn, 'bad day',
                             nagiosplugin.Metric('foo', 2))))


class ResultsTest(unittest.TestCase):

    def test_lookup_by_metric_name(self):
        r = Results()
        result = Result(Ok, '', nagiosplugin.Metric('met1', 0))
        r.add(result, Result(Ok, 'other'))
        self.assertEqual(r['met1'], result)

    def test_lookup_by_index(self):
        r = Results()
        result = Result(Ok, '', nagiosplugin.Metric('met1', 0))
        r.add(Result(Ok, 'other'), result)
        self.assertEqual(r[1], result)

    def test_len(self):
        r = Results()
        r.add(Result(Ok), Result(Ok), Result(Ok))
        self.assertEqual(3, len(r))

    def test_iterate_in_order_of_descending_states(self):
        r = Results()
        r.add(Result(Warn), Result(Ok), Result(Critical), Result(Warn))
        self.assertEqual([Critical, Warn, Warn, Ok],
                         [result.state for result in r])

    def test_most_significant_state_shoud_raise_valueerror_if_empty(self):
        with self.assertRaises(ValueError):
            Results().most_significant_state

    def test_most_significant_state(self):
        r = Results()
        r.add(Result(Ok))
        self.assertEqual(Ok, r.most_significant_state)
        r.add(Result(Critical))
        self.assertEqual(Critical, r.most_significant_state)
        r.add(Result(Warn))
        self.assertEqual(Critical, r.most_significant_state)

    def test_most_significant_should_return_empty_set_if_empty(self):
        self.assertEqual([], Results().most_significant)

    def test_most_signigicant(self):
        r = Results()
        r.add(Result(Ok), Result(Warn), Result(Ok), Result(Warn))
        self.assertEqual([Warn, Warn],
                         [result.state for result in r.most_significant])

    def test_first_significant(self):
        r = Results()
        r.add(Result(Critical), Result(Unknown, 'r1'), Result(Unknown, 'r2'),
              Result(Ok))
        self.assertEqual(Result(Unknown, 'r1'), r.first_significant)
