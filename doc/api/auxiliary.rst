.. _auxiliary-classes:

Auxiliary Classes
=================

nagiosplugin's auxiliary classes are not strictly required to write checks, but
simplify common tasks and provide convenient access to functionality that is
regularly needed by plugin authors.

.. note::

   All classes that plugin authors typically need are imported directly into the
   :mod:`nagiosplugin` name space. For example, use ::

      import nagiosplugin
      # ...
      with nagiosplugin.Cookie(path) as cookie:
         # ...

   to get a cookie.


Cookie
------

.. currentmodule:: nagiosplugin.cookie

.. autoclass:: Cookie

   .. automethod:: __enter__

.. topic:: Cookie example

   Increment a connection count saved in the cookie by `self.new_conns`::

      with nagiosplugin.Cookie(self.statefile) as cookie:
         connections = cookie.get('connections', 0)
         cookie['connections'] += self.new_conns


LogTail
-------

.. currentmodule:: nagiosplugin.logtail

.. autoclass:: LogTail

   .. automethod:: __enter__

.. topic:: LogTail example

   Calls `process()` for each new line in a log file::

      cookie = nagiosplugin.Cookie(self.statefile)
      with nagiosplugin.LogTail(self.logfile, cookie) as newlines:
         for line in newlines:
            process(line.decode())

.. vim: set spell spelllang=en:
