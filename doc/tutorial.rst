.. _tutorial:

Tutorial
========

Class Anatomy
-------------

Plugins written with :py:mod::`nagiosplugin` are subclasses from the
:py:class:`Check` base class, overriding methods to provide
functionality. The methods are called from the :py:class:`Controller` class,
which implements the general plugin control logic.

For instructional purposes, we start writing a very basic plugin that checks the
free space on the root partition. It should return "warning" if the partition is
more than 50% full and "critical" if it is more than 75% full.

To get started, we start with an empty :py:class:`Check` subclass::

   import nagiosplugin
   import os


   class DiskCheck(nagiosplugin.Check):
      pass


   main = nagiosplugin.Controller(DiskCheck)
   if __name__ == '__main__':
      main()

The new plugins functionality will be defined in the class
:py:class:`DiskCheck`. This class is passed to the :py:class:`Controller`'s
constructor which returns the main function. :py:obj:`main` could be used as a
console script entry point or used directly if the script is called from the
command line.


Obtaining Data
--------------

Override the :py:meth:`obtain_data` method to perform the actual measurement.
To obtain the disk usage, we use the standard :py:func:`os.statvfs` call::

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.diskusage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         'diskusage', self.diskusage, '%', '0:50', '0:75', 0, 100)]

Much of the tiresome parts of writing Nagios plugins by hand is capsuled in the
:py:class:`Measure` class. The Measure class is initialized with the check name,
the measured numerical value, the :term:`unit of measure`,
the warning and critical thresholds expressed as standard Nagios :term:`range`,
and the allowed minimum/maximum values.

The array of :py:class:`Measure` values is held in the :py:obj:`measures`
attribute.  This is merely a convention used to harness the predefined output
generation methods in the :py:class:`Check` base class, as described in the next
section.


Generating Output
-----------------

Much of the gory details of generating and formatting plugin API compliant
output are handled by :py:mod:`nagiosplugin`. In the simplest case, we leave
:term:`range` checking and :term:`performance data` generation to the built-in
methods and define just the string returned when everything is OK::

   def default_message(self):
      return 'root partition is %i%% full' % (self.diskusage)

The optional :py:meth:`states` and :py:meth:`performances` methods should return
arrays of :py:class:`State` objects respective performance strings. For now, it
is sufficient to go with the default implementations, which mainly rely mainly
on :py:meth:`Measure.state` and :py:meth:`Measure.performance`.  In more
complicated cases, the default methods can be overridden.  The default
implementation of these methods is roughly equivalent to::

   def states(self):
      return [m.state() for m in self.measures]

   def performances(self):
      return [m.performance() for m in self.measures]

:py:class:`Measure` objects derive their check state (OK, WARNING, CRITICAL)
automatically from their value and their warning/critical ranges. Likewise, the
performance strings are constructed automatically. The :py:class:`Controller`
class reduces the states of all measures (in case of more than one measure) to
the dominant state, which determines the plugin's output. In case of an
exception, UNKNOWN state is output.
