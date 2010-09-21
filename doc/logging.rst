.. _logging:

Logging
=======

When something does not work as expected, plugins should provide diagnostic
output. Since the :term:`Nagios plugin API` requires the status line always
first, simply putting print statements in the plugin code is not an option.

:py:mod:`nagiosplugin` provides a :py:class:`Logger` object which is passed to
the check constructor. To use throughout the plugin, a reference can be saved::

    def __init__(self, optparser, logger):
      ...
      self.log = logger

The standard :py:meth:`Logger.debug`, :py:meth:`Logger.info` and
:py:meth:`Logger.warn` methods may be used to record messages of different
importance levels::

   self.log.debug('frobbing foo with bar')
   self.log.info('system call result is baz')
   self.log.warn('something is fishy about qux!')

The check may be invoked with the predefined :option:`--verbose` (or
:option:`-v` for short) command line option to increase the output level.
:option:`-v` displays all ``warn`` messages along with stack traces for
uncaught exceptions. Stack traces are suppressed by default. :option:`-vv` and
:option:`-vvv` display ``warn`` and ``debug`` messages, respectively.

Log messages output with :py:meth:`Logger.error` are displayed regardless on the
number of :option:`-v` options.
