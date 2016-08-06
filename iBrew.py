#!/usr/bin/python
# -*- coding: utf8 -*

from iBrewUserSettings import *
from iBrewCommandLine import *
from iBrewMonitor import *
from iBrewConsole import *
#from iBrewServer import *

#------------------------------------------------------
# MAIN
#
# Start any program you like, default is command line
# Which has all other options available.
#------------------------------------------------------

# Uncomment the one which you want
iBrewCommandLine(host)
#iBrewServer("")
#iBrewMonitor(host)
#iBrewConsole(host)