# -*- coding: utf-8 -*-
"""POSIX implementation of platform-specific services"""

import fcntl
import signal

import nagiosplugin


def with_timeout(timeout, func, *args, **kwargs):
    """Call `func` but terminate after `timeout` seconds."""
    def timeout_handler(signum, frame):
        raise nagiosplugin.Timeout('{0}s'.format(timeout))

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        func(*args, **kwargs)
    finally:
        signal.alarm(0)


def flock_exclusive(fileobj):
    """Acquire exclusive lock for open file `fileobj`."""
    fcntl.flock(fileobj, fcntl.LOCK_EX)
