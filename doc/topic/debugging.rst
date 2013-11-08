.. _debugging:

.. index:: debugging

Plugin Debugging
================

Debugging plugins can sometimes be complicated since there are so many classes,
which are tied together in an implicit way. I have collected some frequent
questions about debugging.


.. index::
   single: verbose; traceback

An uncaught exception makes the plugin return UNKNOWN. Where is the cause?
--------------------------------------------------------------------------

When your plugin raises an exception, you may get very little output. Example::

   $ check_users.py
   USERS UNKNOWN: RuntimeError: error

Set the **verbose** parameter of :py:meth:`~nagiosplugin.check.Check.main`
to some value greater than zero and you will get the full traceback::

   $ check_users.py -v
   USERS UNKNOWN: RuntimeError: error
   Traceback (most recent call last):
     File "src/nagiosplugin/runtime.py", line 38, in wrapper
       return func(*args, **kwds)
     File "src/nagiosplugin/examples/check_users.py", line 104, in main
       check.main(args.verbose, args.timeout)
     File "src/nagiosplugin/check.py", line 110, in main
       runtime.execute(self, verbose, timeout)
     File "src/nagiosplugin/runtime.py", line 118, in execute
       with_timeout(self.timeout, self.run, check)
     File "src/nagiosplugin/platform/posix.py", line 19, in with_timeout
       func(*args, **kwargs)
     File "src/nagiosplugin/runtime.py", line 107, in run
       check()
     File "src/nagiosplugin/check.py", line 95, in __call__
       self._evaluate_resource(resource)
     File "src/nagiosplugin/check.py", line 73, in _evaluate_resource
       metrics = resource.probe()
     File "src/nagiosplugin/examples/check_users.py", line 57, in probe
       self.users = self.list_users()
     File "src/nagiosplugin/examples/check_users.py", line 34, in list_users
       raise RuntimeError('error')
   RuntimeError: error


A Check constructor dies with "cannot add type <...>"
-----------------------------------------------------

When you see the following exception raised from
:py:meth:`~nagiosplugin.check.Check` (or `Check.add()`)::

   UNKNOWN: TypeError: ("cannot add type <class '__main__.Users'> to check", <__main__.Users object at 0x7f0c64f73f90>)

chances are high that you are trying to add an object that is not an instance
from Resource, Context, Summary, or Results or its subclasses. A common
error is to base a resource class on `object` instead of
:py:class:`~nagiosplugin.resource.Resource`.


.. index:: pdb

I'm trying to use pdb but I get a timeout after 10s
---------------------------------------------------

When using an interactive debugger like pdb on plugins, you may experience that
your debugging session is aborted with a timeout after 10 seconds. Just set the
**timeout** parameter in :py:meth:`~nagiosplugin.check.Check.main` to 0 to avoid
this.


.. vim: set spell spelllang=en:
