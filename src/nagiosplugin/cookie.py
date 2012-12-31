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

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.commit()
        self.close()

    def open(self):
        self.fobj = open_encoded(self.path, 'a+', encoding='ascii')
        flock_exclusive(self.fobj)
        if not os.fstat(self.fobj.fileno()).st_size:
            # file is empty
            return
        try:
            self.data = self.load()
        except ValueError:
            self.fobj.truncate(0)
            raise

    def load(self):
        self.fobj.seek(0)
        data = json.load(self.fobj)
        if not isinstance(data, dict):
            raise ValueError('format error: cookie does not contain dict',
                             self.path, data)
        return data

    def close(self):
        if not self.fobj:
            return
        self.data = {}
        self.fobj.close()
        self.fobj = None

    def commit(self):
        if not self.fobj:
            raise IOError('cannot commit closed cookie', self.path)
        self.fobj.seek(0)
        self.fobj.truncate(0)
        json.dump(self.data, self.fobj)
        self.fobj.write('\n')
        self.fobj.flush()
        os.fsync(self.fobj)
