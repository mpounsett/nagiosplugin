.. Copyright (c) 2011 gocept gmbh & co. kg
.. _plugin_options:

Plugin Options
==============

.. index::
   pair: command line; options

Of course, static range for the warning and critical thresholds are not very
flexible. To gain flexibility, we add some options. This is done in the
:py:meth:`Check.__init__` method. :py:meth:`Check.__init__` get two
additional parameters: an :py:class:`OptionParser` and a :py:class:`Logger`
object. These two come from the Python standard library's :py:mod:`optionparser`
and :py:mod:`logging` modules. The :py:class:`OptionParser` object may be used
to define addition option in addition to the standard options like
:option:`--help` or :option:`--version`.

We define options for warning and critical ranges in the
:py:meth:`Check.__init__` method, but do not use the logging facility for now::

   def __init__(self, optparser, logger):
      optparser.description = 'Check disk usage of the root partition'
      optparser.version = '0.1'
      optparser.add_option(
         '-w', '--warning', default='50', metavar='RANGE',
         help='warning threshold (default: %default%)')
      optparser.add_option(
         '-c', '--critical', default='75', metavar='RANGE',
         help='warning threshold (default: %default%)')

.. seealso::

   Details on how to use logging are discussed in the :ref:`logging` chapter.

After plugin initialization is complete, the :py:class:`Controller` passes the
parsed options and positional arguments to the plugin via the
:py:meth:`Check.process_args` method. Here, we store them::

   def process_args(self, options, args):
      self.warning = options.warning.rstrip('%')
      self.critical = options.critical.rstrip('%')

Note the option postprocessing: As users may append a percent mark to the
thresholds, we perform a option postprocessing step here to remove it.

Of course, the static thresholds in :py:meth:`Check.obtain_data` must now be
replaced with the user-defined ones. The re-worked method read like this::

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.usage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         '/', self.usage, '%', self.warning, self.critical, 0, 100)]

.. index::
   pair: plugin; invocation

Congratulations! Our basic disk usage plugin is now complete.  For example, when
called as :command:`check_disk_tutorial`, it returns OK state due on a computer
with a root partition that is sufficiently free::

   $ python ./check_disk_tutorial.py
   CHECK OK - / is 7% full | /=7%;50;75;0;100

If we call it like :command:`check_disk_tutorial -w 5` to set a tighter range
for the warning threshold, it returns warning state::

   $ python ./check_disk_tutorial.py -w 5
   CHECK WARNING - / value 7% exceeds warning range 5 | /=7%;5;75;0;100

.. index::
   pair: command line; help

At least, using the pre-defined help option generated a nicely formatted help
page::

   $ python examples/check_disk_tutorial.py --help
   Usage: check_disk_tutorial.py [options]

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
