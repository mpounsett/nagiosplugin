.. _tut3:

.. currentmodule:: nagiosplugin

Tutorial #3: check_users
========================

In the third tutorial, we will learn how to process multiple metrics.
Additionally, we will see how to use logging and verbosity levels.


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

To assign a :class:`~nagiosplugin.context.Context` to a
:class:`~nagiosplugin.metric.Metric`, pass the context's name in the metric's
**context** parameter. Both metrics use the same context "users". This way, the
main function must define only one context that applies the same thresholds to
both metrics:

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
practical. Each metric should get its own context now. By default, a metric is
matched by a context of the same name. So we just leave out the **context**
parameters:

.. code-block:: python

   def probe(self):
       [...]
       return [nagiosplugin.Metric('total', len(self.users), min=0),
               nagiosplugin.Metric('unique', len(self.unique_users), min=0)]

We then define two contexts (one for each metric) in the `main()` function:

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


Logging and verbosity levels
----------------------------

**nagiosplugin** integrates with the `logging`_ module from Python's standard
library. If the main function is decorated with `guarded` (which is heavily
recommended), the logging module gets automatically configured before the
execution of the `main()` function starts. Messages logged to the *nagiosplugin*
logger (or any sublogger) are processed with nagiosplugin's integrated logging.

Consider the following example check::

   import argparse
   import nagiosplugin
   import logging

   _log = logging.getLogger('nagiosplugin')


   class Logging(nagiosplugin.Resource):

       def probe(self):
           _log.warning('warning message')
           _log.info('info message')
           _log.debug('debug message')
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

The verbosity level is set in the :meth:`check.main()` invocation depending on
the number of "-v" flags. Let's test this check:

.. code-block:: bash

   $ check_verbose.py
   LOGGING OK - zero is 0 | zero=0
   warning message (check_verbose.py:11)
   $ check_verbose.py -v
   LOGGING OK - zero is 0
   warning message (check_verbose.py:11)
   | zero=0
   $ check_verbose.py -vv
   LOGGING OK - zero is 0
   warning message (check_verbose.py:11)
   info message (check_verbose.py:12)
   | zero=0
   $ check_verbose.py -vvv
   LOGGING OK - zero is 0
   warning message (check_verbose.py:11)
   info message (check_verbose.py:12)
   debug message (check_verbose.py:13)
   | zero=0

When called with *verbose=0,* both the summary and the performance data are
printed on one line and the warning message is displayed. Messages logged with
*warning* or *error* level are always printed.
Setting *verbose* to 1 does not change the logging level but enable multi-line
output. Additionally, full tracebacks would be printed in the case of an
uncaught exception.
Verbosity levels of 2 and 3 enable logging with *info* or *debug* levels.

This behaviour conforms to the "Verbose output" suggestions found in the
`Nagios plug-in development guidelines`_.

It is advisable to sprinkle logging statements in the plugin code, especially
into the resource model classes. A logging example for a users check could look
like this:

.. code-block:: python

   class Users(nagiosplugin.Resource):

       [...]

       def list_users(self):
           """Return list of logged in users."""
           _log.info('querying users with "%s" command', self.who_cmd)
           users = []
           try:
               for line in subprocess.check_output([self.who_cmd]).splitlines():
                   _log.debug('who output: %s', line.strip())
                   users.append(line.split()[0].decode())
           except OSError:
               raise nagiosplugin.CheckError(
                   'cannot determine number of users ({} failed)'.format(
                       self.who_cmd))
           _log.debug('found users: %r', users)
           return users

Interesting items to log are: the command which is invoked to query the
information from the system, or the raw result to verify that parsing works
correctly.

.. _logging: http://docs.python.org/3/library/logging.html

.. _Nagios plug-in development guidelines: http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN39

.. vim: set spell spelllang=en:
