# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
from nagiosplugin import pluginoptparse


class PluginOptionParserTest(unittest.TestCase):

    def setUp(self):
        self.op = pluginoptparse.PluginOptionParser(prog='prog', version='1.0')

    def test_stderr_returns_none_on_success(self):
        self.op.parse_args([])
        self.assertEqual(u'', self.op.get_stderr())

    def test_invalid_option_should_return_msg_in_stderr(self):
        self.op.parse_args(['--invalid'])
        exp = (u'Usage: prog [options]\n\n'
               u'prog: error: no such option: --invalid\n')
        self.assertEqual(exp, self.op.get_stderr())

    def test_help_option_should_return_msg_in_stdout(self):
        self.op.parse_args(['--help'])
        exp = u'-h, --help  show this help message and exit'
        self.assert_(self.op.get_stdout().find(exp) >= 0,
                     u'cannot find "%s" in "%s"' % (exp, self.op.get_stdout()))

    def test_version_option_should_return_msg_in_stdout(self):
        self.op.parse_args(['--version'])
        self.assertEqual(u'prog 1.0\n', self.op.get_stdout())

    def test_report_internal_errors(self):
        self.op.add_option('-r', type='choice', default=u'foo',
                           choices=['foo', 'bar'])
        self.op.parse_args(['-r'])
        self.assert_(self.op.stderr.getvalue().find(u'invalid option') >= 0)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PluginOptionParserTest)
    return suite

if __name__ == '__main__':
    unittest.main()
