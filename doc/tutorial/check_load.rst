Tutorial #2: check_load
=======================

In this tutorial, we will discuss important basic features that are present in
nearly every check. These include command line processing, metric evaluation
with scalar contexts, status line formatting and logging.

The :program:`check_load` plugin resembles the one found in the standard Nagios
plugins collection. It allows to check the system load average against
thresholds.


Data acquisition
----------------

First, we will subclass :py:class:`Resource` to generate metrics for the 1,
5, and 15 minute load averages.

.. literalinclude:: /../src/examples/check_load.py
   :start-after: import re
   :end-before: class LoadSummary

:program:`check_load` has two modes of operation: the load averages may either
be takes as read from the kernel or normalized by cpu. Accordingly, the
:py:meth:`Load()` constructor has a parameter two switch normalization on.

In the :py:meth:`Load.probe` method the check reads the load averages from the
:file:`/proc` filesystem and extracts the interesting values. For each value, a
:py:class:`Metric` object is returned. Each metric has a generated name
("load1", "load5", "load15") and a value. We don't declare a unit of measure
since load averages come without unit. All metrics will share the same context
"load" which means that the thresholds for all three values will be the same.

Note that deriving the number of CPUs from :file:`/proc` is a little bit messy
and deserves an extra method. Resource classes may encapsulate arbitrary complex
measurement logic as long they define a :py:meth:`Resource.probe` method that
returns a list of metrics. In the code example shown above, we sprinkle some
logging statements which show effects when the check is called with an increased
logging level (discussed below).


Evaluation
----------

The :program:`check_load` plugin should accept warning and critical ranges and
determine if any load value is outside these ranges. Since this kind of logic is
pretty standard for most of all Nagios/Icinga plugins,
:py:mod:`nagiosplugin` provides a generalized context class for it. It is
the :py:class:`ScalarContext` class which accepts a warning and a critical range
as well as a template to present metric values in a human-readable way.

When :py:class:`ScalarContext` is sufficient, it may be configured during
instantiation right in the :py:func:`main` function. A first version of
the :py:func:`main` function looks like this:

.. code-block:: python

   def main():
       argp = argparse.ArgumentParser(description=__doc__)
       argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                         help='return warning if load is outside RANGE')
       argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                         help='return critical if load is outside RANGE')
       argp.add_argument('-r', '--percpu', action='store_true', default=False)
       args = argp.parse_args()
       check = nagiosplugin.Check(
           Load(args.percpu),
           nagiosplugin.ScalarContext('load', args.warning, args.critical))
       check.main()

Note that the context name "load" is referenced by all three metrics returned by
the :py:meth:`Load.probe` method.

This version of :program:`check_load` is alreday functional, but the output is a
little bit awkward:

.. code-block:: bash
   :linenos:

   $ ./check_load.py
   LOAD OK - load1 is 0.11
   | load15=0.21;;;0 load1=0.11;;;0 load5=0.18;;;0
   $ ./check_load.py -c 0.1:0.2
   LOAD CRITICAL - load1 is 0.23 (outside range 0.1:0.2)
   | load15=0.22;;0.1:0.2;0 load1=0.23;;0.1:0.2;0 load5=0.2;;0.1:0.2;0
   # exit status 2
   $ ./check_load.py -c 0.1:0.2 -r
   LOAD OK - load1 is 0.115
   | load15=0.11;;0.1:0.2;0 load1=0.115;;0.1:0.2;0 load5=0.1;;0.1:0.2;0

In the first invocation (lines 1-3), :program:`check_load` reports only the
first load value which looks a little bit arbitrary. In the second invocation
(lines 4-7), we set a critical threshold. The range specification is parsed
automatically according to the Nagios plugin API and the first metric that lies
outside is reported. In the third invocation (lines 8-10), we request
normalization and all values fit in the range now.
