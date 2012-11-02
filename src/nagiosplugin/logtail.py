# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

import os


class LogTail(object):

    def __init__(self, path, cookie, mode='r'):
        self.path = os.path.abspath(path)
        self.cookie = cookie
        self.mode = mode
        self.logfile = None
        self.stat = None

    def seek_if_applicable(self, fileinfo):
        self.stat = os.stat(self.path)
        if (self.stat.st_ino == fileinfo.get('inode', -1) and
                self.stat.st_size >= fileinfo.get('pos', 0)):
            self.logfile.seek(fileinfo['pos'])

    def __enter__(self):
        self.logfile = open(self.path, self.mode)
        self.cookie.open()
        self.seek_if_applicable(self.cookie.get(self.path, {}))
        return self.logfile

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.cookie[self.path] = dict(
                inode=self.stat.st_ino, pos=self.logfile.tell())
            self.cookie.commit()
        self.cookie.close()
        self.logfile.close()
