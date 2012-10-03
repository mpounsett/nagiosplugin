import io
import logging
import numbers
import sys
import functools
import traceback


def managed(func):
    @functools.wraps(func)
    def wrapper():
        rt = Runtime()
        try:
            func(rt)
        except Exception:
            exc_type, value, tb = sys.exc_info()
            filename, lineno = traceback.extract_tb(tb)[-1][0:2]
            print('UNKNOWN: %s (%s:%d)' % (
                traceback.format_exception_only(exc_type, value)[0].strip(),
                filename, lineno))
            if rt.verbose > 0:
                traceback.print_exc()
                print(rt.logchan.stream.getvalue())
            sys.exit(3)
    return wrapper


class Runtime:
    def __init__(self):
        rootlogger = logging.getLogger()
        rootlogger.setLevel(logging.DEBUG)
        self.logchan = logging.StreamHandler(io.StringIO())
        self.logchan.setFormatter(logging.Formatter(
            '%(filename)s:%(lineno)d: %(message)s'))
        rootlogger.addHandler(self.logchan)
        self.verbose = 0
        self.timeout = 10
        self.output = ''
        self.exitcode = 70  # EX_SOFTWARE

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
        elif self._verbose == 2:
            self.logchan.setLevel(logging.INFO)
        else:
            self.logchan.setLevel(logging.WARNING)

    def run(self, check):
        check()
        self.output += str(check)
        self.output += self.logchan.stream.getvalue()
        self.exitcode = check.exitcode

    def execute(self, check):
        self.run(check)
        print(self.output)
        sys.exit(self.exitcode)
