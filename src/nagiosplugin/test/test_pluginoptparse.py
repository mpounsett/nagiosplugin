# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
from nagiosplugin import pluginoptparse


class PluginOptionParserTest(unittest.TestCase):
    pass


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PluginOptionParserTest)
    return suite

if __name__ == '__main__':
    unittest.main()
