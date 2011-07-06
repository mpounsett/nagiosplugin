.. _multiple_measures:

Multiple Measures
=================

Plugins may check multiple measures at once. An example is the load check on
Unix machines: thresholds need to be compared for the 1, 5, and 15 minute
averages.

Creating Multiple Measures
--------------------------

.. index::
   single: measures; multiple

To support multiple measures, instantiate several :py:class:`Measure` objects and
return them as a list at :py:meth:`Check.states` and :py:meth:`Check.performances`.

To reduce coding overhead, the :py:func:`Measure.array` factory returns a list
of similar measure objects. In the load example, all three load measures could
be created with::

   self.data = nagiosplugin.Measure.array(
      names=['load1', 'load5', 'load15'],
      values=self.load,
      warnings=self.warn,
      criticals=self.crit,
      minimums=[0])

The parameters are the same as in :py:meth:`Measure.__init__`, but they take
lists instead of single values. All lists except names and values replicate the
last element if the list is too short. So one could provide one to three
thresholds in the `warnings` and `criticals` parameters. The single element in
the `minimums` parameter illustrates this principle.


Multiple Warning/Critical Thresholds
------------------------------------

The easiest way to provide the user with a flexible way to specify multiple
thresholds is to accept comma-separated lists. In the aforementioned example, a
code line like::

   self.warn = opts.warning.split(',')

can be used in :py:meth:`Check.process_args`. The plugin may now called::

   $ check_load -w 2

as well as::

   $ check_load -w 3,6,9

In the first case, the warning threshold applies to all three load measures. In
the second case, thresholds of 3, 6, and 9 are applied to the 1, 5, and 15
minute load averages.

.. vim: set spell spelllang=en_us:
