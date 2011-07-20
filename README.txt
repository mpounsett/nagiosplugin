The nagiosplugin library
========================

About
-----

`nagiosplugin` is a class library which helps writing Nagios (or Icinga)
compatible plugins easily in Python. It cares for much of the boilerplate code
and default logic commonly found in Nagios checks, including:

- Nagios 3 Plugin API compliant parameters and output formatting
- Controller to handle the general plugin control flow
- Full Nagios range syntax support
- Automatic threshold checking
- Multiple independend measures and overall state logic
- Long output and performance data
- Timeout handling
- Default options
- Persistent "cookies" to retain state information between check runs.


Feedback and Suggestions
------------------------

`nagiosplugin` is primarily written and maintained by Christian Kauhaus
<kc@gocept.com>. Feel free to contact the author for bugs, suggestions and
patches.

A public issue tracker can be found at
http://projects.gocept.com/projects/projects/nagiosplugin/issues.


License
-------

The `nagiosplugin` package is released the Zope Public License (ZPL), a BSD-style Open Source license.


Documentation
-------------

To get started writing Nagios plugins, see the examples in the :file:`examples`
subdirectory.

More documentation on using this package can be found in the :file:`doc`
directory.  There is also an `online copy`_ of the docs available.

.. _online copy: http://packages.python.org/nagiosplugin/

.. vim: set ft=rst sw=3 sts=3 et:
