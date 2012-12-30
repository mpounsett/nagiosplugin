.. _core-api:

Core API
========

The core API consists of all functions and classes which are typically called in
the `main` function of a plugin. A typical plugin has a :func:`guarded` main
function that creates a :class:`~nagiosplugin.check.Check` instance. The check
instance is fed with instances of :class:`~nagiosplugin.resource.Resource`,
:class:`~nagiosplugin.context.Context`, or
:class:`~nagiosplugin.summary.Summary` (respective custom subclasses). Finally,
control is passed to the check's :meth:`~nagiosplugin.check.Check.__call__`
method.

.. note::

   All classes that plugin authors typically need are imported directly into the
   :mod:`nagiosplugin` name space. For example, use ::

      import nagiosplugin
      # ...
      check = nagiosplugin.Check()

   to get a :class:`~nagiosplugin.check.Check` instance.


nagiosplugin module-level functions
-----------------------------------

.. currentmodule:: nagiosplugin.runtime

.. autofunction:: guarded


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


Context
-------

.. currentmodule:: nagiosplugin.context

.. autoclass:: Context

.. autoclass:: ScalarContext


Summary
-------

.. currentmodule:: nagiosplugin.summary

.. autoclass:: Summary

.. vim: set spell spelllang=en:
