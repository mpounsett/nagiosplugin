.. _tutorial:

*****************************
First steps with nagiosplugin
*****************************

This tutorial will guide you through all important steps of writing a check with
the :py:mod:`nagiosplugin` class library. Read this to get started.

:py:mod:`nagiosplugin` has a fine-grained class model of classes with a single
responsibility each. This allows plugin writes to focus on one particular tasks
at a time while writing plugins. These are the most important classes and their
relationships::

                +----------+
                | Resource |
                +----------+
          _____/     |      \_____
         v           v            v
   +---------+   +---------+   +---------+
   | Metric  |   | Metric  |   | Metric  |
   +---------+   +---------+   +---------+
        |             |             |
        v             v             v
   +---------+   +---------+   +---------+
   | Context |   | Context |   | Context |
   +---------+   +---------+   +---------+
        |             |             |
        v             v             v
   +---------+   +---------+   +---------+
   | Result  |   | Result  |   | Result  |
   +---------+   +---------+   +---------+
              \___    |    ___/
                  v   v   v
                 +---------+
                 | Summary |
                 +---------+

Resource
   A model of the thing being monitored. It should usually have the same name than
   the whole plugin. Generates one or more metrics.

Metric
   A single measured data point. A metric consists of a name, a value, a unit,
   and optional minimum and maximum bounds. Metrics are numeric in many cases.

Context
   Additional information to evaluate a metric. A context has usually a warning
   and critical range which allows to determine if a given metric is OK or not.
   Contexts also include information on how to present a metric in a
   human-readable way.

Result
   Product of a metric and a context. A result consists of a state ("ok",
   "warning", "critical", "unknown") and some explanatory text.

Summary
   Condenses all results in a single status line. The status line is the
   plugin's most important output: it appears in mails, text messages,
   pager alerts etc.

Read the following tutorials which will guide you through the most important
features of :py:mod:`nagiosplugin` in increasing order of complexity.

.. toctree::

   check_load

.. vim: set spell spelllang=en:
