# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.runtime import Runtime, guarded
from nagiosplugin.compat import StringIO
import nagiosplugin
import logging

try:
    import unittest2 as unittest
except ImportError:  # pragma: no cover
    import unittest


def make_check():
    class Check(object):
        summary_str = 'summary'
        verbose_str = 'long output'
        name = 'check'
        state = nagiosplugin.Ok
        exitcode = 0
        perfdata = None

        def __call__(self):
            pass

    return Check()


class RuntimeTestBase(unittest.TestCase):

    def setUp(self):
        Runtime.instance = None
        self.r = Runtime()
        self.r.sysexit = lambda: None
        self.r.stdout = StringIO()


class RuntimeTest(RuntimeTestBase):

    def test_runtime_is_singleton(self):
        self.assertEqual(self.r, Runtime())

    def test_run_sets_exitcode(self):
        self.r.run(make_check())
        self.assertEqual(0, self.r.exitcode)

    def test_verbose(self):
        testcases = [(None, logging.WARNING, 0),
                     (1, logging.WARNING, 1),
                     ('vv', logging.INFO, 2),
                     (3, logging.DEBUG, 3),
                     ('vvvv', logging.DEBUG, 3)]
        for argument, exp_level, exp_verbose in testcases:
            self.r.verbose = argument
            self.assertEqual(exp_level, self.r.logchan.level)
            self.assertEqual(exp_verbose, self.r.verbose)

    def test_execute_uses_defaults(self):
        self.r.execute(make_check())
        self.assertEqual(1, self.r.verbose)
        self.assertEqual(None, self.r.timeout)

    def test_execute_sets_verbose_and_timeout(self):
        self.r.execute(make_check(), 2, 10)
        self.assertEqual(2, self.r.verbose)
        self.assertEqual(10, self.r.timeout)


class RuntimeExceptionTest(RuntimeTestBase):

    def setUp(self):
        super(RuntimeExceptionTest, self).setUp()

    def run_main_with_exception(self, exc):
        @guarded
        def main():
            raise exc
        main()

    def test_handle_exception_set_exitcode_and_formats_output(self):
        self.run_main_with_exception(RuntimeError('problem'))
        self.assertEqual(3, self.r.exitcode)
        self.assertIn('UNKNOWN: RuntimeError: problem',
                      self.r.stdout.getvalue())

    def test_handle_exception_prints_no_traceback(self):
        self.r.verbose = 0
        self.run_main_with_exception(RuntimeError('problem'))
        self.assertNotIn('Traceback', self.r.stdout.getvalue())

    def test_handle_exception_verbose(self):
        self.r.verbose = 1
        self.run_main_with_exception(RuntimeError('problem'))
        self.assertIn('Traceback', self.r.stdout.getvalue())

    def test_handle_timeout_exception(self):
        self.run_main_with_exception(nagiosplugin.Timeout('1s'))
        self.assertIn('UNKNOWN: Timeout: check execution aborted after 1s',
                      self.r.stdout.getvalue())
