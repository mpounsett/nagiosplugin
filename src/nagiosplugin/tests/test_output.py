# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from __future__ import unicode_literals, print_function
from nagiosplugin.output import Output
import nagiosplugin
import io
import logging
import unittest


class FakeCheck:

    name = 'Fake'
    state = nagiosplugin.Ok
    summary_str = 'check summary'
    verbose_str = 'hello world\n'
    perfdata = ['foo=1m;2;3', 'bar=1s;2;3']


class OutputTest(unittest.TestCase):

    def setUp(self):
        self.logio = io.StringIO()
        self.logchan = logging.StreamHandler(self.logio)

    def test_add_longoutput_string(self):
        o = Output(self.logchan)
        o.add_longoutput('first line\nsecond line\n')
        self.assertEqual(str(o), 'first line\nsecond line\n')

    def test_add_longoutput_list(self):
        o = Output(self.logchan)
        o.add_longoutput(['first line', 'second line'])
        self.assertEqual(str(o), 'first line\nsecond line\n')

    def test_add_longoutput_tuple(self):
        o = Output(self.logchan)
        o.add_longoutput(('first line', 'second line'))
        self.assertEqual(str(o), 'first line\nsecond line\n')

    def test_str_should_append_log(self):
        o = Output(self.logchan)
        print('debug log output', file=self.logio)
        self.assertEqual('debug log output\n', str(o))

    def test_empty_summary_perfdata(self):
        o = Output(self.logchan)
        check = FakeCheck()
        check.summary_str = ''
        check.perfdata = []
        o.add(check)
        self.assertEqual('FAKE OK\n', str(o))

    def test_empty_name(self):
        o = Output(self.logchan)
        check = FakeCheck()
        check.name = None
        check.perfdata = []
        o.add(check)
        self.assertEqual('OK - check summary\n', str(o))

    def test_add_check_singleline(self):
        o = Output(self.logchan)
        o.add(FakeCheck())
        self.assertEqual("""\
FAKE OK - check summary | foo=1m;2;3 bar=1s;2;3
""", str(o))

    def test_add_check_multiline(self):
        o = Output(self.logchan, verbose=1)
        o.add(FakeCheck())
        self.assertEqual("""\
FAKE OK - check summary
hello world
| foo=1m;2;3 bar=1s;2;3
""", str(o))

    def test_remove_illegal_chars(self):
        check = FakeCheck()
        check.summary_str = 'PIPE | STATUS'
        check.verbose_str = 'long pipe | output'
        check.perfdata = []
        print('debug pipe | x', file=self.logio)
        o = Output(self.logchan, verbose=1)
        o.add(check)
        self.assertEqual("""\
FAKE OK - PIPE  STATUS
long pipe  output
debug pipe  x
warning: removed illegal characters (0x7c) from status line
warning: removed illegal characters (0x7c) from long output
warning: removed illegal characters (0x7c) from logging output
""", str(o))

    def test_perfdata_linebreak(self):
        check = FakeCheck()
        check.verbose_str = ''
        check.perfdata = ['duration=340.4ms;500;1000;0'] * 5
        o = Output(self.logchan, verbose=1)
        o.add(check)
        self.assertEqual("""\
FAKE OK - check summary
| duration=340.4ms;500;1000;0 duration=340.4ms;500;1000;0
duration=340.4ms;500;1000;0 duration=340.4ms;500;1000;0
duration=340.4ms;500;1000;0
""", str(o))

    def test_log_output_precedes_perfdata(self):
        check = FakeCheck()
        check.perfdata = ['foo=1']
        print('debug log output', file=self.logio)
        o = Output(self.logchan, verbose=1)
        o.add(check)
        self.assertEqual("""\
FAKE OK - check summary
hello world
debug log output
| foo=1
""", str(o))
