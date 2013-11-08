# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

"""Functions and classes to interface with the system.

This module contains the :class:`Runtime` class that handles exceptions,
timeouts and logging. Plugin authors should not use Runtime directly,
but decorate the plugin's main function with :func:`~.runtime.guarded`.
"""

from __future__ import unicode_literals, print_function
from .output import Output
from .error import Timeout
from .platform import with_timeout
import io
import logging
import numbers
import sys
import functools
import traceback


def guarded(func):
    """Runs a function in a newly created runtime environment.

    A guarded function behaves correctly with respect to the Nagios
    plugin API if it aborts with an uncaught exception or a
    timeout. It exits with an *unknown* exit code and prints a traceback
    in a format acceptable by Nagios.

    This function should be used as a decorator for the plugin's `main`
    function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        runtime = Runtime()
        try:
            return func(*args, **kwds)
        except Timeout as exc:
            runtime._handle_exception(
                'Timeout: check execution aborted after {0}'.format(
                    exc))
        except Exception:
            runtime._handle_exception()
    return wrapper


class Runtime(object):

    instance = None
    check = None
    _verbose = 1
    timeout = None
    logchan = None
    output = None
    stdout = sys.stdout
    exitcode = 70  # EX_SOFTWARE

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(Runtime, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        rootlogger = logging.getLogger(__name__.split('.', 1)[0])
        rootlogger.setLevel(logging.DEBUG)
        if not self.logchan:
            self.logchan = logging.StreamHandler(io.StringIO())
            self.logchan.setFormatter(logging.Formatter(
                '%(message)s (%(filename)s:%(lineno)d)'))
            rootlogger.addHandler(self.logchan)
        if not self.output:
            self.output = Output(self.logchan)

    def _handle_exception(self, statusline=None):
        exc_type, value = sys.exc_info()[0:2]
        name = self.check.name.upper() + ' ' if self.check else ''
        self.output.status = '{0}UNKNOWN: {1}'.format(
            name, statusline or traceback.format_exception_only(
                exc_type, value)[0].strip())
        if self.verbose > 0:
            self.output.add_longoutput(traceback.format_exc())
        print('{0}'.format(self.output), end='', file=self.stdout)
        self.exitcode = 3
        self.sysexit()

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        if isinstance(verbose, numbers.Number):
            self._verbose = int(verbose)
        else:
            self._verbose = len(verbose or [])
        if self._verbose >= 3:
            self.logchan.setLevel(logging.DEBUG)
            self._verbose = 3
        elif self._verbose == 2:
            self.logchan.setLevel(logging.INFO)
        else:
            self.logchan.setLevel(logging.WARNING)
        self.output.verbose = self._verbose

    def run(self, check):
        check()
        self.output.add(check)
        self.exitcode = check.exitcode

    def execute(self, check, verbose=None, timeout=None):
        self.check = check
        if verbose is not None:
            self.verbose = verbose
        if timeout is not None:
            self.timeout = int(timeout)
        if self.timeout:
            with_timeout(self.timeout, self.run, check)
        else:
            self.run(check)
        print('{0}'.format(self.output), end='', file=self.stdout)
        self.sysexit()

    def sysexit(self):
        sys.exit(self.exitcode)
