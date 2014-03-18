# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

"""Python 2/3 compatibility wrappers.

This module contains imports and functions that help mask Python 2/3
compatibility issues.
"""

# UserDict
try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict

# StringIO
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO
