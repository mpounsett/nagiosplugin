nagiosplugin
============

Features
--------

`nagiosplugin` is a package which helps writing Nagios/Icinga compatible
plugins easily in Python. It cares for much of the boilerplate code and default
logic commonly found in Nagios checks, including:

* Nagios 3 Plugin API compliant parameters and output formatting
* Controller to handle the general plugin control flow
* Full Nagios range syntax support
* Automatic threshold checking
* Multiple independend measures and overall state logic
* Long output and performance data
* Timeout handling
* Default options
* Persistent "cookies" to retain state information between check runs.


Documentation
-------------

To get started writing Nagios plugins, see the examples in the `examples`
subdirectory.

More documentation on using this package can be found in the `doc` directory.


Authors
-------

`nagiosplugin` is primarily written and maintained by Christian Kauhaus
<kc@gocept.com>. Feel free to contact the author for bug fixes, suggestions and
patches.

A public issue tracker can be found at
http://projects.gocept.com/projects/projects/nagiosplugin/issues.


License
-------

The `nagiosplugin` package is released the Zope Public License (ZPL), a BSD-style Open Source license.

.. vim: set ft=rst sw=3 sts=3 et:
