.. _intermediate-data-api:

Intermediate data API
=====================

The following classes allow to handle intermediate data that are used during the
plugin's execution in a structured way. Most of them are used by the
:mod:`nagiosplugin` library itself to create objects which are passed into
code written by plugin authors. Other classes (like
:class:`~nagiosplugin.metric.Metric`) are used by plugin authors to generate
intermediate data during :term:`acquisition` or :term:`evaluation` steps.

.. note::

   All classes that plugin authors typically need are imported directly into the
   :mod:`nagiosplugin` name space. For example, use ::

      import nagiosplugin
      # ...
      result = nagiosplugin.Result(nagiosplugin.Ok)

   to get a :class:`~nagiosplugin.result.Result` instance.


Metric
------

.. currentmodule:: nagiosplugin.metric

.. autoclass:: Metric

   .. automethod:: __new__
   .. automethod:: __str__


State
-----

ServiceState base class
^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: nagiosplugin.state

.. autoclass:: ServiceState

   .. automethod:: __str__
   .. automethod:: __int__

.. note::

   :class:`ServiceState` is not imported into the :mod:`nagiosplugin`
   top-level name space since there is usually no need to access it directly.

State subclasses
^^^^^^^^^^^^^^^^

The state subclasses are singletons. Plugin authors should use the class
name (without parentheses) to access the instance. For example::

   check_state = nagiosplugin.Critical


.. autoclass:: nagiosplugin.state.Ok
.. autoclass:: nagiosplugin.state.Warn
.. autoclass:: nagiosplugin.state.Critical
.. autoclass:: nagiosplugin.state.Unknown


Performance
-----------

.. currentmodule:: nagiosplugin.performance

:term:`Performance data` are created during metric evaluation in a context and
are written into the *perfdata* section of the plugin's output.
For sake of consistency, performance data should represent their values in their
respective base unit, so `Performance('size', 10000, 'B')` is better than
`Performance('size', 10, 'kB')`.

.. autoclass:: Performance

   .. automethod:: __new__
   .. automethod:: __str__


Result
------

.. currentmodule:: nagiosplugin.result

The :class:`Result` class is the base class for all evaluation results. The
:class:`ScalarResult` class provides convenient access for the common special
case when evaluating :class:`~nagiosplugin.context.ScalarContext`. The
:class:`Results` class (plural form) provides a result container with access
functions and iterators.

.. autoclass:: Result

   .. automethod:: __new__
   .. automethod:: __str__

.. autoclass:: ScalarResult

.. autoclass:: Results

   .. automethod:: __iter__
   .. automethod:: __len__
   .. automethod:: __getitem__
   .. automethod:: __contains__
