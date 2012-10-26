The nagiosplugin library
========================

About
-----

`nagiosplugin` is a Python class library which helps writing Nagios (or Icinga)
compatible plugins easily in Python. It cares for much of the boilerplate code
and default logic commonly found in Nagios checks, including:

- Nagios 3 Plugin API compliant parameters and output formatting
- Full Nagios range syntax support
- Automatic threshold checking
- Multiple independend measures
- Custom status line to communicate the main point quickly
- Long output and performance data
- Timeout handling
- Persistent "cookies" to retain state information between check runs
- Resume log file processing at the point where the last run left
- No dependencies beyond the Python standard library.

`nagiosplugin` runs on POSIX and Windows systems. It requires Python 3, but
Python 2.7 compatibility is planned.


Feedback and Suggestions
------------------------

`nagiosplugin` is primarily written and maintained by Christian Kauhaus
<kc@gocept.com>. Feel free to contact the author for bugs, suggestions and
patches.

A public issue tracker can be found at
http://projects.gocept.com/projects/nagiosplugin/issues. There is also a forum
available at https://projects.gocept.com/projects/nagiosplugin/boards.


License
-------

The `nagiosplugin` package is released the Zope Public License (ZPL), a
BSD-style Open Source license.


Documentation
-------------

To get started writing Nagios plugins, see the examples in the `examples`
subdirectory.

More documentation on using this package can be found in the `doc`
directory of the source distribution.  There is also an `online copy`_ of the
docs available.

.. _online copy: http://packages.python.org/nagiosplugin/

.. vim: set ft=rst:
