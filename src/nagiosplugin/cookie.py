# Copyright (c) gocept gmbh & co. kg
# See also LICENSE.txt

"""Persistent dict to remember state between invocations.

Cookies are used to remember file positions, counters and the like
between plugin invocations. It is not intended for substantial amounts
of data. Cookies are serialized into JSON and saved to a state file. We
prefer a plain text format to allow administrators to inspect and edit
its content. See :class:`~nagiosplugin.logtail.LogTail` for an
application of cookies to get only new lines of a continuously growing
file.

Cookies are locked exclusively so that at most one process at a time has
access to it. Changes to the dict are not reflected in the file until
:meth:`Cookie.commit` is called. It is recommended to use Cookie as
context manager to get it opened and committed automatically.
"""

from .compat import UserDict, open_encoded
from .platform import flock_exclusive
import json
import os


class Cookie(UserDict, object):

    def __init__(self, path):
        """Creates a persistent dict to keep state.

        After creation, a cookie behaves like a normal dict.

        :param path: file to save the dict in (state file)
        """
        super(Cookie, self).__init__()
        self.path = path
        self.fobj = None

    def __enter__(self):
        """Allows Cookie to be used as context manager.

        Opens the file and passes a dict-like object into the
        subordinate context. See :meth:`open` for details about opening
        semantics. When the context is left in the regular way (no
        exception raised), the cookie is :meth:`commit`\ ted to disk.

        :yields: open cookie
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.commit()
        self.close()

    def open(self):
        """Reads/creates the state file and initializes the dict.

        If the state file does not exist, it is touched into existence.
        An exclusive lock is acquired to ensure serialized access. If
        :meth:`open` fails to parse file contents, it truncates
        the file before raising an exception. This guarantees that
        plugins will not fail repeatedly when their state files get
        damaged.

        :returns: Cookie object (self)
        :raises ValueError: if the state file is corrupted or does not
            deserialize into a dict
        """
        self.fobj = open_encoded(self.path, 'a+', encoding='ascii')
        flock_exclusive(self.fobj)
        if os.fstat(self.fobj.fileno()).st_size:
            try:
                self.data = self._load()
            except ValueError:
                self.fobj.truncate(0)
                raise
        return self

    def _load(self):
        self.fobj.seek(0)
        data = json.load(self.fobj)
        if not isinstance(data, dict):
            raise ValueError('format error: cookie does not contain dict',
                             self.path, data)
        return data

    def close(self):
        """Closes a cookie and its underlying state file.

        This method has no effect if the cookie is already closed.
        Once the cookie is closed, any operation (like :meth:`commit`)
        will raise an exception.
        """
        if not self.fobj:
            return
        self.data = {}
        self.fobj.close()
        self.fobj = None

    def commit(self):
        """Persists the cookie's dict items in the state file.

        The cookies content is serialized as JSON string and saved to
        the state file. The buffers are flushed to ensure that the new
        content is saved in a durable way.
        """
        if not self.fobj:
            raise IOError('cannot commit closed cookie', self.path)
        self.fobj.seek(0)
        self.fobj.truncate(0)
        json.dump(self.data, self.fobj)
        self.fobj.write('\n')
        self.fobj.flush()
        os.fsync(self.fobj)
