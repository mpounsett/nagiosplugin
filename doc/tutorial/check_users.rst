.. _tut3:

.. currentmodule:: nagiosplugin

Tutorial #3: check_users
========================

In the third tutorial, we will learn how to process multiple metrics. Apart from
that, we will see how to use logging and verbosity levels.


Multiple metrics
----------------

A plugin can perform several measurements at once. This is often necessary to
perform more complex state evaluations or improve latency. Consider a check that
determines both the number of total logged in users and the number of unique
logged in users.

A Resource implementation could look like this:

.. code-block:: python

   class Users(nagiosplugin.Resource):

       def __init__(self):
           self.users = []
           self.unique_users = set()

       def list_users(self):
           """Return logged in users as list of user names."""
           [...]
           return users

       def probe(self):
           """Return both total and unique user count."""
           self.users = self.list_users()
           self.unique_users = set(self.users)
           return [nagiosplugin.Metric('total', len(self.users), min=0,
                                       context='users'),
                   nagiosplugin.Metric('unique', len(self.unique_users), min=0,
                                       context='users')]

The `probe()` method returns a list containing two metric objects.
Alternatively, the `probe()` method can act as generator and yield
metrics:

.. code-block:: python

   def probe(self):
       """Return both total and unique user count."""
       self.users = self.list_users()
       self.unique_users = set(self.users)
       yield nagiosplugin.Metric('total', len(self.users), min=0,
                                 context='users')
       yield nagiosplugin.Metric('unique', len(self.unique_users), min=0,
                                 context='users')]

This may be more comfortable than constructing a list of metrics first and
returning them all at once.

Note that both metrics in the example use the same context *users*. This way,
the main function needs to define only one context that provides the same
thresholds for both metrics:

.. code-block:: python

   @nagiosplugin.guarded
   def main():
       argp = argparse.ArgumentParser()
       [...]
       args = argp.parse_args()
       check = nagiosplugin.Check(
           Users(),
           nagiosplugin.ScalarContext('users', args.warning, args.critical,
                                      fmt_metric='{value} users logged in'))
       check.main()


Multiple contexts
-----------------

The above example defines only one context for all metrics. This may not be
practical. Each metric should get its own context now.
In the simplest case we can rely on the fact that each metric takes by default a
context with the same name as the metric itself. So just leave out the
`context=` parameters:

.. code-block:: python

   def probe(self):
       [...]
       return [nagiosplugin.Metric('total', len(self.users), min=0),
               nagiosplugin.Metric('unique', len(self.unique_users), min=0)]

Of course, we need to define two contexts names "total" and "unique" in the
`main()` function:

.. code-block:: python

   @nagiosplugin.guarded
   def main():
       [...]
       args = argp.parse_args()
       check = nagiosplugin.Check(
           Users(),
           nagiosplugin.ScalarContext('total', args.warning, args.critical,
                                      fmt_metric='{value} users logged in'),
           nagiosplugin.ScalarContext(
               'unique', args.warning_unique, args.critical_unique,
               fmt_metric='{value} unique users logged in'))
       check.main(args.verbose, args.timeout)

Alternatively, we can require every context that fits in metric definitions.


Logging and verbose levels
--------------------------

`nagiosplugin` integrates with the `logging`_ module from Python's standard
library. If the main function is decorated with `guarded` (which is heavily
recommended), the logging module gets automatically configured before the
execution of the `main()` function starts.

Consider the following example check::

   import argparse
   import nagiosplugin
   import logging


   class Logging(nagiosplugin.Resource):

       def probe(self):
           logging.warning('warning message')
           logging.info('info message')
           logging.debug('debug message')
           return [nagiosplugin.Metric('zero', 0, context='default')]


   @nagiosplugin.guarded
   def main():
       argp = argparse.ArgumentParser()
       argp.add_argument('-v', '--verbose', action='count', default=0)
       args = argp.parse_args()
       check = nagiosplugin.Check(Logging())
       check.main(args.verbose)

   if __name__ == '__main__':
       main()

.. TODO:: explain source
.. TODO:: explain output without -v and with one to three -v

.. _logging: http://docs.python.org/3/library/logging.html

.. vim: set spell spelllang=en:
