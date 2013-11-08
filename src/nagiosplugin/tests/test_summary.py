# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.summary import Summary
import nagiosplugin
import unittest


class SummaryTest(unittest.TestCase):

    def test_ok_returns_first_result(self):
        results = nagiosplugin.Results(
            nagiosplugin.Result(nagiosplugin.Ok, 'result 1'),
            nagiosplugin.Result(nagiosplugin.Ok, 'result 2'))
        self.assertEqual('result 1', Summary().ok(results))

    def test_problem_returns_first_significant(self):
        results = nagiosplugin.Results(
            nagiosplugin.Result(nagiosplugin.Ok, 'result 1'),
            nagiosplugin.Result(nagiosplugin.Critical, 'result 2'))
        self.assertEqual('result 2', Summary().problem(results))

    def test_verbose(self):
        self.assertEqual(
            ['critical: reason1', 'warning: reason2'],
            Summary().verbose(nagiosplugin.Results(
                nagiosplugin.Result(nagiosplugin.Critical, 'reason1'),
                nagiosplugin.Result(nagiosplugin.Ok, 'ignore'),
                nagiosplugin.Result(nagiosplugin.Warn, 'reason2'))))
