# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import fcntl
import os
import os.path
from contextlib import contextmanager


class Cookie(object):

    def __init__(self, filename, dir=None):
        if dir:
            self.filename = os.path.join(os.path.abspath(dir), filename)
        else:
            self.filename = os.path.abspath(filename)
        self.new = not os.path.exists(self.filename)
        self.changed = False
        self.f = file(self.filename, 'a+')
        fcntl.lockf(self.f, fcntl.LOCK_EX)
        self.cur_value = None
        self.new_value = None

    def get(self, default=None):
        if not self.new and self.cur_value is None:
            self.f.seek(0)
            self.cur_value = self.f.read()
        if not self.cur_value:
            return default
        return self.cur_value

    def set(self, value=None):
        self.new_value = value
        self.changed = True

    def close(self):
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
    c = Cookie(filename, dir)
    yield c
    c.close()
