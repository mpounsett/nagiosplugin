# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

from .platform import flock_exclusive
import json
import os


class Cookie:

    def __init__(self, path):
        self.path = path
        self.new = not os.path.exists(path)
        self.fh = None
        self.value = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.commit()
        self.close()

    def open(self):
        self.fh = open(self.path, 'a+')
        flock_exclusive(self.fh)
        self.fh.seek(0)
        try:
            self.value = json.load(self.fh)
        except ValueError:
            self.value = {}

    def close(self):
        if not self.fh:
            return
        self.fh.close()
        if self.new and self.value == {}:
            os.unlink(self.path)
        self.value = None
        self.fh = None

    def commit(self):
        self.fh.seek(0)
        self.fh.truncate()
        json.dump(self.value, self.fh, indent=1)

    def get(self, key, default=None):
        try:
            return self.value[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, newvalue):
        self.value[key] = newvalue

    def __delitem__(self, key):
        del self.value[key]

    def __len__(self):
        return len(self.value)
