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


nagiosplugin.metric
-------------------

.. automodule:: nagiosplugin.metric
   :no-members:

.. autoclass:: Metric

   .. automethod:: __new__
   .. automethod:: __str__


nagiosplugin.state
------------------

.. automodule:: nagiosplugin.state
   :no-members:

.. autoclass:: ServiceState

   .. automethod:: __str__
   .. automethod:: __int__

.. note::

   :class:`ServiceState` is not imported into the :mod:`nagiosplugin`
   top-level name space since there is usually no need to access it directly.

.. autofunction:: nagiosplugin.state.worst

State subclasses
^^^^^^^^^^^^^^^^

The state subclasses are singletons. Plugin authors should use the class
name (without parentheses) to access the instance. For example::

   state = nagiosplugin.Critical


.. autoclass:: nagiosplugin.state.Ok
.. autoclass:: nagiosplugin.state.Warn
.. autoclass:: nagiosplugin.state.Critical
.. autoclass:: nagiosplugin.state.Unknown


nagiosplugin.performance
------------------------

.. automodule:: nagiosplugin.performance
   :no-members:

.. autoclass:: Performance

   .. automethod:: __new__
   .. automethod:: __str__


nagiosplugin.range
------------------

.. automodule:: nagiosplugin.range
   :no-members:

.. autoclass:: Range

   .. automethod:: __new__
   .. automethod:: __str__
   .. automethod:: __repr__


nagiosplugin.result
-------------------

.. automodule:: nagiosplugin.result
   :no-members:

.. autoclass:: Result

   .. automethod:: __new__
   .. automethod:: __str__

.. autoclass:: ScalarResult

.. autoclass:: Results

   .. automethod:: __iter__
   .. automethod:: __len__
   .. automethod:: __getitem__
   .. automethod:: __contains__
