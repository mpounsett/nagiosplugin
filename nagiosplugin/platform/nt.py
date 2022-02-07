# -*- coding: utf-8 -*-
"""NT implementation of platform-specific services."""

import threading
# This only loads on Windows
# pylint: disable-next=import-error
import msvcrt

import nagiosplugin

# Changing the badly-named `t` variable at this point is likely API-breaking,
# so it will be left in place.
# pylint: disable-next=invalid-name
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
