# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .platform import flock_exclusive

try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict

import json
import os


def open_file(path, mode, buffering=-1, encoding=None):
    """ Helper for opening a file with a specified encoding """
    if not encoding:
        return open(path, mode, buffering=buffering)
    try:
        return open(path, mode, buffering=buffering, encoding=encoding)
    except TypeError:
        import codecs
        return codecs.open(path, mode, encoding, 'strict', buffering)


class Cookie(UserDict, object):

    def __init__(self, path):
        super(Cookie, self).__init__()
        self.path = path
        self.fh = None
        self.new = not os.path.exists(path)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.commit()
        self.close()

    def open(self, mode='a+', encoding=None):
        self.fh = open_file(self.path, mode, 16384, encoding)
        flock_exclusive(self.fh)
        self.fh.seek(0)
        try:
            self.data = json.load(self.fh)
        except ValueError:
            self.data = {}

    def close(self):
        if not self.fh:
            return
        self.fh.close()
        if self.new and self.data == {}:
            os.unlink(self.path)
        self.data = {}
        self.fh = None

    def commit(self):
        self.fh.seek(0)
        self.fh.truncate()
        json.dump(self.data, self.fh, indent=1)
        self.fh.flush()
