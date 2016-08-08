# -*- coding: utf8 -*

from iBrewClient import *
from iBrewVersion import *

#------------------------------------------------------
# iBrew MONITOR
#
# Monitors iKettle 2.0 or Smarter Coffee Devices
#------------------------------------------------------

class iBrewMonitor:

    def __init__(self,host):
        iBrewPrintAppVersion()
        client = iBrewClient(host)
        client.print_connect_status()
        print "iBrew: Press ctrl-c to quit"
        lastResponse = ""
        while True:
            try:
                response = client.read()
                if lastResponse == response:
                    pass
                else:
                    lastResponse = response
                    client.print_short_status()
            except:
                print
                break;