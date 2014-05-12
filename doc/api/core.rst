.. _core-api:

Core API
========

The core API consists of all functions and classes which are called in
a plugin's `main` function. A typical main function is decorated with
:func:`~nagiosplugin.runtime.guarded` and creates a
:class:`~nagiosplugin.check.Check` object. The check instance is fed with
instances of :class:`~nagiosplugin.resource.Resource`,
:class:`~nagiosplugin.context.Context`, or
:class:`~nagiosplugin.summary.Summary` (respective custom subclasses). Finally,
control is passed to the check's :meth:`~nagiosplugin.check.Check.main` method.

.. note::

   All classes that plugin authors typically need are imported into the
   :mod:`nagiosplugin` name space. For example, use ::

      import nagiosplugin
      # ...
      check = nagiosplugin.Check()

   to get a :class:`~nagiosplugin.check.Check` instance.


nagiosplugin.check
------------------

.. automodule:: nagiosplugin.check
   :no-members:

.. autoclass:: Check

   .. automethod:: __call__

   .. attribute:: name

      Short name which is used to prefix the check's status output (as commonly
      found in plugins shipped with Nagios). It defaults to the uppercased class
      name of the first resource added. However, plugin authors may override
      this by assigning an user-defined name. If this attribute is None, status
      output will not be prefixed with a check name.

   .. attribute:: results

      :class:`~nagiosplugin.result.Results` container that allows accessing the
      :class:`~nagiosplugin.result.Result` objects generated during the
      evaluation.

.. topic:: Example: Skeleton main function

   The following pseudo code outlines how :class:`Check` is typically used in
   the main function of a plugin::

      def main():
         check = nagiosplugin.Check(MyResource1(...), MyResource2(...),
                                    MyContext1(...), MyContext2(...),
                                    MySummary(...))
         check.main()


nagiosplugin.resource
---------------------

.. automodule:: nagiosplugin.resource
   :no-members:

.. autoclass:: Resource


nagiosplugin.context
--------------------

.. automodule:: nagiosplugin.context
   :no-members:

.. autoclass:: Context

.. autoclass:: ScalarContext

.. topic:: Example ScalarContext usage

   Configure a ScalarContext with warning and critical ranges found in
   ArgumentParser's result object `args` and add it to a check::

      c = Check(..., ScalarContext('metric', args.warning, args.critical), ...)


nagiosplugin.summary
--------------------

.. automodule:: nagiosplugin.summary
   :no-members:

.. autoclass:: Summary


nagiosplugin.runtime
--------------------

.. automodule:: nagiosplugin.runtime
   :no-members:

.. autofunction:: guarded

.. vim: set spell spelllang=en:
