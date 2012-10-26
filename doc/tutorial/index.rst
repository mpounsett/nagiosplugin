.. _tutorials:

*****************************
First steps with nagiosplugin
*****************************

This tutorial will guide you through all important steps of writing a check with
the :py:mod:`nagiosplugin` class library. Read this to get started.

Key concepts
============

:py:mod:`nagiosplugin` has a fine-grained class model with clear separation of
concerns. This allows plugin writers to focus on one
particular tasks at a time while writing plugins. Nagios/Icinga plugins need to
perform three tasks: data acquisition, evaluation, and presentation. Each task
has an associated class (Resource, Context, Summary) and information between
tasks is passed with structured value objects (Metric, Result).

Classes overview
================

Here is a diagram with the most important classes and their relationships::

                +----------+                \
                | Resource |                 |
                +----------+                 |
          _____/      |     \_____           | Acquisition
         v            v           v          |
   +---------+   +---------+   +---------+   |
   | Metric  |...| Metric  |...| Metric  |  <
   +---------+   +---------+   +---------+   |
        |             |             |        |
        v             v             v        |
   +---------+   +---------+   +---------+   |
   | Context |...| Context |...| Context |   | Evaluation
   +---------+   +---------+   +---------+   |
        |             |             |        |
        v             v             v        |
   +---------+   +---------+   +---------+   |
   | Result  |...| Result  |...| Result  |  <
   +---------+   +---------+   +---------+   |
              \___    |    ___/              |
                  v   v   v                  | Presentation
                 +---------+                 |
                 | Summary |                 |
                 +---------+                /

Resource
   A model of the thing being monitored. It should usually have the same name
   as the whole plugin. Generates one or more metrics.

   *Example: system load*

Metric
   A single measured data point. A metric consists of a name, a value, a unit,
   and optional minimum and maximum bounds. Most metrics are scalar (the value
   can be represented as single number).

   *Example: load1=0.75*

Context
   Additional information to evaluate a metric. A context has usually a warning
   and critical range which allows to determine if a given metric is OK or not.
   Contexts also include information on how to present a metric in a
   human-readable way.

   *Example: warning=0.5, critical=1.0*

Result
   Product of a metric and a context. A result consists of a state ("ok",
   "warning", "critical", "unknown"), some explanatory text, and references to
   the objects that it was generated from.

   *Example: WARNING - load1 is 0.75*

Summary
   Condenses all results in a single status line. The status line is the
   plugin's most important output: it appears in mails, text messages,
   pager alerts etc.

   *Example: LOAD WARNING - load1 is 0.75 (greater than 0.5)*

The following tutorials which will guide you through the most important
features of :py:mod:`nagiosplugin`.

Tutorials
=========

.. toctree::

   check_world
   check_load

.. vim: set spell spelllang=en:
