# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import os
import os.path
from contextlib import contextmanager

if os.name == 'nt':
    import msvcrt
    from win32com.shell import shell, shellcon
else:
    import fcntl


class Cookie(object):
    """Status information for plugins that is persisted between runs.

    Nagios Plugins may keep track of details like the last position in a
    logfile etc. Cookie helps with that task: a string is kept between
    runs. The cookie is identified with a file name (the file goes into
    $HOME by default, which is /var/nagios on most systems). The plugin
    is responsible for serializing/deserializing that information.
    Human-readable ASCII text is strongly preferred.
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
            home = os.path.expanduser("~")
            self.filename = os.path.join(os.path.expanduser(home), filename)
        self.new = not os.path.exists(self.filename)
        self.changed = False
        self.f = file(self.filename, 'a+')
        if os.name == 'nt':
            msvcrt.locking(self.f.fileno(), msvcrt.LK_LOCK, 2147483647L)
        else:
            fcntl.flock(self.f, fcntl.LOCK_EX)
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
