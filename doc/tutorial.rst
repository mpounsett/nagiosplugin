.. _tutorial:

********
Tutorial
********

Class Anatomy
=============

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
==============

Override the :py:meth:`obtain_data` method to perform the actual measurement.
To obtain the disk usage, we use the standard :py:func:`os.statvfs` call::

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.usage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         '/', self.usage, '%', self.warning, self.critical, 0, 100)]

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
=================

Much of the gory details of generating and formatting plugin API compliant
output are handled by :py:mod:`nagiosplugin`. In the simplest case, we leave
:term:`range` checking and :term:`performance data` generation to the built-in
methods and define just the string returned when everything is OK::

   def default_message(self):
      return '/ is %i%% full' % (self.usage)

The optional :py:meth:`states` and :py:meth:`performances` methods should return
arrays of :py:class:`State` objects respective performance strings.  The
:py:class:`Controller` class reduces the states of all measures (if there is
more than one) to the dominant state, which determines the plugin's output.  In
case of an exception, UNKNOWN state is output.

.. hint::

   For now, it is sufficient to go with the default implementations, which
   mainly rely mainly on :py:meth:`Measure.state` and
   :py:meth:`Measure.performance`.  In more complicated cases, the default
   methods can be overridden.  The default implementation of these methods is
   roughly equivalent to::

      def states(self):
         return [m.state() for m in self.measures]

      def performances(self):
         return [m.performance() for m in self.measures]

   :py:class:`Measure` objects derive their check state (OK, WARNING, CRITICAL)
   automatically from their value and their warning/critical ranges. Likewise,
   the performance strings are constructed automatically.

.. todo::

   Add link to multiple measures section.


Plugin Options
==============

Of course, static range for the warning and critical thresholds are not very
flexible. To gain flexibility, we add some options. This is done in the
:my:meth:__init__ method. The :py:meth::`__init__` method get two additional
parameters: an :py:class:`OptionParser` and a :py:class:`Logger` object. These
two come from the standard librarie's :py:mod:`optionparser` and
:py:mod:`logging` modules. The :py:class:`OptionParser` object may be used to
define addition option in addition to the standard options like :option:`--help`
or :option:`--version`.

.. todo::

   Add link to logging section.

We define option for warning and critical ranges in the :py:meth:`__init__`
method, but do not use the logging facility for now::

   def __init__(self, optparser, logger):
      optparser.description = 'Check disk usage of the root partition'
      optparser.version = '0.1'
      optparser.add_option(
         '-w', '--warning', default='50', metavar='RANGE',
         help='warning threshold (default: %default%)')
      optparser.add_option(
         '-c', '--critical', default='75', metavar='RANGE',
         help='warning threshold (default: %default%)')

After plugin initialization is complete, the :py:class:`Controller` passes the
parsed options and positional arguments to the plugin via the
:py:meth:`process_args` method. Here, we store them::

   def process_args(self, options, args):
      self.warning = options.warning.rstrip('%')
      self.critical = options.critical.rstrip('%')

Note the option postprocessing: As users may append a percent mark to the
thresholds, we perform a option postprocessing step here to remove it.

Of course, the static thresholds in :py:meth:`obtain_data` must now be replaced
with the user-defined ones. The re-worked method read like this::

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.usage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         '/', self.usage, '%', self.warning, self.critical, 0, 100)]

Congratulations! Our basic disk usage plugin is now complete.  For example, when
called as :command:`check_disk`, it returns OK state due on a computer with a
root partition that is sufficiently free::

   $ python ./check_disk.py
   CHECK OK - / is 7% full | /=7%;50;75;0;100

If we call it like :command:`check_disk -w 5` to set a tighter range for the
warning threshold, it returns warning state::

   $ python ./check_disk.py -w 5
   CHECK WARNING - / value 7% exceeds warning range 5 | /=7%;5;75;0;100

At least, using the pre-defined help option generated a nicely formatted help
page::

   $ python examples/check_disk.py --help
   Usage: check_disk.py [options]

   Check disk usage of the root partition

   Options:
     -h, --help            show this help message and exit
     -V, --version         print version and exit
     -v, --verbose         increase output verbosity (up to 3 times)
     -t TIMEOUT, --timeout=TIMEOUT
                           abort execution after TIMEOUT seconds (default: 15)
     -w RANGE, --warning=RANGE
                           warning threshold (default: 50%)
     -c RANGE, --critical=RANGE
                           warning threshold (default: 75%)

We have now come to the end of our tutorial. Try yourself in enhancing our basic
check, like adding another option to select the partition. The next sections
cover more advaned topics like logging, processing multiple measures and more.
