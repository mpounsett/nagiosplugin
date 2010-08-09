nagiosplugin
============

:py:mod:`nagiosplugin` is a package which helps writing Nagios/Icinga compatible
plugins easily in Python. It cares for much of the boilerplate code commonly
found in Nagios check, including:

* Nagios 3 Plugin API compliant parameters and output formatting
* Controller to handle the general plugin control flow
* Full Nagios range syntax support
* Automatic threshold checking
* Multiple independend measures and overall state logic
* Long output and performance data
* Option parsing
* Timeout handling
* Persistent "cookies" to retain state information between check runs.

To get started writing Nagios plugins, see the examples in the :doc:`examples`
subdirectory.

The :py:mod:`nagiosplugin` package is released under a BSD-style Open Source
license (ZPL).

# vim: set ft=rst sts=3:
