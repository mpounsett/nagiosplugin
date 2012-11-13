# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.metric import Metric
import nagiosplugin
import unittest


class MetricTest(unittest.TestCase):

    def test_description(self):
        self.assertEqual('time is 1s', Metric(
            'time', 1, 's', contextobj=nagiosplugin.Context('ctx')
        ).description)

    def test_valueunit_float(self):
        self.assertEqual('1.302s', Metric('time', 1.30234876, 's').valueunit)

    def test_valueunit_nonfloat(self):
        self.assertEqual('text', Metric('text', 'text').valueunit)

    def test_evaluate_fails_if_no_context(self):
        with self.assertRaises(RuntimeError):
            Metric('time', 1, 's').evaluate()

    def test_performance_fails_if_no_context(self):
        with self.assertRaises(RuntimeError):
            Metric('time', 1, 's').performance()
