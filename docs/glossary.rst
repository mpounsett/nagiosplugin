.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   unit of measure
      Property of a metric which is returned in
      :term:`Performance Data` and is used for example as axis label in
      performance graphs. Nagios plugins should only use base units like *s*,
      *B*, etc. instead of scaled units like *days*, *MiB* etc.

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

   acquisition
      First step of check execution in the context of the nagiosplugin
      library. Data is retrieved from the system under surveillance using custom
      code. This is where the meat of a plugin is. Data acquisition is performed
      by one or more :term:`domain model` objects which are usually
      :class:`~nagiosplugin.resource.Resource` subclasses.

   evaluation
      Second step of check execution in the context of the nagiosplugin library.
      Data generated in the :term:`acquisition` step is evaluated according to
      criteria specified in :class:`~nagiosplugin.context.Context` objects.

   presentation
      Third step of check execution in the context of the nagiosplugin library.
      Outcomes from the :term:`evaluation` step are condensed into a compact
      summary which is suited to inform the admin about relevant system state.
      Data presentation is the responsibility of
      :class:`~nagiosplugin.summary.Summary` objects which also generate the
      :term:`performance data` output section.

   domain model
      One or more classes that abstract the properties of the system under
      surveillance that are relevant for the check. The domain model code should
      not be interspersed with secondary aspects like data representation or
      interfacing with outside monitoring infrastructure.

   perfdata
      See :term:`performance data`.

.. _main document: http://nagiosplug.sourceforge.net/developer-guidelines.html
.. _Nagios 3 extensions: http://nagios.sourceforge.net/docs/3_0/pluginapi.html

.. vim: set spell spelllang=en:
