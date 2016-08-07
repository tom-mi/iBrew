# -*- coding: utf8 -*

import sys
from iBrewProtocol import *
from iBrewClient import *
from iBrewCommandLine import *
from iBrewMonitor import *
from iBrewConsole import *

#------------------------------------------------------
# iBrew COMMAND LINE
#
# Command line access for iKettle 2.0 or Smarter Coffee
# Device
#------------------------------------------------------

class iBrewCommandLine:

    def help(self):
        print "iBrew ☕ Smarter Coffee & ♨ iKettle 2.0 Control"
        print iBrewVersion
        print
        print 'Usage:'
        print '  iBrew.py [option] (host)'
        print
        print '[options]'
        print '  console'
        print '  cups [number]'
        print '  calibrate'
        print '  calibrate base'
        print '  emulate [kettle, coffee]'
        print '  grinder'
        print '  hotplate off'
        print '  hotplate on'
        print '  monitor'
        print '  off'
        print '  on'
        print '  protocol'
        print '  raw [data]'
        print '  relay'
        print '  status'
        print '  strength [weak, medium or strong]'
        print

    def __init__(self,host):
        # Lower Case Arguments
        arguments = len(sys.argv) - 1
        if arguments >= 1:
            arg1 = sys.argv[1].lower()
        if arguments >= 2:
            arg2 = sys.argv[2].lower()
        if arguments >= 3:
            arg3 = sys.argv[3].lower()

        # No arguments display help
        if arguments == 0:
            self.help()
            sys.exit()

        # FIX THIS SHIT Set the device host if in arguments
        if arguments == 3:
            host = arg3
        elif arguments == 2:
            host = arg2

        # Preform action!
        if arguments >= 1:
            if arg1 == "on":
                iBrewClient(host).on()
            elif arg1 == "calibrate":
                if arguments >= 2 and arg2 == "base":
                    iBrewClient(host).calibrate_base()
                else:
                    iBrewClient(host).calibrate()
                    # FiX Print
            elif arg1 == "off":
                iBrewClient(host).off()
            elif arg1 == "status":
                iBrewClient(host).print_status()
            elif arg1 == "grinder":
                iBrewClient(host).grinder()
            elif arg1 == "protocol":
                iBrewProtocol().all()
            elif arg1 == "monitor":
                iBrewMonitor(host)
            elif arg1 == "console":
                iBrewConsole(host)
            elif arg1 == "relay":
                iBrewRelay()
            elif arg1 == "domoticz":
                iBrewDomoticzBridge(host)
            elif arguments >= 2 and not arg1 == "calibrate":
                if arg1 == "raw":
                    iBrewClient(host).raw(arg2)
                elif arg1 == "hotplate" and arg2 == "on":
                    iBrewClient(host).hotplate_on()
                elif arg1 == "hotplate" and arg2 == "off":
                    iBrewClient(host).hotplate_off()
                elif arg1 == "strength":
                    iBrewClient(host).coffee_strength(arg2)
                elif arg1 == "cups":
                    # FIX WRONG IP{UT
                    iBrewClient(host).number_of_cups(arg2)
                elif arg1 == "emulate" and arg2 == "kettle":
                    iBrewServer() #.emulate("kettle")
                elif arg1 == "emulate" and arg2== "coffee":
                    iBrewServer() #.emulate("coffee")
                else:
                    self.help()
                    print 'iBrew: Invalid option: ',arg1
                    print
            else:
                self.help()
                print 'iBrew: Invalid option: ',arg1
                print