# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

from .compat import UserDict, open_encoded
from .platform import flock_exclusive
import json
import os


class Cookie(UserDict, object):

    def __init__(self, path):
        super(Cookie, self).__init__()
        self.path = path
        self.fobj = None
        self.new = not os.path.exists(path)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.commit()
        self.close()

    def open(self, mode='a+', encoding=None):
        self.fobj = open_encoded(self.path, mode, encoding=encoding)
        flock_exclusive(self.fobj)
        self.fobj.seek(0)
        try:
            self.data = json.load(self.fobj)
        except ValueError:
            self.data = {}

    def close(self):
        if not self.fobj:
            return
        self.fobj.close()
        if self.new and self.data == {}:
            os.unlink(self.path)
        self.data = {}
        self.fobj = None

    def commit(self):
        if not self.fobj:
            raise IOError('cannot commit closed Cookie', self.path)
        self.fobj.seek(0)
        self.fobj.truncate()
        json.dump(self.data, self.fobj, indent=1)
        self.fobj.flush()
