.. Copyright (c) 2011 gocept gmbh & co. kg
.. _obtaining_data:

Obtaining Data
==============

.. index::
   single: data
   single: measures; simple

Override the :py:meth:`Check.obtain_data` method to perform the actual
measurement.  To obtain the disk usage, we use the standard
:py:func:`os.statvfs` call::

   def obtain_data(self):
      vfs = os.statvfs('/')
      self.usage = 100 - (100 * vfs.f_bfree / vfs.f_blocks)
      self.measures = [nagiosplugin.Measure(
         '/', self.usage, '%', self.warning, self.critical, 0, 100)]

.. index:: threshold

Much of the tiresome parts of writing Nagios plugins by hand is capsuled in the
:py:class:`Measure` class. The Measure class is initialized with the check name,
the measured numerical value, the :term:`unit of measure`,
the warning and critical thresholds expressed as standard Nagios :term:`range`,
and the allowed minimum/maximum values.

The array of :py:class:`Measure` values is held in the :py:obj:`measures`
attribute.  This is merely a convention used to harness the predefined output
generation methods in the :py:class:`Check` base class, as described in the next
section.


