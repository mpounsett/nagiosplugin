.. _cookies:

Cookies
=======

.. index:: cookie

The :py:class:`Cookie` class allows plugins to store and retrieve state between
runs.  This can be helpful for example to retain the last file position while
processing log files.


Basic Usage
-----------

Cookies are used to store unstructured information (preferably ASCII content) in
a file between runs. To get a cookie, call::

   mycookie = nagiosplugin.Cookie('filename')

To retrieve and set new content, call :py:meth:`Cookie.get` and
:py:meth:`Cookie.set`. When a new cookie value has been set, no data is written
to disk first. Thus, plugins restart with the old value after a failure.  To
persist the cookie's content, call :py:meth:`Cookie.close`.

As an example, we save a time stamp in a cookie to process
events in non-overlapping time windows::

   cookie = nagiosplugin.Cookie('example_timestamp')
   start = cookie.get()
   if start:
      start = datetime.datetime.strptime(start.strip(), self.ISOFORMAT)
   end = datetime.datetime.now()
   self.process_events(start, end)
   # process_events could raise an exception
   cookie.set(end.strftime(self.ISOFORMAT))
   cookie.close()

Note that the ending time stamp is set before the processing begins. The
processing could take a significant amount of time, resulting in gaps between
the start and end times of successive runs.

:py:meth:`Cookie.get` returns `None` if no cookie exists. In our example, the
`process_events` method should be prepared to accept `None` as start time.


Context Manager Usage
---------------------

.. index::
   pair: cookie; context manager

Cookies can also be used as context manager with Python 2.5 or newer. The
:py:func:`cookie.store` function can be used with a `with` block::

   with nagiosplugin.cookie.store('example_timestamp') as c:
      start = c.get()
      ...

:py:meth:`Cookie.__init__` is called implicitly at the beginning and is passed
all arguments from :py:func:`cookie.store`. :py:meth:`Cookie.close` is called
when the `with` block is left.

.. vim: set spell spelllang=en_us:
