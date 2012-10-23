.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   unit of measure
      Property of Nagios measure which is returned in
      :term:`Performance Data` and is used for example as axis label in
      performance graphs.

   uom
      See :term:`Unit of Measure`.

   performance data
      Part of the plugin output which is passed to external programs by Nagios.

   range
      String notation defined in the :term:`Nagios plugin API` to express a set
      of acceptable values. Values outside a range trigger a warning or critical
      condition.

   Nagios plugin API
      Documents that define how a Nagios/Icinga compatible plugin must be called
      and how it should respond. There is a `main document`_ and an appendix for
      `Nagios 3 extensions`_.

.. _main document: http://nagiosplug.sourceforge.net/developer-guidelines.html
.. _Nagios 3 extensions: http://nagios.sourceforge.net/docs/3_0/pluginapi.html
