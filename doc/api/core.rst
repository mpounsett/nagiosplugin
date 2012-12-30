Core classes
============

The following classes constitute the core of the :mod:`nagiosplugin` library.
All plugin authors need to use them in the majority of cases. Note that objects
of some of the following classes will be created implicitly as result by methods
of other core classes. For example, calling
:meth:`~nagiosplugin.check.Check.__call__` will create
:class:`~nagiosplugin.result.Result` and
:class:`~nagiosplugin.performance.Performance` objects.

.. note::

   All classes that plugin authors typically need are imported directly into the
   :mod:`nagiosplugin` name space. For example, use ::

      import nagiosplugin
      # ...
      check = nagiosplugin.Check()

   to get a :class:`~nagiosplugin.check.Check` instance.


Check
-----

.. currentmodule:: nagiosplugin.check

.. autoclass:: Check

   .. automethod:: __call__

   .. attribute:: results

      :class:`~nagiosplugin.result.Results` container that allows accessing the
      :class:`~nagiosplugin.result.Result` objects generated during the
      evaluation.

   .. attribute:: perfdata

      List of strings representing a single bit of performance data each.


Resource
--------

.. currentmodule:: nagiosplugin.resource

.. autoclass:: Resource


Metric
------

.. currentmodule:: nagiosplugin.metric

.. autoclass:: Metric

   .. automethod:: __new__
   .. automethod:: __str__


Context
-------

.. currentmodule:: nagiosplugin.context

.. autoclass:: Context


ScalarContext
-------------

.. autoclass:: ScalarContext


State
-----

ServiceState
^^^^^^^^^^^^

.. currentmodule:: nagiosplugin.state

.. autoclass:: ServiceState

   .. automethod:: __str__
   .. automethod:: __int__

.. note::

   :class:`ServiceState` is not imported into the :mod:`nagiosplugin`
   top-level name space since there is usually no need to access it directly.


State subclasses
^^^^^^^^^^^^^^^^

The state subclasses are singletons. Plugin authors should just use the class
name to access the instance. For example::

   check_state = nagiosplugin.Critical


.. autoclass:: nagiosplugin.state.Ok
.. autoclass:: nagiosplugin.state.Warn
.. autoclass:: nagiosplugin.state.Critical
.. autoclass:: nagiosplugin.state.Unknown


Performance
-----------

.. currentmodule:: nagiosplugin.performance

Performance data are created during metric evaluation in a context and are
written into the *perfdata* section of the plugin's output.
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


Summary
-------

.. currentmodule:: nagiosplugin.summary

.. autoclass:: Summary

.. vim: set spell spelllang=en:
