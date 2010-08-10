# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import doctest
import os
import sys
import unittest


def suite():
    base = os.path.abspath('%s/../..' % os.path.dirname(__file__))
    sys.path[0:0] = [base, os.path.join(base, '../examples')]
    suite = doctest.DocFileSuite(
        'check_load.txt',
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS |
                    doctest.REPORT_NDIFF)
    return suite


# needed for setuptools
def additional_tests():
    return suite()


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
