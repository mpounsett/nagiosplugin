********
API docs
********

.. module:: nagiosplugin

The :mod:`nagiosplugin` module consists of several submodules which are
discussed in detail as follows. All classes you need to write plugins are
imported directly to the nagiosplugin top-level name space, so ::

   import nagiosplugin

should be sufficient to access the functionality.

All relevant classes are documented below in alphabetical order. Refer to the
":ref:`tutorials`" section for an introduction on how to use them for typical
use cases.

.. toctree::
   :maxdepth: 1

   check
   resource
   metric
   context
   summary

.. Style
   * Talk about class/method/attribute in third person.
   * Involved personas: 1. plugin authors, 2. library developers
   * Address the documentation reader in second person, i.e. while referring to
     another section.
   * Use RFC2119 keywords where appropriate.

.. vim: set spell spelllang=en:
