nagiosplugin.check
==================

.. automodule:: nagiosplugin.check
   :no-members:

The :class:`Check` class is imported into the main :mod:`nagiosplugin` name
space so there is no need to import :mod:`nagiosplugin.check`.


Check
-----

.. autoclass:: nagiosplugin.check.Check

   .. automethod:: __call__

   .. attribute:: results

      :class:`Results` container that allows accessing the :class:`Result`
      objects generated during the evaluation.

   .. attribute:: perfdata

      List of strings representing a single bit of performance data each.

.. vim: set spell spelllang=en:
