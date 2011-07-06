.. Copyright (c) 2011 gocept gmbh & co. kg
.. _generating_output:

Generating Output
=================

.. index:: output

Much of the gory details of generating and formatting :term:`Nagios plugin API`
compliant output are handled by :py:mod:`nagiosplugin`. In the simplest case, we
leave :term:`range` checking and :term:`performance data` generation to the
built-in methods and define just the string returned when everything is OK::

   def default_message(self):
      return '/ is %i%% full' % (self.usage)

The optional :py:meth:`Check.states` and :py:meth:`Check.performances` methods
should return arrays of :py:class:`State` objects respective performance
strings.  The :py:class:`Controller` class reduces the states of all measures
(if there is more than one) to the dominant state, which determines the plugin's
output.  In case of an exception, UNKNOWN state is output.

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

To create arrays of similar measures automatically, see also the shortcuts
described in :ref:`multiple_measures`.
