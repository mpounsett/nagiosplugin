# -*- coding: utf-8 -*-
"""Python 2/3 compatibility wrappers.

This module contains imports and functions that help mask Python 2/3
compatibility issues.
"""

import tempfile


# UserDict
try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict   # noqa: F401

# StringIO
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO   # noqa: F401


# Python 2: TemporaryFile does not support the `encoding` parameter
def TemporaryFile(mode='w+b', encoding=None, suffix='', prefix='tmp',
                  dir=None):
    try:
        return tempfile.TemporaryFile(
            mode=mode, encoding=encoding, suffix=suffix, prefix=prefix,
            dir=dir)
    except TypeError:
        return tempfile.TemporaryFile(
            mode=mode, suffix=suffix, prefix=prefix, dir=dir)
