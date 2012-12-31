# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

"""Access previously unseen parts of a growing text file."""

import os


class LogTail(object):

    def __init__(self, path, cookie):
        self.path = os.path.abspath(path)
        self.cookie = cookie
        self.logfile = None
        self.stat = None

    def seek_if_applicable(self, fileinfo):
        self.stat = os.stat(self.path)
        if (self.stat.st_ino == fileinfo.get('inode', -1) and
                self.stat.st_size >= fileinfo.get('pos', 0)):
            self.logfile.seek(fileinfo['pos'])

    def __enter__(self):
        self.logfile = open(self.path, 'rb')
        self.cookie.open()
        self.seek_if_applicable(self.cookie.get(self.path, {}))
        line = self.logfile.readline()
        while len(line):
            yield line
            line = self.logfile.readline()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.cookie[self.path] = dict(
                inode=self.stat.st_ino, pos=self.logfile.tell())
            self.cookie.commit()
        self.cookie.close()
        self.logfile.close()
