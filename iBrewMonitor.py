# -*- coding: utf8 -*

from iBrewClient import *

#------------------------------------------------------
# iBrew MONITOR
#
# Monitors iKettle 2.0 or Smarter Coffee Devices
#------------------------------------------------------

class iBrewMonitor:

    def __init__(self,host):
        iBrewPrintHeader()
        client = iBrewClient(host)
        client.print_connect_status()
        print "iBrew: Press ctrl-c to quit"
        lastreply = ""
        while True:
            try:
                reply = client.read()
                if lastreply == reply:
                    pass
                else:
                    lastreply = reply
                    client.print_short_status()
            except:
                print
                break;