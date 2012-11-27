nagiosplugin.state
==================

.. automodule:: nagiosplugin.state
   :no-members:

.. currentmodule:: nagiosplugin

The singletons :class:`Ok`, :class:`Warn`, :class:`Critical`, and
:class:`Unknown` are imported into the main :mod:`nagiosplugin` name space. The
:class:`nagiosplugin.state.ServiceState` base class is not since it is usually
not needed by plugin authors.


ServiceState
------------

.. autoclass:: nagiosplugin.state.ServiceState

State subclasses
----------------

The state subclasses are singletons. Plugin authors should just use the class
name to access the instance. Example::

   check_state = nagiosplugin.Critical


.. autoclass:: nagiosplugin.Ok
.. autoclass:: nagiosplugin.Warn
.. autoclass:: nagiosplugin.Critical
.. autoclass:: nagiosplugin.Unknown

.. vim: set spell spelllang=en:

