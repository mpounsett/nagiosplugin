# -*- coding: utf-8 -*-
"""NT implementation of platform-specific services."""

import nagiosplugin
import threading
import msvcrt


def with_timeout(t, func, *args, **kwargs):
    """Call `func` but terminate after `t` seconds.

    We use a thread here since NT systems don't have POSIX signals.
    """

    func_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    func_thread.daemon = True  # quit interpreter even if still running
    func_thread.start()
    func_thread.join(t)
    if func_thread.is_alive():
        raise nagiosplugin.Timeout('{0}s'.format(t))


def flock_exclusive(fileobj):
    """Acquire exclusive lock for open file `fileobj`."""
    msvcrt.locking(fileobj.fileno(), msvcrt.LK_LOCK, 2147483647)
