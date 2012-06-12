# Copyright (c) 2012 gocept gmbh & co. kg
# See also LICENSE.txt

"""Class library for writing Nagios (Icinga) plugins"""

# abbreviate commonly used classes
from check import Check
from controller import Controller
from measure import Measure
from range import Range
from state import State
from cookie import Cookie, store
