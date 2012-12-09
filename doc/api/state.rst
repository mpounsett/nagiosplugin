nagiosplugin.state
==================

.. automodule:: nagiosplugin.state
   :no-members:

The singletons :class:`Ok`, :class:`Warn`, :class:`Critical`, and
:class:`Unknown` are imported into the main :mod:`nagiosplugin` name space. The
:class:`ServiceState` base class is not since it is usually
not needed by plugin authors.


ServiceState
------------

.. autoclass:: nagiosplugin.state.ServiceState

State subclasses
----------------

The state subclasses are singletons. Plugin authors should just use the class
name to access the instance. Example::

   check_state = nagiosplugin.Critical


.. autoclass:: nagiosplugin.state.Ok
.. autoclass:: nagiosplugin.state.Warn
.. autoclass:: nagiosplugin.state.Critical
.. autoclass:: nagiosplugin.state.Unknown

.. vim: set spell spelllang=en:

