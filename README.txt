The nagiosplugin library
========================

About
-----

**nagiosplugin** is a Python class library which helps writing Nagios (or Icinga)
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
- No dependencies beyond the Python standard library (except for Python 2.6).

nagiosplugin runs on POSIX and Windows systems. It is compatible with Python
3.4, Python 3.3, Python 3.2, and Python 2.7.

Feedback and Suggestions
------------------------

nagiosplugin is currently maintained by Matt Pounsett <matt@conundrum.com>.  A
public issue tracker can be found at
<https://github.com/mpounsett/nagiosplugin/issues> for bugs, suggestions, and
patches.

License
-------

The nagiosplugin package is released under the Zope Public License 2.1 (ZPL), a
BSD-style Open Source license.


Documentation
-------------

Comprehensive documentation is `available online`_. The examples mentioned in
the `tutorials`_ can also be found in the `nagiosplugin/examples` directory of
the source distribution.

.. _available online: http://pythonhosted.org/nagiosplugin/
.. _tutorials: http://pythonhosted.org/nagiosplugin/tutorial/

Acknowledgements
----------------

nagiosplugin was originally written and maintained by Christian Kauhaus
<kc@flyingcircus.io>.  Additional contributions from the community are
acknowledged in the file CONTRIBUTORS.txt

.. vim: set ft=rst:
