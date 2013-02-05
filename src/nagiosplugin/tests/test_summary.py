# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.summary import Summary
import nagiosplugin
import unittest


class SummaryTest(unittest.TestCase):

    def test_ok_returns_first_result(self):
        results = ['result 1', 'result 2']
        self.assertEqual('result 1', Summary().ok(results))

    def test_verbose(self):
        self.assertEqual(
            ['critical: reason1', 'warning: reason2'],
            Summary().verbose([
                nagiosplugin.Result(nagiosplugin.Critical, 'reason1'),
                nagiosplugin.Result(nagiosplugin.Ok, 'ignore'),
                nagiosplugin.Result(nagiosplugin.Warn, 'reason2')]))
