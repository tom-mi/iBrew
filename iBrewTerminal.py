# -*- coding: utf8 -*

import sys
import time
import datetime

from smarter.SmarterClient import *
from smarter.SmarterProtocol import *
from smarter.SmarterHelp import *

from domoticz.Domoticz import *

from iBrewWeb import *
from iBrewJokes import *

import traceback

#------------------------------------------------------
# iBrew
#
# Terminal Interface to iKettle 2.0 & SmarterCoffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Kettle Rattle (rev 6)
#------------------------------------------------------



#------------------------------------------------------
# iBrew VERSION INFORMATION
#------------------------------------------------------


iBrewApp          = "iBrew: iKettle 2.0 & SmarterCoffee Interface"
iBrewInfo         = "iBrew: Kettle Rattle © 2016 Tristan (@monkeycat.nl)"
iBrewContribute   = "Please contribute any discoveries on https://github.com/Tristan79/iBrew/issues"


class iBrewTerminal:

    #------------------------------------------------------
    # iBrew MONITOR
    #------------------------------------------------------
    # assume we're connected to a client! we're printing
    # every message received. you can stop the monitor by
    # pressing ctrl-c, the only messages we expect to
    # receive is a response message 14 (status device),
    # if there are any other messages we print them too!
    
    def monitor(self):
        print "iBrew: Press ctrl-c to stop"
        
        
        dump = self.client.dump
        self.client.dump_status = True
        self.client.dump = True
        
        while True:
            try:
                x = raw_input("")
            except:
                break
    
        self.client.dump = dump
        self.client.dump_status = False
        print



    #------------------------------------------------------
    # iBrew WEB
    #------------------------------------------------------

    # assume we're connected to a client
    # you can stop the sweep by pressing ctrl-c
    def web(self,port=Smarter.Port+1):
 
        webs = None
        try:
            if self.haveHost:
                webs = iBrewWeb()
                webs.run(port,self.client.dump,self.client.host)
            else:
                webs = iBrewWeb()
                webs.run(port,self.client.dump)
        except:
            print "iBrew: Failed to run Web Interface & REST API on port " + str(port)
            return
        print "iBrew: Starting Web Interface & REST API on port " + str(port) + ". Press ctrl-c to stop"
        self.monitor()
        print "iBrew: Stopped Web Interface & REST API on port " + str(port)
        webs.kill()


    #------------------------------------------------------
    # iBrew SWEEP
    #------------------------------------------------------

    # assume we're connected to a client
    # you can stop the sweep by pressing ctrl-c
    def sweep(self,start=1):
        if int(start) <= 0 or start > 256:
            print 'iBrew: sweep start out of range [00..ff]'
            return

        dump = self.client.dump
        self.client.dump = True
        self.client.dump_status = False
        
        print
        print "DO NOT DO THIS IF YOU DO NOT KNOW WHAT YOU ARE DOING"
        print
        print "IT CAN RENDER THE " + Smarter.device_to_string(self.client.deviceId) + " COMPLETELY USELESS"
        print
        print "Are you really, really sure?"
        try:
            i = raw_input("Please enter YES if you are: ")
            if i != "YES":
                return
        except:
            return
        print "iBrew: Press ctrl-c to stop"
 

        for id in range(int(start),256):
            try:
                # known command/message?
                known = Smarter.message_is_known(id)
                # know command for other device except itself?
                if not known:
                
                    # add zero here...
                    print "iBrew: Testing Command: " + Smarter.number_to_code(id)

                    # button pressed quit...
                    self.client.send_command(id)

                    # check if got also a ???status message... FIX
                    if self.client.commandStatus != Smarter.StatusInvalid:
                        print "iBrew: New Command Found: " + Smarter.number_to_code(id)
                    self.client.dump = False
                    self.client.device_stop()
                    self.client.dump = True
            except:
                break;
        self.client.dump = dump



    #------------------------------------------------------
    # iBrew Console MAIN LOOP
    #------------------------------------------------------

    def is_valid_ipv4_address(self,address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True


    def is_valid_ipv6_address(self,address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True


    def print_devices_found(self,devices):
        for i in range(0,len(devices)):
            print "iBrew: Found " + Smarter.device_info(devices[i][1],devices[i][2]) + " [" + devices[i][0] + "]"


    def execute(self,line):
        try:
            numarg = 0
            if len(line) == 0:
                if self.console:
                    if self.client.connected:
                        self.client.print_short_status()
                    else: print "iBrew: Not connected"
                    return
                else:
                    argument = line
                    command = "help"
            else:
                command = line[0].lower()
                numarg = len(line) - 1
                arguments = line[1:]

            if command == "exit" or command == "quit":
                self.client.run = False
                self.quit = True
                return

            if command == "dump":
                if numarg == 0 and not self.console:
                    print "iBrew: Do I look like a civet cat to you?"
                    return
                else:
                    if self.client.dump and numarg == 0:
                        self.client.dump = False
                        if self.console:
                            print "iBrew: Dump raw messages disabled"
                    else:
                        self.client.dump = True
                        if self.console:
                            print "iBrew: Dump raw messages enabled"
                    
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    else:
                        return

            if command == "shout":
                if self.console or numarg == 0:
                    print "iBrew: Can't hear you. Drinking tea at a dinner on the other side of the universe..."
                    return
                command = arguments[0].lower()
                arguments = arguments[1:]
                numarg -= 1
                if not self.console:
                    self.client.shout      = True
                    self.client.isKettle   = True
                    self.client.isCoffee   = True
                else:
                    print "iBrew: \'shout\' not available in the console"
                

            if command == "coffee":
                if self.console or numarg == 0:
                    print "iBrew: Can't hear you. Drinking tea at a dinner on the other side of the universe..."
                    return
                command = arguments[0].lower()
                arguments = arguments[1:]
                numarg -= 1
                if not self.console:
                    self.client.isCoffee   = True
                else:
                    print "iBrew: \'coffee\' not available in the console"


            if command == "kettle":
                if self.console or numarg == 0:
                    print "iBrew: Can't hear you. Drinking tea at a dinner on the other side of the universe..."
                    return
                command = arguments[0].lower()
                arguments = arguments[1:]
                numarg -= 1
                if not self.console:
                    self.client.isKettle   = True
                else:
                    print "iBrew: \'kettle\' not available in the console"



            if command == "fahrenheid":
                if numarg == 0 and not self.console:
                    print "iBrew: Kelvin..."
                    return
                else:
                    Smarter.fahrenheid = True
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    if self.console:
                        print "iBrew: Temperature in fahrenheid"
                        return


            if command == "celsius":
                    Smarter.fahrenheid = False
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    if self.console:
                        print "iBrew: Temperature in celsius"
                        return


            self.haveHost = False
            if numarg > 0:
                if self.is_valid_ipv4_address(arguments[numarg-1]) or self.is_valid_ipv6_address(arguments[numarg-1]):
                    self.client.host = arguments[numarg-1]
                    self.haveHost = True
                    numarg -= 1
                    arguments = arguments[0:numarg]
                    if self.client:
                        self.client.disconnect()


            if not self.client.connected and not self.haveHost and command != "help"  and command != "list" and command != "message" and command != "usage" and command != "commands" and command != "web" and command != "joke" and command != "protocol" and command != "structure" and command != "notes" and command != "examples" and command != "messages" and not (command == "domoticz" and numarg == 0):
            
            

                devices = self.client.find_devices()
                if self.client.dump:
                    self.print_devices_found(devices)
                if len(devices) >= 1:
                    self.client.host = devices[0][0]
                    self.haveHost = True
                    
                if command == "console" or command == "connect":
                    self.console = True
                    self.client.fast = False
                    self.client.shout = False

                try:
                    self.client.connect()
                    if self.console:
                        self.client.init_default()
                        self.client.print_connect_status()
                        self.client.print_status()
                except:
                    print "Wel that failed"


            if command == "connect" or command == "console" or command == "sweep" or command == "monitor" or (command == "domoticz" and numarg != 0):
                
                if not self.console or command == "connect":
                    self.app_info()
                    try:
                        if self.client.connected:
                            self.client.init_default()
                    except:
                        pass
                    self.joke()
                    self.client.print_connect_status()
                    self.client.print_status()
                    
                if (command == "console" or command == "connect") and command != "monitor":
                    self.client.dump_status = False
                    self.intro()
                    return
            

            if command == "web":
                self.app_info()
                self.joke()

            if command == "help" or command == "?":
                                            self.usage()
                                            self.commands()
            elif command == "usage":        self.usage()
            elif command == "commands":     self.commands()
            elif command == "protocol":     SmarterHelp.protocol()
            elif command == "structure":    SmarterHelp.structure()
            elif command == "notes":        SmarterHelp.notes()
            elif command == "examples":     self.examples()
            elif command == "messages":
                                            if numarg >= 1:
                                                if arguments[0].lower() == "all":   SmarterHelp.all()
                                                else:                       print "iBrew: Expected \'all\' got " + arguments[0]
                                            else:                           SmarterHelp.messages()
            elif command == "message":
                                            if numarg >= 1:
                                                SmarterHelp.message(Smarter.code_to_number(arguments[0]))
                                            else:
                                                print "iBrew: expected [00..FF]"
            elif command == "list":         self.print_devices_found(self.client.find_devices())
            elif command == "joke" or command == "quote":
                                            print
                                            self.joke()
                                            print
            elif command == "stats":
                                            print
                                            print "  " + str(self.client.connectCount).rjust(10, ' ') + "  Connected"
                                            print "  " + str(self.client.sendCount).rjust(10, ' ')   + "  Commands ("  + Smarter.bytes_to_human(self.client.sendBytesCount) + ")"
                                            print "  " + str(self.client.readCount).rjust(10, ' ')   + "  Responses (" + Smarter.bytes_to_human(self.client.readBytesCount) + ")"
                                            print
                                            
                                            for id in sorted(self.client.commandCount):
                                                print "  " + str(self.client.commandCount[id]).rjust(10, ' ') + "  [" + Smarter.number_to_code(id) + "] " + Smarter.message_description(id)
                                            print
                                            
                                            for id in sorted(self.client.responseCount):
                                                print "  " + str(self.client.responseCount[id]).rjust(10, ' ') + "  [" + Smarter.number_to_code(id) + "] "  + Smarter.message_description(id)
                                            print
            elif command == "web":
                                            if numarg == 0:
                                                self.web()
                                            else:
                                                self.web(int(arguments[0]))

            # Kettle
            elif not self.client.connected: return
            elif command == "heat":
                                            if numarg >= 1:
                                                self.client.kettle_heat()
                                            else:
                                                self.client.kettle_heat()
            elif command == "formula":
                                            if numarg >= 1:
                                                self.client.kettle_formula_heat()
                                            else:
                                                self.client.kettle_formula_heat()
            elif command == "default":      self.client.device_restore_default()
            elif command == "calibrate":
                                            if self.client.OnBase:
                                                print "Please remove kettle for accurate calibration"
                                            self.client.kettle_calibrate()
            elif command == "base":
                                            if numarg == 0:
                                                self.client.kettle_calibrate_base()
                                            if numarg >= 1:
                                                self.client.kettle_calibrate_store_base(Smarter.string_to_watersensor(arguments[0]))
                                                if not self.client.dump: self.client.print_watersensor_base()

            # WiFi
            elif command == "firmware":
                                            self.client.wifi_firmware()
                                            if not self.client.dump: self.client.print_wifi_firmware()
            elif command == "leave":        self.client.wifi_leave()
            elif command == "scan":
                                            self.client.wifi_scan()
                                            if not self.client.dump: self.client.print_wireless_networks()
            elif command == "join":
                                            if numarg >= 1:
                                                password = ""
                                                network = arguments[0]
                                                if numarg >= 2:
                                                    password = arguments[1]
                                                self.client.wifi_join(network,password)
                                            else:
                                                print "iBrew: no wireless network name"
            # Coffee
            elif command == "hotplate":
                                            if numarg >= 1:
                                                if arguments[0].lower() == "off":
                                                      self.client.coffee_hotplate_off()
                                                elif arguments[0].lower() == "on":
                                                    if numarg >= 2:
                                                            self.client.coffee_hotplate_on(Smarter.string_to_hotplate(arguments[1]))
                                                    else:
                                                        self.client.coffee_hotplate_on()
                                                else:
                                                    print "iBrew: hotplate missing [on/off] got " + arguments[0]
                                            else:
                                                print "iBrew: hotplate missing [on/off]"
            elif command == "carafe":       self.client.coffee_carafe()
            elif command == "singlecup":    self.client.coffee_single_cup_mode()
            elif command == "grinder":
                                            if self.client.useGrinder:
                                                print "iBrew: Grinder already used"
                                            else:
                                                self.client.coffee_grinder()
                                                print "iBrew: Grinder used"
            elif command == "filter":
                                            if not self.client.useGrinder:
                                                print "iBrew: Filter already used"
                                            else:
                                                self.client.coffee_filter()
                                                print "iBrew: Filter used"
            elif command == "brew":
                                            if numarg == 0:
                                                self.client.coffee_brew()
                                            elif numarg >= 1:
                                                print "Not yet implemented"
                                                # imclient.coffee_cups(arguments[1])
            elif command == "strength":
                                            if numarg == 0:
                                                print "iBrew: specify strength [weak,medium,strong]"
                                            elif numarg >= 1:
                                                self.client.coffee_strength(arguments[0])
            elif command == "weak":         self.client.coffee_strength("weak")
            elif command == "medium":       self.client.coffee_strength("medium")
            elif command == "strong":       self.client.coffee_strength("strong")
            elif command == "cups":
                                            if numarg == 0:
                                                print "iBrew: specify cups [1..12]"
                                            elif numarg >= 1:
                                                self.client.coffee_cups(Smarter.string_to_cups(arguments[0]))

              # Console Commands
            elif command == "domoticz":
                                            if numarg >= 2:
                                                self.domoticz_bridge(arguments[0],arguments[1])
                                            elif numarg == 1:
                                                print "iBrew: missing Domoticz sensor base name"
                                            else:
                                                self.domoticz()
            elif command == "monitor":      self.monitor()
            elif command == "sweep":
                                            if numarg >= 1:
                                                 self.sweep(Smarter.code_to_number(arguments[0]))
                                            else:
                                                self.sweep()
            elif command == "settings":     # FAST fix need device...
                                            if numarg == 0:
                                                self.client.device_settings()
                                                if not self.client.dump: self.client.print_settings()
                                            elif numarg == 0: print "iBrew: Could not store coffee settings, missing all arguments"
                                            elif numarg == 1 and self.client.isCoffee: print "iBrew: Could not store coffee settings, missing cups"
                                            elif numarg == 2 and self.client.isCoffee: print "iBrew: Could not store coffee settings, missing grinder"
                                            elif numarg == 3 and self.client.isCoffee: print "iBrew: Could not store coffee settings, missing hotplate"
                                            elif numarg == 1 and self.client.isKettle: print "iBrew: Could not store kettle settings, missing temperature"
                                            elif numarg == 2 and self.client.isKettle: print "iBrew: Could not store kettle settinss, missing formula mode"
                                            elif numarg == 3 and self.client.isKettle: print "iBrew: Could not store kettle settings, missing formula temperature"
                                            elif numarg >= 4:
                                                self.client.device_store_settings(arguments[0],arguments[1],arguments[2],arguments[3])
                                                if not self.client.dump: self.client.print_settings()
            elif command == "stop" or command == "off":
                                            if numarg == 0:
                                                self.client.device_stop()
                                            else:
                                                if arguments[0].lower() == "kettle":
                                                    self.client.kettle_stop()
                                                elif arguments[0].lower() == "coffee":
                                                    self.client.coffee_stop()
                                                else:
                                                    print "iBrew: Unknown device: "  + arguments[0]
                                                    self.client.device_stop()
                                        
            elif command == "on" or command == "start":
                                            if numarg == 0:
                                                self.client.device_start()
                                            else:
                                                if arguments[0].lower() == "kettle":
                                                    self.client.kettle_heat()
                                                elif arguments[0].lower() == "coffee":
                                                    self.client.coffee_brew()
                                                else:
                                                    print "iBrew: Unknown device: "  + arguments[0]
                                                    

            elif command == "reset":        self.client.device_reset()
            elif command == "info":
                                            self.client.device_info()
                                            if not self.client.dump: self.client.print_info()
            elif command == "history":
                                            self.client.device_history()
                                            if not self.client.dump: self.client.print_history()
            elif command == "time":
                                            print "not yet implemented"
                                            self.client.device_time()
            
            elif command == "status":       self.client.print_status()
            else:
                                            try:
                                                self.client.device_raw(command+''.join(arguments))
                                            except:
                                                print "iBrew: Sending raw command message failed"
        except Exception,e:
            if not self.console:
                self.quit = True
            print str(e)
            print(traceback.format_exc())
            print "iBrew: Command Failed"
            
        
    def __init__(self,arguments):
        self.console = False
        self.quit = True
        self.client = SmarterClient()
        self.client.fast = True
        try:
            self.execute(arguments)
        except:
            self.console = False
  
        if self.console:
            self.quit = False
        while not self.quit:
            try:
                # is should be threaded... since the kettle input is still comming as we wait for user input...
                cursor = self.client.host + ":" + self.client.device + "$"
                self.execute(raw_input(cursor).strip().split())
            except:
                break
        self.client.disconnect()
        
#------------------------------------------------------
# iBrew Console PRINT
#------------------------------------------------------
    def app_info(self):
        print iBrewApp
        print iBrewInfo
        print
        print iBrewContribute
        print

    def intro(self):
        print
        print "For list of commands type: help and press enter"
        print "Press enter for status update and press ctrl-c to quit"
        print

    def joke(self):
        joke = iBrewJokes().joke()
        if self.client is not None:
            if self.client.isCoffee:
                joke = iBrewJokes().coffee()
            elif self.client.isKettle:
                joke = iBrewJokes().tea()
        print "\n      \'" + joke[0] + "\'\n                  -- " + joke[1] + "\n"


    def usage(self):
        print
        print "  Usage: iBrew (dump) (shout|coffee|kettle) (fahrenheid) [command] (host)"
        print
        print "    fahrenheid             use fahrenheid"
        print "    dump                   dump message enabled"
        print "    host                   host address (format: ip4, ip6, fqdn)"
        print "    shout                  sends commands and quits not waiting for a reply"
        print "    command                action to take!"
        print
        print "  If you do not supply a host, it will try to connect to the first detected device"
        print "  Thus if you have more then one device supply a host (if its not in direct mode)"

    def commands(self):
        print
        print "  iKettle 2.0 & SmarterCoffee  Commands"
        print "    default                set default settings"
        print "    info                   device info"
        print "    history                action history"
        print "    list                   list detected devices"
        print "    reset                  reset device to default"
        print "    start                  start the device"
        print "    status                 show status"
        print "    settings               show user settings"
        print "    stop                   stop the appliance"
        print "    time [time]            set the device time"
        print
        print "  iKettle 2.0 Commands"
        print "    base                   show watersensor base value"
        print "    base [base]            store watersensor base value"
        print "    calibrate              calibrates watersensor"
        print "    celsius                use celsius ºC [console only]"
        print "    fahrenheid             use fahrenheid ºF [console only]"
        print "    formula ()()           heat kettle in formula mode"
        print "    heat ()()              heat kettle"
        print "    stop kettle            stops heating"
        print "    settings [keepwarm] [temperature] [formula] [formulatemperature] store kettle user settings"
        print
        print "  SmarterCoffee  Commands"
        print "    brew ()                brew coffee"
        print "    carafe                 returns if carafe is required"
        print "    cups [number]          set number of cups [1..12]"
        print "    grinder                use grinder"
        print "    filter                 use filter"
        print "    hotplate off           turn hotplate off"
        print "    hotplate on (minutes)  turn hotplate on (time in minutes)"
        print "    singlecup              return if singlecup mode is on"
        print "    (strength) [strength]  set strength coffee [weak, medium or strong]"
        print "    stop coffee            stops brewing"
        print "    settings [cups] [strength] [grinder] [hotplate]   store user settings"
        print
        print "  Wireless Network Commands"
        print "    join [net] [pass]      connect to wireless network"
        print "    leave                  disconnect (and open direct mode)"
        print "    scan                   scan wireless networks"
        print
        print "  Protocol Help Commands"
        print "    examples               show examples of commands"
        print "    messages               show all known protocol messages"
        print "    message [id]           show protocol message detail of message [id]"
        print "    notes                  show developer notes on the devices"
        print "    structure              show protocol structure information"
        print
        print "  Bridge Commands"
        print "    domoticz               show domoticz bridge help"
        print "    web (port)             start web interface & rest api on port [default 2082]"
        print
        print "  Debug Commands"
        print "    [hexdata]              send raw data to device (e.g. \'64 7e\')"
        print "    dump                   toggle \'dump raw messages\'"
        print "    console                start console [command line only]"
        print "    connect [host]         connect to device [console only]"
        print "    firmware               show firmware Wifi"
        print "    monitor                monitor incomming traffic"
        print "    protocol               show all protocol information available"
        print "    stats                  show traffic statistics"
        print "    sweep (id)             try (all or start with id) unknown command codes"
        print
        print "  Console Commands"
        print "    joke                   show joke"
        print "    quit                   quit console [console only]"
        print

    def domoticz(self):
        print """

  Domoticz Bridge
  _______________


  Bridge between iKettle 2.0 and domoticz. Its auto-creates 4 devices in domoticz, if not yet created,
  and monitors the kettle and update the domoticz devices accordingly.
  
    Water Temperature in ºC (temperature device)
    Water Height (custom device)
    Kettle on base (motion device)
    Kettle status (text device)
    
  Currently you have to create your heat, brew switches yourself (working on it), so:
  
    Place or link iBrew in your domoticz script folder or somewhere readable and reachable.
    Run iBrew in domoticz bridge mode to auto create the 'smarter' dummy hardware.
    Go to [SETUP] [HARDWARE] press 'create virtual sensors' on the dummy hardware called 'smarter'
    Give it a name (e.g. Kettle Heating) and select sensor type is switch.
    Go to [SWITCHES], scroll all the way down.
    Select 'edit' on your newly created device.
      Switch Icon, well heating is nice!
      On Action:  script://locationibrew/iBrew on kettleip
      Off Action: script://locationibrew/iBrew off kettleip
      
    You now have a functional heat/stop switch... 
    
    If you do not want a switch you can also create two push (on/off) buttons
    and fill in the action.
  
  If you use homebridge for domoticz (https://www.domoticz.com/forum/viewtopic.php?t=10272) you can use
  apple homekit with the kettle. You have to create extra virtual sensor (motion heat???) because the text sensor is not supported
  by homekit, all the other are.
  

  Usage:

    domoticz [domoticz] [basename] [kettle]

  Where:
  
    domoticz        Connection string to domoticz, [host:port] or [username:password@host:port]
    basename        Base name of your kettle devices in domoticz. The name may contain spaces.
    kettle          Connection string to iKettle 2.0, [host]
    host            Format: ip4, ip6, fqdn
    

  Notes:
  
    It will auto-create the devices in Domoticz
    Tested on Domoticz v3.52
    *** Currently iKettle 2.0 Only ***
  
  Examples:
  
    iBrew domoticz sofia:$ecrit@localhost:8080 Kettle Kitchen 192.168.4.1
    iBrew domoticz 10.0.0.1:9001 Kettle Office 192.168.10.13
    iBrew dump domoticz 10.0.0.1:9001 Kettle Office 192.168.10.13
    iBrew domoticz localhost:8080 Kettle 
  
              """

    def examples(self):
        print
        print "  Example:"
        print "    off            Stop heating/brewing"
        print "    messages       Show all protocol messages"
        print "    message 3e     Show protocol message 3a, turn hotplate on"
        print "    167E           Send kettle raw stop"
        print "    21 30 05 7e    Send kettle raw heat"
        print "    strength weak  Set coffee strength to weak"
        print "    cups 3         Set number of cups to brew"
        print

