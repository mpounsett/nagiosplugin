.. Copyright (c) 2011 gocept gmbh & co. kg
.. _class_anatomy:

Class Anatomy
=============

.. index:: plugin

Plugins written with :py:mod:`nagiosplugin` are subclasses from the
:py:class:`Check` base class, overriding methods to provide
functionality. The methods are called from the :py:class:`Controller` class,
which implements the general plugin control logic.

For instructional purposes, we start writing a very basic plugin that checks the
free space on the root partition. It should return "warning" if the partition is
more than 50% full and "critical" if it is more than 75% full.

To get started, we start with an empty :py:class:`Check` subclass::

   import nagiosplugin
   import os

   class DiskCheck(nagiosplugin.Check):
      name = 'disk tutorial'
      version = '0.1'

   main = nagiosplugin.Controller(DiskCheck)
   if __name__ == '__main__':
      main()

The new plugins functionality will be defined in the class
:py:class:`DiskCheck`. This class is passed to the :py:class:`Controller`'s
constructor which returns the main function. :py:obj:`main` could be used as a
console script entry point or used directly if the script is called from the
command line. The :py:attr:`name` and :py:attr:`version` attributes
define basic check properties used for output.


