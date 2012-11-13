.. _tut1:

.. currentmodule:: nagiosplugin

Tutorial #1: 'Hello world' check
================================

In the first tutorial, we will develop `check_world`. This check will determine
if the world exists. The algorithm is simple: if the world would not exist, the
check would not execute.

This minimalistic check consists of a :py:class:`Resource` World which models
the part of the world that is interesting for the purposes of our check.
Resource classes must define a :py:meth:`Resource.probe` method which returns a
list of metrics. We just return a single :py:class:`Metric` object that states
that the world exists.

.. literalinclude:: /../src/nagiosplugin/examples/check_world.py

We don't have a context to evaluate the returned metric yet, so we resort to the
built-in "null" context. The "null" context does nothing with its associated
metrics.

We now create a :py:class:`Check` object that is fed only with the resource
object. We could put context and summary objects into the :py:meth:`Check()`
constructor as well. This will be demonstrated in the next tutorial. There is
also no command line processing nor timeout handling nor output control. We call
the :py:meth:`Check.main` method to evaluate resources, construct text output
and exit with the appropriate status code.

Running the plugin creates very simple output:

.. code-block:: bash
   :linenos:

   $ check_world.py
   WORLD OK

The plugin's exit status is 0, signalling success to the calling process.

.. vim: set spell spelllang=en:
