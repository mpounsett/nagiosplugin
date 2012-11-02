# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.summary import Summary
from nagiosplugin.result import Result
from nagiosplugin import state
import unittest


class SummaryTest(unittest.TestCase):

    def test_ok_returns_first_result(self):
        results = ['result 1', 'result 2']
        self.assertEqual('result 1', Summary().ok(results))

    def test_verbose(self):
        self.assertEqual(['critical: reason1', 'warning: reason2'],
                         Summary().verbose([
                             Result(state.Critical, 'reason1'),
                             Result(state.Ok, 'ignore'),
                             Result(state.Warn, 'reason2')]))
