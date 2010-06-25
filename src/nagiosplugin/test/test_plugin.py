# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import os
import os.path
import sys
import unittest

sys.path[0:0] = [os.path.abspath('%s/../..' % os.path.dirname(__file__))]
import nagiosplugin.plugin

class PluginTest(unittest.TestCase):

    def test_truth(self):
        self.assert_(True)


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(PluginTest)
    return suite


if __name__ == '__main__':
    unittest.main()
