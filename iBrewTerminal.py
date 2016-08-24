# -*- coding: utf8 -*

import sys
import random
import time
import datetime

from smarter.SmarterClient import *
from smarter.SmarterProtocol import *
from smarter.SmarterHelp import *

from domoticz.Domoticz import *

from iBrewREST import *

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
        self.client.dump = True
        # repeat until...
        previousResponse = ""
        while True:
            # ...we catch ctrl-c, lets try...
            try:
                # ...read response message (every second or so)...
                response = self.client.read()
                
                # ...if the response is the same as before then skip...
                
                # this is possible due to that response message 14/32 (status device)
                # is the only one repeated after eachothers
                # and we are not interested in anything but changes!
                
                if previousResponse != response:
                    previousResponse = response
                    # ...else got one! yeah! print it!
            except:
                break
        self.client.dump = dump
                


    #------------------------------------------------------
    # iBrew DOMOTICZ
    #------------------------------------------------------
    # See monitor


    def domoticz_bridge(self, server, name, sleep = 0, secure=False):
        if self.client.isKettle:
            domoticz_bridge_kettle(server,name,sleep,secure)
        elif self.client.isCoffee:
            domoticz_bridge_coffee(server,name,sleep,secure)
            

    def domoticz_bridge_kettle(self, server, name, sleep = 0, secure=False):
        
        if not self.client.isKettle:
            print "iBrew: SmarterCoffee not supported"
            return
        
        domoticz = Domoticz(server,secure)
        
        if domoticz.use_virtual_hardware("Smarter"):

            temp_name    = name + " Water Temperature"
            temp_type    = domoticz.SensorTemperature
            offbase_name = name + " Base"
            offbase_type = domoticz.SensorSwitch
            water_name   = name + " Water Height"
            water_type   = domoticz.SensorCustom
            
            #default_temp_name = name + " Default Temperature"
            #default_temp_type = domoticz.SensorSwitch
            #default_temp_form_name = name + " Default Formula Temperature"
            #default_temp_form_type = domoticz.SensorSwitch
            

            status_name = name + " Status"
            status_type = domoticz.SensorSwitch
            
            water_idx   = domoticz.use_virtual_custom_water(water_name,"")
            temp_idx    = domoticz.use_virtual_temperature(temp_name)
            offbase_idx = domoticz.use_virtual_motion(offbase_name)
            status_idx  = domoticz.use_virtual_text(status_name)
            
            #default_temp_idx = domoticz.use_virtual_heat_dimmer(default_temp_name)
            #default_temp_form_idx = domoticz.use_virtual_heat_dimmer(default_temp_form_name)
            
            #if default_temp_form_idx == "None" or default_temp_idx == "None" or
            if status_idx == "None" or offbase_idx == "None" or temp_idx == "None" or water_idx == "None":
                print "iBrew: Failed to get Sensor IDX"
                return
            
            print "iBrew: Using " + domoticz.print_type(temp_type) + " sensor ["+ temp_name + "] IDX " + str(temp_idx)
            print "iBrew: Using " + domoticz.print_type(water_type) + " sensor ["+ water_name + "] IDX " + str(water_idx)
            print "iBrew: Using " + domoticz.print_type(offbase_type) + " sensor ["+ offbase_name + "] IDX " + str(offbase_idx)
            print "iBrew: Using " + domoticz.print_type(status_type) + " sensor ["+ status_name + "] IDX " + str(status_idx)
            #print "iBrew: Using " + domoticz.print_type(default_temp_type) + " sensor ["+ default_temp_name + "] IDX " + str(default_temp_idx)
            #print "iBrew: Using " + domoticz.print_type(default_temp_form_type) + " sensor ["+ default_temp_form_name + "] IDX " + str(default_temp_form_idx)
        else:
            print "iBrew: Could not find hardware"
            return


        print "iBrew: iKettle 2.0 Domoticz Bridge. Press ctrl-c to stop"

        previousResponse = ""
        previousWaterSensor = 0
        previousStatus = "Unknown"
        
        prevPreviousTemperature = self.client.temperature
        previousTemperature = self.client.temperature
        previousAverage = self.client.temperature
        
        previousBase = False
        previousBaseFirst = True

        then = time.time()

        update = 30
        
        while True:
            try:
                now = time.time()
                stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print stamp + " ♨"

                response = self.client.read()
                #self.client.print_short_status()
               
                average = int(round(float((float(previousTemperature) + float(prevPreviousTemperature) + float(self.client.temperature))/3),0))

                if int(now-then) > update:
                    if domoticz.set_temperature(temp_idx,average,False):
                        print stamp + " Water temperature: " + Smarter.temperature_to_string(average)
                    if domoticz.set_custom(water_idx,self.client.waterSensor,False):
                        print stamp + " Water height: " + str(self.client.waterSensor)
       
                if previousAverage != average:
                    if domoticz.set_temperature(temp_idx,average):
                        print stamp + " Water temperature: " + Smarter.temperature_to_string(average)
                    previousAverage = average

                prevPreviousTemperature = previousTemperature
                previousTemperature = self.client.temperature

                if previousResponse == response:
                    if int(now-then) > update: then = now
                    continue

                previousResponse = response

                if previousStatus != self.client.kettleStatus:
                    status = Smarter.status_kettle_description(self.client.kettleStatus)
                    if domoticz.set_text(status_idx,status):
                        print stamp + " iKettle 2.0 is " + status.lower()
                    previousStatus = self.client.kettleStatus
            
                if previousWaterSensor - 3 > self.client.waterSensor or previousWaterSensor + 3 < self.client.waterSensor or int(now-then) > update:
                    if domoticz.set_custom(water_idx,self.client.waterSensor):
                        print stamp + " Water height: " + str(self.client.waterSensor)
                    previousWaterSensor = self.client.waterSensor
                
                if previousBaseFirst or (previousBase != self.client.onBase):
                    if domoticz.set_motion(offbase_idx,self.client.onBase):
                        if self.client.onBase:
                            s = "on"
                        else:
                            s = "off"
                        print stamp + " iKettle 2.0 is " + s + " base"
                    previousBase = self.client.onBase
                    previousBaseFirst = False

                if int(now-then) > update: then = now

            except:
                break
        
 
 
 
    def domoticz_bridge_coffee(self, server, name, sleep = 0, secure=False):
        
        if not self.client.isCoffee:
            print "iBrew: iKettle 2.0 not supported"
            return
        
        domoticz = Domoticz(server,secure)
        
        if domoticz.use_virtual_hardware("Smarter"):

            water_name   = name + " Water Level"
            water_type   = domoticz.SensorCustom
            status_name = name + " Status"
            status_type = domoticz.SensorSwitch
            
            water_idx   = domoticz.use_virtual_custom_water(water_name,"")
            status_idx  = domoticz.use_virtual_text(status_name)

            if status_idx == "None" or water_idx == "None":
                print "iBrew: Failed to get Sensor IDX"
                return
            
            print "iBrew: Using " + domoticz.print_type(water_type) + " sensor ["+ water_name + "] IDX " + str(water_idx)
            print "iBrew: Using " + domoticz.print_type(status_type) + " sensor ["+ status_name + "] IDX " + str(status_idx)
        else:
            print "iBrew: Could not find hardware"
            return


        print "iBrew: SmarterCoffee Domoticz Bridge. Press ctrl-c to stop"

        previousResponse = ""
        previousWaterSensor = 0
        previousStatus = "Unknown"

        then = time.time()
        update = 30
        
        while True:
            try:
                now = time.time()
                stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print stamp + " ♨"

                response = self.client.read()
                #self.client.print_short_status()
               
                average = int(round(float((float(previousTemperature) + float(prevPreviousTemperature) + float(self.client.temperature))/3),0))

                if int(now-then) > update:
                    if domoticz.set_temperature(temp_idx,average,False):
                        print stamp + " Water temperature: " + Smarter.temperature_to_string(average)
                    if domoticz.set_custom(water_idx,self.client.waterSensor,False):
                        print stamp + " Water height: " + str(self.client.waterSensor)
       
                if previousAverage != average:
                    if domoticz.set_temperature(temp_idx,average):
                        print stamp + " Water temperature: " + Smarter.temperature_to_string(average)
                    previousAverage = average

                prevPreviousTemperature = previousTemperature
                previousTemperature = self.client.temperature

                if previousResponse == response:
                    if int(now-then) > update: then = now
                    continue

                previousResponse = response

                if previousStatus != self.client.kettleStatus:
                    status = Smarter.status_kettle_description(self.client.kettleStatus)
                    if domoticz.set_text(status_idx,status):
                        print stamp + " SmarterCoffee  is " + status.lower()
                    previousStatus = self.client.kettleStatus
            
                if previousWaterSensor != self.client.waterSensor:
                    if domoticz.set_custom(water_idx,self.client.waterSensor):
                        print stamp + " Water level: " + str(self.client.waterSensor)
                    previousWaterSensor = self.client.waterSensor

                if int(now-then) > update: then = now

            except:
                break

    #------------------------------------------------------
    # iBrew SWEEP
    #------------------------------------------------------

    # assume we're connected to a client
    # you can stop the sweep by pressing ctrl-c
    def sweep(self,start=1):
        if int(start) <= 0 or start > 256:
            print 'iBrew: sweep start out of range [00..ff]'
            return
        print "iBrew: Press ctrl-c to stop"
 
        dump = self.client.dump
        self.client.dump = True

        for id in range(int(start),256):
            try:
                # known command/message?
                known = Smarter.message_is_known(id)
                # know command for other device except itself?
                if not known:
                
                    # add zero here...
                    print "iBrew: Testing Command: " + Smarter.number_to_code(id)

                    # button pressed quit...
                    self.client.send(Smarter.number_to_raw(id))

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
    # iBrew REST
    #------------------------------------------------------

    # assume we're connected to a client
    # you can stop the sweep by pressing ctrl-c
    def rest(self,port=Smarter.Port+1):
        dump = self.client.dump
        self.client.dump = False
        print "iBrew: Starting REST API on port " + str(port) + ". Press ctrl-c to stop"
        iBrewREST(port)
        print "iBrew: Stopped REST API on port " + str(port)
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
    #    try:
            numarg = 0
            if len(line) == 0:
                if self.console:
                    if not dump:
                        client.print_short_status()
                    return
                else:
                    argument = line
                    command = "help"
            else:
                command = line[0].lower()
                numarg = len(line) - 1
                arguments = line[1:]
            
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
                    self.client.fast       = True
                    self.client.shout      = True
                    self.client.isKettle   = True
                    self.client.isCoffee   = True
                else:
                    print "iBrew: \'shout\' not available in the console"
                

            if command == "fahrenheid":
                if numarg == 0 and not self.console:
                    print "iBrew: Kelvin..."
                    return
                else:
                    Smarter.fahrenheid = True
                    if self.console:
                        print "iBrew: Temperature in fahrenheid"
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    else:
                        return
            
            if command == "celcius":
                    Smarter.fahrenheid = False
                    if self.console:
                        print "iBrew: Temperature in celcius"
                    if numarg > 0:
                        command = arguments[0].lower()
                        arguments = arguments[1:]
                        numarg -= 1
                    else:
                        return

            haveHost = False
            if numarg > 0:
                if self.is_valid_ipv4_address(arguments[numarg-1]) or self.is_valid_ipv6_address(arguments[numarg-1]):
                    self.client.host = arguments[numarg-1]
                    haveHost = True
                    numarg -= 1
                    arguments = arguments[0:numarg]



            if not self.client.connected and not haveHost and command != "help" and command != "help" and command != "message" and command != "usage" and command != "commands" and command != "joke" and command != "protocol" and command != "structure" and command != "notes" and command != "examples" and command != "messages" and not (command == "domoticz" and numarg == 0):

                devices = self.client.find_devices()
                if self.client.dump:
                    self.print_devices_found(devices)
                if len(devices) == 1:
                    self.client.host = devices[0][0]
                    haveHost = True


            if command == "connect" or command == "console" or command == "sweep" or command == "monitor" or (command == "domoticz" and numarg != 0):
                self.app_info()
                self.client.init_default()
                self.joke()
                self.client.print_connect_status()
                self.client.print_status()
                if command == "console" or command == "connect":
                    self.console = True
                    self.intro()
                return

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
                                                SmarterHelp.message(Smarter.code_to_number(argument[0]))
                                            else:
                                                print "iBrew: expected [00..FF] got " + argument[0]

            # Kettle
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
            elif command == "calibrate":    self.client.calibrate()
            elif command == "base":
                                            if numarg == 0:
                                                self.client.calibrate_base()
                                            if numarg >= 1:
                                                self.client.calibrate_store_base(Smarter.string_to_watersensor(arguments[0]))
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
            elif command == "grinder":      self.client.coffee_grinder()
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
            elif command == "cups":
                                            if numarg == 0:
                                                print "iBrew: specify cups [1..12]"
                                            elif numarg >= 1:
                                                self.client.coffee_cups(int(arguments[0]))

              # Console Commands


            elif command == "exit" or command == "quit":
                                            self.quit = True
            elif command == "domoticz":
                                            if numarg >= 2:
                                                self.domoticz_bridge(arguments[0],arguments[1])
                                            elif numarg == 1:
                                                print "iBrew: missing Domoticz sensor base name"
                                            else:
                                                self.domoticz()
            elif command == "list":         self.print_devices_found(self.client.find_devices())
            elif command == "monitor":      self.monitor()
            elif command == "sweep":
                                            if numarg > 1:
                                                 self.sweep(id)
                                            else:
                                                self.sweep()
            elif command == "joke" or command == "quote":
                                            print
                                            self.joke()
                                            print
            elif command == "rest":
                                            if numarg == 0:
                                                self.rest()
                                            else:
                                                self.rest(int(arguments[0]))
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
            else:                           self.client.device_raw(command+''.join(arguments))
    #   except:
     #       print "iBrew: Command Failed"
        
    def __init__(self,arguments):
        self.console = False
        self.quit = True
        self.client = SmarterClient()
        self.client.fast = True
        self.execute(arguments)
        if self.console:
            self.quit = False
            cursor = self.client.host + ":" + self.client.device + "$"
        while not self.quit:
            try:
                # is should be threaded... since the kettle input is still comming as we wait for user input...
                self.execute(raw_input(cursor).strip().split())
            except:
                break
        
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
        print "    stop                   stop the appliance if its brewing or boiling"
        print "    time [time]            set the device time"
        print
        print "  iKettle 2.0 Commands"
        print "    base                   show watersensor base value"
        print "    base [base]            store watersensor base value"
        print "    calibrate              calibrates watersensor"
        print "    celcius                use celcius ºC [console only]"
        print "    fahrenheid             use fahrenheid ºF [console only]"
        print "    formula ()()           heat kettle in formula mode"
        print "    heat ()()              heat kettle"
        print "    stop kettle            stops boiling"
        print "    settings [keepwarm] [temperature] [formula] [formulatemperature] store kettle user settings"
        print
        print "  SmarterCoffee  Commands"
        print "    brew ()                brew coffee"
        print "    carafe                 returns if carafe is required"
        print "    cups [number]          set number of cups [1..12]"
        print "    grinder                toggle grinder"
        print "    hotplate off           turn hotplate off"
        print "    hotplate on (minutes)  turn hotplate on (time in minutes)"
        print "    singlecup              return if singlecup mode is on"
        print "    strength [strength]    set strength coffee [weak, medium or strong]"
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
        print "    rest (port)            start rest api on port default 2082"
        print
        print "  Debug Commands"
        print "    [hexdata]              send raw data to device (e.g. \'64 7e\')"
        print "    dump                   toggle \'dump raw messages\'"
        print "    console                start console [command line only]"
        print "    connect [host]         connect to device [console only]"
        print "    firmware               show firmware Wifi"
        print "    monitor                monitor incomming traffic"
        print "    protocol               show all protocol information available"
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
    
  Currently you have to create your boil, brew switches yourself (working on it), so:
  
    Place or link iBrew in your domoticz script folder or somewhere readable and reachable.
    Run iBrew in domoticz bridge mode to auto create the 'smarter' dummy hardware.
    Go to [SETUP] [HARDWARE] press 'create virtual sensors' on the dummy hardware called 'smarter'
    Give it a name (e.g. Kettle Boil) and select sensor type is switch.
    Go to [SWITCHES], scroll all the way down.
    Select 'edit' on your newly created device.
      Switch Icon, well heating is nice!
      On Action:  script://locationibrew/iBrew on kettleip
      Off Action: script://locationibrew/iBrew off kettleip
      
    You now have a functional boil/stop switch... 
    
    If you do not want a switch you can also create two push (on/off) buttons
    and fill in the action.
  
  If you use homebridge for domoticz (https://www.domoticz.com/forum/viewtopic.php?t=10272) you can use
  apple homekit with the kettle. You have to create extra virtual sensor (motion boil???) because the text sensor is not supported
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
        print "    off            Stop boiling/brewing"
        print "    messages       Show all protocol messages"
        print "    message 3e     Show protocol message 3a, turn hotplate on"
        print "    167E           Send kettle raw stop"
        print "    21 30 05 7e    Send kettle raw boil"
        print "    strength weak  Set coffee strength to weak"
        print "    cups 3         Set number of cups to brew"
        print

    teaJokes = [["What do you call a talkative drink?","Chai-tea."],
                ["How long does it take to brew chinese tea?","Oolong time."],
                ["When shouldn't you drink a hot beverage?","If it's not your cup of tea."],
                ["How does Moses make his tea?","Hebrews it."],
                ["What drink do goalies hate?","Penal-tea."],
                ["How do you ask a dinosaur to lunch?","Tea Rex?"],
                ["What does a worry wart drink?","Safe-tea."],
                ["Why did the hipster burn his tongue?","Because he drank his tea before it was cool."],
                ["What drink brings you down to earth?","Gravi-tea."],
                ["What do sophisticated fish drink?","Salt-tea."],
                ["Why did the tea bag have to do it's laundry?","Because it was stained."],
                ["What kind of music do teapots like?","Jasmine."],
                ["Why must you be careful of tea at night?","Because it might mug you."],
                ["What does a tea bag do when it's tired?","It seeps."],
                ["Why did the teapot get in trouble?","Because he was naugh-tea."],
                ["What did the teapot wear to bed?","A nightea"],
                ["What happens when an old teapot laughs too hard?","It teas its pants."],
                ["It is time to get this par tea started!","Right?"],
                ["Hello Brew-TEA-Full!!!","Your kettle"],
                ["I love to drink tea each day","It brings out my inner tranquili-tea"],
                ["Today!","Full of creativi-Tea"],
                ["It tends to break the ice very easily","Flirt-tea."],
                ["When your kettle is too","Chat-tea"],
                ["Where there is tea","There is hope!"],
                ["If tea is the drink of love","Then brew on!"],
                ["It really is a serious problem","If tea can’t fix it."],
                ["The study into soaked leafs","Teaology"],
                ["Why I have an iKettle two zero?","So my wife only has to walk, once!"]
                ]
    
    coffeeJokes =  [["Why is a bad cup of coffee the end of a marriage?","Because it's grounds for divorce!"],
                ["What do you call sad coffee?","Despresso"],
                ["Did you know it's a sin for a woman to make coffee?","In the bible it says He-brews"],
                ["Why Coffee is better than a Woman?","Coffee goes down easier!"],
                ["They call me \'coffee\' ","Cause I grind so fine."],
                ["Hold the sugar please","You're sweet enough for the both of us"],
                ["So I've been thinking about you a latte","Your coffee grinder"],
                ["How do you look so good before coffee?","Your coffee machine"],
                ["Why are men are like coffee?"," The best ones are rich, hot, and can keep you up all night!"],
                ["Coffee runs to you!","Coffee runs to me!"],
                ["Come to the Darkside™","We have coffee"],
                ["","Pot-head!!!"],
                ["Coffee!","Makes me poop!"],
                ["How does a tech-guy drink Coffee?","He installs Java!"],
                ["Why do they call coffee mud?","Because it was ground a couple of minutes ago"],
                ["What's fat, slimy, and drinks a lot of coffee?","Java the Hut"],
                ["Why don't snakes drink coffee?","It makes them viperactive!"],
                ["What are you, if you call your cats cream and sugar?","You're probably drinking too much coffee"],
                ["What's black and doesn't work?","Decaffeinated coffee"],
                ["Where is all the coffee?","We were mugged!"],
                ["Energy is...","MilkCoffee²"],
                ["I'm sure all coffee beans are juvenile","They're always getting grounded!"],
                ["Is coffee your daily grind?","Your coffee machine"]
                
        ]


    def joke(self):
        joke = random.choice(self.teaJokes+self.coffeeJokes)
        if self.client is not None:
            if self.client.isCoffee:
                joke = random.choice(self.coffeeJokes)
            elif self.client.isKettle:
                joke = random.choice(self.teaJokes)
        print "\n      \'" + joke[0] + "\'\n                  -- " + joke[1] + "\n"

