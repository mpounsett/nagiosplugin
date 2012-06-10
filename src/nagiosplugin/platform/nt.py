# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""NT implementation of platform-specific services"""

from __future__ import print_function, unicode_literals
from nagiosplugin.errors import TimeoutError
import threading


def with_timeout(t, func, args=(), kwargs={}):
    """Call `func` but terminate after `t` seconds.

    We use a thread here since NT systems don't have POSIX signals.
    """

    func_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    func_thread.daemon = True  # quit interpreter even if still running
    func_thread.start()
    func_thread.join(t)
    if func_thread.is_alive():
        raise TimeoutError('timeout exceeded')
