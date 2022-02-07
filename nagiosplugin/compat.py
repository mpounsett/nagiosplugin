# -*- coding: utf-8 -*-
"""Python 2/3 compatibility wrappers.

This module contains imports and functions that help mask Python 2/3
compatibility issues.
"""
import tempfile


# UserDict
try:
    # pylint: disable-next=unused-import
    from collections import UserDict
except ImportError:
    from UserDict import UserDict   # noqa: F401

# StringIO
try:
    # pylint: disable-next=unused-import
    from io import StringIO
except ImportError:
    from StringIO import StringIO   # noqa: F401


# This reproduces the py27 signature for this function, so we'll ignore the
# shadowed built-in in this case.
def TemporaryFile(mode='w+b', encoding=None, suffix='', prefix='tmp',
                  dir=None):    # pylint: disable=redefined-builtin
    """
    Provide py2/3 compatability for TemporaryFile.

    Redefining TemporaryFile from py27 because it doesn't support the
    `encoding` parameter.
    """
    try:
        return tempfile.TemporaryFile(
            mode=mode, encoding=encoding, suffix=suffix, prefix=prefix,
            dir=dir)
    except TypeError:
        return tempfile.TemporaryFile(
            mode=mode, suffix=suffix, prefix=prefix, dir=dir)
