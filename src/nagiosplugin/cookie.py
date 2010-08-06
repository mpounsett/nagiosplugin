# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import fcntl
import os
import os.path
from contextlib import contextmanager


class Cookie(object):
    """Status information for plugins that is persisted between runs.

    Nagios Plugins may keep track of details like the last position in a logfile
    etc. Cookie helps with that task: a string is kept between runs. The cookie
    is identified with a file name (the file goes into $HOME by default, which
    is /var/nagios on most systems). The plugin is responsible for
    serializing/deserializing that information. Human-readable ASCII text is
    strongly preferred.
    """

    def __init__(self, filename, dir=None):
        """Create new or lookup existing cookie.

        `filename` is the file where the cookie lives.
        `dir` defaults to the home directory.
        """
        if dir:
            self.filename = os.path.join(os.path.abspath(dir), filename)
        elif filename.startswith('/'):
            self.filename = os.path.abspath(filename)
        else:
            self.filename = os.path.join(os.path.expanduser('~'), filename)
        self.new = not os.path.exists(self.filename)
        self.changed = False
        self.f = file(self.filename, 'a+')
        fcntl.lockf(self.f, fcntl.LOCK_EX)
        self.cur_value = None
        self.new_value = None

    def get(self, default=None):
        """Return cookie content, or `default` if there was none."""
        if not self.new and self.cur_value is None:
            self.f.seek(0)
            self.cur_value = self.f.read()
        if not self.cur_value:
            return default
        return self.cur_value

    def set(self, value=None):
        """Set new cookie content, or remove cookie if `value` is None."""
        self.new_value = value
        self.changed = True

    def close(self):
        """Write cookie to disk if it's content has changed."""
        if self.changed and self.new_value != self.cur_value:
            self.f.seek(0)
            self.f.truncate(0)
            self.f.write(self.new_value)
            if not self.new_value.endswith(u'\n'):
                self.f.write(u'\n')
        self.f.close()
        self.f = None
        if (self.new or self.changed) and self.new_value is None:
            os.unlink(self.filename)


@contextmanager
def store(filename, dir=None):
    """Encapsulate init/close into `with` block."""
    c = Cookie(filename, dir)
    yield c
    c.close()
