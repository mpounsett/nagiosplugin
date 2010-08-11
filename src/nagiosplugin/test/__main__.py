# Test runner for command line test execution.
# Usage: python nagiosplugin/test
#
# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import os
import os.path
import sys
import unittest


here = os.path.dirname(__file__)
sys.path[0:0] = [os.path.abspath(here + '/../..')]


def suite():
    suite = unittest.TestSuite()
    for fn in os.listdir(here):
        if fn.startswith('test') and fn.endswith('.py'):
            modname = 'nagiosplugin.test.' + fn[:-3]
            __import__(modname)
            module = sys.modules[modname]
            suite.addTest(module.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
