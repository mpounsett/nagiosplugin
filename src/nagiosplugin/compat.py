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


# open has no encoding parameter in Python 2
def open_encoded(path, mode, buffering=-1, encoding=None):
    """Opens a file with specific encoding."""
    if not encoding:
        return open(path, mode, buffering=buffering)
    try:
        return open(path, mode, buffering=buffering, encoding=encoding)
    except TypeError:
        import codecs
        return codecs.open(path, mode, encoding, 'strict', buffering)
