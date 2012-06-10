# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Common errors used in the nagiosplugin library"""

from __future__ import print_function, unicode_literals


class TimeoutError(RuntimeError):
    """Plugin execution exceeded timeout."""
    pass
