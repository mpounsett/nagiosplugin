# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from nagiosplugin.output import Output
import unittest
import logging
import io


class OutputTest(unittest.TestCase):

    def setUp(self):
        self.logio = io.StringIO()
        self.logchan = logging.StreamHandler(self.logio)

    def test_add_status(self):
        o = Output(self.logchan)
        o.add_status('CHECK_NAME: STATUS Text')
        self.assertEqual(str(o), 'CHECK_NAME: STATUS Text\n')

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

    def test_remove_illegal_chars(self):
        o = Output(self.logchan)
        o.add_status('PIPE | STATUS')
        o.add_longoutput('long pipe | output')
        print('debug pipe | x', file=self.logio)
        self.assertEqual("""\
PIPE  STATUS
long pipe  output
debug pipe  x
warning: removed illegal characters (0x7c) from status line
warning: removed illegal characters (0x7c) from long output
warning: removed illegal characters (0x7c) from logging output
""", str(o))

    def test_add_check_singleline(self):
        # XXX
        pass

    def test_add_check_multiline(self):
        # XXX
        pass
