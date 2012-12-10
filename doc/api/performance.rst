nagiosplugin.performance
========================

.. automodule:: nagiosplugin.performance
   :no-members:

Performance data are created during metric evaluation in a context and are
output in the perfdata section. They are used for automatic postprocessing, for
example by graphing packages. Please note that for sake of consistency,
performance data should represent their values in their respective base unit, so
`Performance('size', 10000, 'B')` is better than `Performance('size', 10,
'kB')`.

The :class:`Performance` class is imported into the main :mod:`nagiosplugin`
name space.


Performance
-----------

.. autoclass:: nagiosplugin.performance.Performance
   :special-members: __str__

.. vim: set spell spelllang=en:

