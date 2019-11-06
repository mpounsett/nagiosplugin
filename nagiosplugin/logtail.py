# -*- coding: utf-8 -*-
"""Access previously unseen parts of a growing file.

LogTail builds on :class:`~.cookie.Cookie` to access new lines of a
continuosly growing log file. It should be used as context manager that
provides an iterator over new lines to the subordinate context. LogTail
saves the last file position into the provided cookie object.
As the path to the log file is saved in the cookie, several LogTail
instances may share the same cookie.
"""

import os


class LogTail(object):

    def __init__(self, path, cookie):
        """Creates new LogTail context.

        :param path: path to the log file that is to be observed
        :param cookie: :class:`~.cookie.Cookie` object to save the last
            file position
        """
        self.path = os.path.abspath(path)
        self.cookie = cookie
        self.logfile = None
        self.stat = None

    def _seek_if_applicable(self, fileinfo):
        self.stat = os.stat(self.path)
        if (self.stat.st_ino == fileinfo.get('inode', -1) and
                self.stat.st_size >= fileinfo.get('pos', 0)):
            self.logfile.seek(fileinfo['pos'])

    def __enter__(self):
        """Seeks to the last seen position and reads new lines.

        The last file position is read from the cookie. If the log file
        has not been changed since the last invocation, LogTail seeks to
        that position and reads new lines. Otherwise, the position saved
        in the cookie is reset and LogTail reads from the beginning.
        After leaving the subordinate context, the new position is saved
        in the cookie and the cookie is closed.

        :yields: new lines as bytes strings
        """
        self.logfile = open(self.path, 'rb')
        self.cookie.open()
        self._seek_if_applicable(self.cookie.get(self.path, {}))
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
