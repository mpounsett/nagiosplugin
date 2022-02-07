# -*- coding: utf-8 -*-
"""NT implementation of platform-specific services."""

import threading
# This only loads on Windows
# pylint: disable-next=import-error
import msvcrt

import nagiosplugin

def with_timeout(timeout, func, *args, **kwargs):
    """Call `func` but terminate after `timeout` seconds.

    We use a thread here since NT systems don't have POSIX signals.
    """

    func_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    func_thread.daemon = True  # quit interpreter even if still running
    func_thread.start()
    func_thread.join(timeout)
    if func_thread.is_alive():
        raise nagiosplugin.Timeout('{0}s'.format(timeout))


def flock_exclusive(fileobj):
    """Acquire exclusive lock for open file `fileobj`."""
    msvcrt.locking(fileobj.fileno(), msvcrt.LK_LOCK, 2147483647)
