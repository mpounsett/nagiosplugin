# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
from nagiosplugin import pluginoptparse


class PluginOptionParserTest(unittest.TestCase):

    def setUp(self):
        self.op = pluginoptparse.PluginOptionParser()

    def test_stderr_returns_none_on_success(self):
        self.op.parse_args([])
        self.assertEqual(u'', self.op.stderr)

    def test_invalid_option_should_return_msg_in_stderr(self):
        self.op.parse_args(['--invalid'])
        self.assertEqual(u'no such option: --invalid\n', self.op.stderr)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PluginOptionParserTest)
    return suite

if __name__ == '__main__':
    unittest.main()
