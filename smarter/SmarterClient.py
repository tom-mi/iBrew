# -*- coding: utf8 -*-

import socket
import os
import sys
import string
import random
import time

import threading

from SmarterProtocol import *

#------------------------------------------------------
# SMARTER CLIENT INTERFACE
#
# Python interface to iKettle 2.0 & SmarterCoffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Kettle Rattle (rev 6)
#------------------------------------------------------


#------------------------------------------------------
# CLIENT INTERFACE CLASS
#------------------------------------------------------

class SmarterClient:
    
    def init(self):
        # network
        self.port                       = Smarter.Port
        
        # device
        self.commandStatus              = Smarter.StatusSucces
        self.sendMessage                = None
        self.responseMessage            = None
        self.readMessage                = None
        self.statusMessage              = None
        
        # device info
        self.device                     = "None"
        self.deviceId                   = 0
        self.version                    = 0
    
        # kettle
        self.isKettle                   = False
        self.kettleStatus               = Smarter.KettleReady
        self.temperature                = 0
        self.onBase                     = False
        self.defaultTemperature         = 100
        self.defaultKeepWarmTime        = 0
        self.defaultFormula             = False
        self.defaultFormulaTemperature  = 50
        # watersensor
        self.waterSensorBase            = 0
        self.waterSensor                = 0
        self.waterSensorStable          = 0
        self.temperatureStable          = 0
        
        # coffee
        self.isCoffee                   = False
        self.coffeeStatus               = 0 # unknown
        self.cups                       = 1
        self.strength                   = Smarter.CoffeeMedium
        self.carafe                     = False
        self.singlecup                  = False
        self.defaultCups                = 1
        self.defaultStrength            = 1
        self.defaultGrinder             = False
        self.defaultHotPlate            = 0
        self.waterLevel                 = 0
        
 
        # Wifi
        self.Wifi                       = []
        self.WifiFirmware               = "None"


    def __init__(self):
        self.host                       = Smarter.DirectHost
        self.dump_status                = True
        self.dump                       = False
                #set this to try is you want to connect send receive and don't care about the new status or other messages the about the out come, its disconnect afterwards....
        self.fast                       = False
        #set this to try is you want to connect send and really do not care about the about the out come, its disconnect afterwards....
        self.shout                      = False
        
        
        self.sendCount                  = 0
        self.readCount                  = 0
        self.sendBytesCount             = 0
        self.readBytesCount             = 0
        self.connectCount               = 0
        self.commandCount               = dict()
        self.responseCount              = dict()
        
        # Threading info
        self.sending                    = False
        self.sendingMonitor             = False
        self.reading                    = False
        self.connected                  = False
        self.monitor                    = None
        self.run                        = False
  
        self.init()


    def __del__(self):
        self.disconnect()


    #------------------------------------------------------
    # CONNECTION
    #------------------------------------------------------


    def init_default(self):
        self.fast = False
        self.shout = False
        self.device_info()
        self.wifi_firmware()
        #self.device_history()
        if self.isKettle:
            self.kettle_settings()
            self.calibrate_base()
        elif self.isCoffee:
            self.coffee_settings()
            self.coffee_single_cup_mode()
            self.coffee_carafe()


    def monitor_device(self):
        self.reading = False
        
        previousResponse = ""
        previousWaterSensor = self.waterSensor
        
        prevPreviousTemperature = self.temperature
        previousTemperature = self.temperature
        previousAverage = self.temperature
        
        self.waterSensorStable  = self.waterSensor
        self.temperatureStable  = self.temperature
        
        monitorCount = 0
        self.run = True
   
        #printsend = True
        #printmonitor = True
        timeout = 40
        while self.run:
            self.reading = True
            if not self.sending:
                
                #if printmonitor:
                #    print "Monitor Read"
                
                #printmonitor = False
                
                #printsend = True
                
                try:
                    response = self.read()
                    monitorCount += 1
                    if previousResponse != response:
                        previousResponse = response
                        # call monitor function
                        # ...else got one! yeah! print it!
                except:
                    # do something?
                    print(traceback.format_exc())
                    print "There was an error"
                    self.disconnect()
                    #raise SmarterErrorOld("Monitor Error")
                
                dump = self.dump
                
                if self.dump_status:
                    self.dump = True;
                else:
                    self.dump = False;
                
                if monitorCount % timeout == timeout - 1:
                    if self.isKettle:   self.send_message(Smarter.number_to_raw(Smarter.CommandBase))
                    if self.isCoffee:   self.send_message(Smarter.number_to_raw(Smarter.CommandSingleCupMode))

                if monitorCount % timeout == timeout - 9:
                    if self.isCoffee:   self.send_message(Smarter.number_to_raw(Smarter.CommandCarafe))

                if monitorCount % timeout == timeout - 19:
                    if self.isKettle:   self.send_message(Smarter.number_to_raw(Smarter.CommandKettleSettings))
                    if self.isCoffee:   self.send_message(Smarter.number_to_raw(Smarter.CommandCoffeeSettings))

                if monitorCount % timeout == timeout - 29:
                    if self.isKettle:   self.send_message(Smarter.number_to_raw(Smarter.CommandKettleHistory))
                    if self.isCoffee:   self.send_message(Smarter.number_to_raw(Smarter.CommandCoffeeHistory))

                self.dump = dump


                if previousWaterSensor - 3 > self.waterSensor or previousWaterSensor + 3 < self.waterSensor:
                    self.waterSensorStable = self.waterSensor
                    previousWaterSensor = self.waterSensor
                
                average = int(round(float((float(previousTemperature) + float(prevPreviousTemperature) + float(self.temperature))/3),0))

                if previousAverage != average:
                    self.temperatureStable = average
                    previousAverage = average

                prevPreviousTemperature = previousTemperature
                previousTemperature = self.temperature
            #else:
                #printmonitor = True
                #if printsend:
                #    print "Sending Message"
                #printsend = False
            else:
                pass
            self.reading = False
    
 
     #------------------------------------------------------
    # TRANSMISSION
    #------------------------------------------------------


    # MESSAGE READ


    def read_message(self):
        try:
            if not self.connected:
                self.connect()
            message = ""
            raw = self.socket.recv(1)
            id = Smarter.raw_to_number(raw)
            #r = random.random()
            #print "read" + str(r)
            # debug
            #print "[" + Smarter.number_to_code(id) + "]"
            minlength = Smarter.message_response_length(id)

            i = 1
            while raw != Smarter.number_to_raw(Smarter.MessageTail) or (minlength > 0 and raw == Smarter.number_to_raw(Smarter.MessageTail) and i < minlength):
                
            
                message += raw
                raw = self.socket.recv(1)
                
                # debug
                #print "[" + Smarter.raw_to_code(raw) + "]"
                
                i += 1
            self.readBytesCount += i
            message += raw
            self.readMessage = message
            self.readCount += 1
            
            if id in self.responseCount:
                self.responseCount[id] += 1
            else:
                self.responseCount[id] = 1
 
            #print "readend" + str(r)
       
            return message

        except socket.error, msg:
            raise SmarterErrorOld("Could not read message (" + msg[1] + ")")
        except:
            raise SmarterErrorOld("Could not read message")


    # MESSAGE READ PROTOCOL

    def read(self):
        message = self.read_message()
        id = Smarter.raw_to_number(message[0])
        
        if   id == Smarter.ResponseKettleStatus:    self.decode_ResponseKettleStatus(message)
        elif id == Smarter.ResponseCoffeeStatus:    self.decode_ResponseCoffeeStatus(message)
        elif id == Smarter.ResponseCommandStatus:   self.decode_ResponseCommandStatus(message)
        elif id == Smarter.ResponseBase:            self.decode_ResponseBase(message)
        elif id == Smarter.ResponseCarafe:          self.decode_ResponseCarafe(message)
        elif id == Smarter.ResponseSingleCupMode:   self.decode_ResponseSingleCupMode(message)
        elif id == Smarter.ResponseKettleHistory:   self.decode_ResponseKettleHistory(message)
        elif id == Smarter.ResponseCoffeeHistory:   self.decode_ResponseCoffeeHistory(message)
        elif id == Smarter.ResponseKettleSettings:  self.decode_ResponseKettleSettings(message)
        elif id == Smarter.ResponseDeviceInfo:      self.decode_ResponseDeviceInfo(message)
        elif id == Smarter.ResponseWifiFirmware:    self.decode_ResponseWifiFirmware(message)
        elif id == Smarter.ResponseWirelessNetworks:self.decode_ResponseWirelessNetworks(message)
        
        if self.dump:
            if self.dump_status:
                #if id == Smarter.ResponseCoffeeStatus or id == Smarter.ResponseKettleStatus:
                self.print_message_read(message)
                #print "self dumo"
            else:
                if self.sending and id != Smarter.ResponseCoffeeStatus and id != Smarter.ResponseKettleStatus:
                    self.print_message_read(message)
                #print "dump"

        return message


    # MESSAGE SEND
    

    def send_message(self,message):
        try:
            if not self.connected:
                self.connect()
            if len(message) == 0:
                raise SmarterErrorOld("Cannot send an empty message")
            self.socket.send(message)
        except socket.error, msg:
            raise SmarterErrorOld("Could not send message (" + msg[1] + ")")
        except Exception,e:
            print str(e)
            print(traceback.format_exc())
            raise SmarterErrorOld("Could not send message")

        self.sendBytesCount += len(message)

        id = Smarter.raw_to_number(message[0])
        self.sendCount += 1
        if id in self.commandCount:
            self.commandCount[id] += 1
        else:
            self.commandCount[id] = 1

        self.sendMessage = message
        if self.dump:
            self.print_message_send(message)


    # MESSAGE SEND PROTOCOL

    def send_command(self,id,arguments=""):
        x = Smarter.message_connection(id)
        if len(x) != 0:
            # that whole fast thing should be fixed.
            if x[0] != Smarter.ResponseCommandStatus:
                self.fast = False
        else:
            self.fast = False
        self.send(Smarter.number_to_raw(id) + arguments + Smarter.number_to_raw(Smarter.MessageTail))


    def send(self,message):
        
        #if self.reading:
        #    while self.sending:
        #        print "Waiting for send"
        #        pass
 
        if self.sending:
            while self.sending:
                pass
        
        self.sending = True
        
        if self.reading:
            while self.reading and self.connected:
                pass

        #if not self.connected:
        #    self.sending = False
        #    return
        
        try:
            self.send_message(message)
        except:
            self.sending = False
            self.disconnect()
            return

        
        if self.shout:
            self.sending = False
            self.disconnect()
            return

        self.read()
        data = Smarter.raw_to_number(self.readMessage[0])
        
        while (data == Smarter.ResponseKettleStatus) or (data == Smarter.ResponseCoffeeStatus):
            try:
                self.read()
            except:
                self.sending = False
                self.disconnect()
                return
            
            data = Smarter.raw_to_number(self.readMessage[0])
         
        self.responseMessage = self.readMessage

        if self.fast:
            self.sending = False
            self.disconnect()
            return
        # read until right message.... no threaded read
        
        # Smarter.message_connection(raw_to_number(self.readMessage[0])[0]
        try:
            self.read()
        except:
            self.sending = False
            self.disconnect()
            return
            

        data = Smarter.raw_to_number(self.readMessage[0])
        while (data != Smarter.ResponseKettleStatus) and (data != Smarter.ResponseCoffeeStatus):
            try:
                self.read()
            except:
                self.sending = False
                self.disconnect()
                return
            data = Smarter.raw_to_number(self.readMessage[0])

        self.sending = False
        
        
 
    def connect(self):
        self.disconnect()
        self.init()
        if self.host == "":
            self.host = Smarter.DirectHost
        try:
            print "Connecting..." + self.host
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(15)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.connectCount += 1
        except socket.error, msg:
            raise SmarterErrorOld("Could not connect to + " + self.host + " (" + msg[1] + ")")

        if not self.fast and not self.monitor:
            import threading
            self.monitor = threading.Thread(target=self.monitor_device)
            self.reading = False
            self.monitor.start()


    def disconnect(self):
        self.run = False
        if self.connected:
            print "Disconnect..."+self.host
            self.connected = False
            try:
                if self.monitor:
                    self.monitor.join()
            except:
                print "X"
                self.reading = False
                self.sending = False
                self.monitor = None
                raise SmarterError(SmarterClientFailedStopThread,"Could not disconnect from " + self.host)
            try:
                if self.socket:
                    self.socket.close()
            # FIX: Also except thread exceptions..
            except socket.error, msg:
                raise SmarterError(SmarterClientFailedStop,"Could not disconnect from " + self.host + " (" + msg[1] + ")")
 


    def find_devices(self):
        devices = []
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            command = Smarter.number_to_raw(Smarter.CommandDeviceInfo) + Smarter.number_to_raw(Smarter.MessageTail)
            #command = '\x64\x7e'
  
            cs.sendto(command, ('255.255.255.255', self.port))
            cs.settimeout(2)

            # support up to 100 devices
            for i in range (0,100):
                message, server = cs.recvfrom(4)
                # '0x64 type version 0x7e
                if Smarter.raw_to_number(message[0]) == Smarter.ResponseDeviceInfo and Smarter.raw_to_number(message[3]) == Smarter.MessageTail:
                    devices.append((server[0],Smarter.raw_to_number(message[1]),Smarter.raw_to_number(message[2])))
        except:
            pass
        finally:
            cs.close()
        return devices
        
    #------------------------------------------------------
    # MESSAGE RESPONSE DECODERS
    #------------------------------------------------------


    def decode_ResponseKettleSettings(self,message):
        self.defaultKeepWarmTime  = Smarter.raw_to_number(message[2])
        self.defaultTemperature   = Smarter.raw_to_temperature(message[1])
        self.defaultFormulaTemperature = Smarter.raw_to_temperature(message[3])


    def decode_ResponseCoffeeSettings(self,message):
        self.defaultCups          = Smarter.raw_to_number(message[1])
        self.defaultStrength      = Smarter.raw_to_temperature(message[2])
        self.defaultGrinder       = Smarter.raw_to_temperature(message[3])
        self.defaultHotPlate      = Smarter.raw_to_temperature(message[4])


    def decode_ResponseKettleStatus(self,message):
        isKettle = True
        self.statusMessage       = message
        self.kettleStatus        = Smarter.raw_to_number(message[1])
        self.temperature         = Smarter.raw_to_temperature(message[2])
        self.waterSensor         = Smarter.raw_to_watersensor(message[3],message[4])
        self.onBase              = Smarter.is_on_base(message[2])


    def decode_ResponseCoffeeStatus(self,message):
        isCoffee = True
        self.statusMessage       = message
        self.coffeeStatus        = Smarter.raw_to_number(message[1])
        self.waterLevel          = Smarter.raw_to_number(message[2])
        self.strength            = Smarter.raw_to_strength(message[4])
        self.cups                = Smarter.raw_to_cups(message[5])


    def decode_ResponseDeviceInfo(self,message):
        self.isCoffee = False
        self.isKettle = False
        
        self.deviceId = Smarter.raw_to_number(message[1])
        self.version = Smarter.raw_to_number(message[2])

        if self.deviceId == Smarter.DeviceKettle:
            self.isKettle = True
            self.device = "iKettle 2.0"
        
        if self.deviceId == Smarter.DeviceCoffee:
            self.isCoffee = True
            self.device = "SmarterCoffee"


    def decode_ResponseBase(self,message):
        self.waterSensorBase = Smarter.raw_to_watersensor(message[1],message[2])


    def decode_ResponseResponseCarafe(self,message):
        isCoffee = True
        self.carafe = Smarter.raw_to_number(message[1])


    def decode_ResponseSingleCupMode(self,message):
        isCoffee = True
        self.singlecup  = Smarter.raw_to_bool(message[1])


    def decode_ResponseCommandStatus(self,message):
        self.commandStatus = Smarter.raw_to_number(message[1])


    def decode_ResponseWifiFirmware(self,message):
        s = ""
        for i in range(1,len(message)-1):
            x = str(message[i])
            if x in string.printable:
                s += x
        self.WifiFirmware = s


    def decode_ResponseWirelessNetworks(self,message):
        a = ""
        w = []
        db = False
        for i in range(1,len(message)-1):
            x = str(message[i])
            if x == ',':
               db = True
               d = ""
               continue
            elif x == '}':
               db = False
               w += [(a,int(d))]
               a = ""
               continue
            elif not db and x in string.printable:
                a += x
            elif db and x in string.printable:
                d += x
        from operator import itemgetter
    
        # most powerfull wifi on top
        self.Wifi = sorted(w,key=itemgetter(1),reverse=True)


    def decode_ResponseCoffeeHistory(self,message):
        counter = Smarter.raw_to_number(message[1])
        if counter > 0:
            for i in range(0,counter):
                pass
        else:
            pass
  
  
    def decode_ResponseKettleHistory(self,message):
        counter = Smarter.raw_to_number(message[1])
        if counter > 0:
            for i in range(0,counter):
                # read 32 bytes payload
                # queue!!!!
                self.historyTemperature = Smarter.raw_to_temperature(message[i*32+1+2])
                self.historyKeepWarmTime = Smarter.raw_to_keepwarm(message[i*32+2+2])
                self.historyFormulaTemperature = Smarter.raw_to_temperature(message[i*32+3+2])
                self.historyHours   = Smarter.raw_to_temperature(message[i*32+6+2])
                self.historyMinutes = Smarter.raw_to_temperature(message[i*32+7+2])
                self.historyDay     = Smarter.raw_to_temperature(message[i*32+8+2])
                self.historyMonth   = Smarter.raw_to_temperature(message[i*32+9+2])
                self.historyYear    = Smarter.raw_to_temperature(message[i*32+10+2])+1980
                
    
                # CHECK THIS
                
                #print str(self.historyHours) + ":" + str(self.historyMinutes)
                #print str(self.historyDay) + "-" + str(self.historyMonth) + "-" + str(self.historyYear)
                self.historySuccess = Smarter.raw_to_bool(message[i*32+13])
        else:
            self.historyTemperature = 0
            self.historyFormulaTemperature = 0
            self.historySuccess = False
            self.historyKeepWarmTime = 0



    #------------------------------------------------------
    # COMMANDS: Calibrate
    #------------------------------------------------------


    def calibrate(self):
        self.send_command(Smarter.CommandCalibrate)


    def calibrate_base(self):
        self.send_command(Smarter.CommandBase)


    def calibrate_store_base(self,base = 1000):
        self.send_command(Smarter.CommandStoreBase,Smarter.watersensor_to_raw(base))
        self.waterSensorBase = base



    #------------------------------------------------------
    # COMMANDS: iKettle 2.0 & SmarterCoffee 
    #------------------------------------------------------


    def device_raw(self,code):
        dump = self.dump
        self.dump = True
        self.send(Smarter.codes_to_message(code))
        self.dump = dump
        

    def device_info(self):
        self.send_command(Smarter.CommandDeviceInfo)


    def device_check(self):
            if not self.isKettle and not self.isCoffee:
                self.fast = False
                self.device_info()

    def device_store_settings(self,v1,v2,v3,v4):
        self.device_check()
        if self.isKettle:   self.kettle_store_settings(v1,v2,v3,v4)
        elif self.isCoffee: self.coffee_store_settings(v1,v2,v3,v4)


    def device_settings(self):
        self.device_check()
        if self.isKettle:   self.kettle_settings()
        elif self.isCoffee: self.coffee_settings()


    def device_history(self):
        self.device_check()
        if   self.isKettle: self.kettle_history()
        elif self.isCoffee: self.coffee_history()


    def device_stop(self):
        self.device_check()
        if self.isKettle:   self.kettle_stop()
        elif self.isCoffee: self.coffee_stop()


    def device_start(self):
        self.device_check()
        if self.isKettle:   self.kettle_heat()
        elif self.isCoffee: self.coffee_brew()


    def device_default(self):
        self.device_check()
        if self.isKettle:   self.kettle_store_settings()
        elif self.isCoffee: self.coffee_store_settings()


    def device_reset(self):
        self.send_command(Smarter.CommandResetSettings)


    def device_update(self):
        self.send_command(Smarter.CommandUpdate)


    def device_time(self,second = 0,minute = 0,hour = 12,unknown = 0,day = 17, month=1, century = 20,year = 16):
        self.send_command(Smarter.CommandDeviceTime,Smarter.number_to_raw(second) + Smarter.number_to_raw(minute) + Smarter.number_to_raw(hour) + Smarter.number_to_raw(unknown) + Smarter.number_to_raw(day) + Smarter.number_to_raw(month) + Smarter.number_to_raw(century) + Smarter.number_to_raw(year))



    #------------------------------------------------------
    # COMMANDS: Wifi
    #------------------------------------------------------


    def wifi_firmware(self):
        self.send_command(Smarter.CommandWifiFirmware)


    def wifi_scan(self):
        self.send_command(Smarter.CommandWifiScan)


    def wifi_leave(self):
        self.send_command(Smarter.CommandWifiLeave)


    def wifi_join(self,network,password):
        self.send_command(Smarter.CommandWifiNetwork,Smarter.text_to_raw(network))
        self.send_command(Smarter.CommandWifiPassword,Smarter.text_to_raw(password))
        self.send_command(Smarter.CommandWifiJoin)


    #------------------------------------------------------
    # COMMANDS: iKettle 2.0
    #------------------------------------------------------

 
    def kettle_store_settings(self,temperature = 100, timer = 0, formulaOn = False, formulaTemperature = 75):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleStoreSettings, Smarter.keepwarm_to_raw(timer) + Smarter.temperature_to_raw(temperature) + Smarter.bool_to_raw(formulaOn) + Smarter.temperature_to_raw(formulaTemperature))
            if self.commandStatus == Smarter.StatusSucces:
                self.defaultKeepWarmTime        = timer
                self.defaultFormula             = formulaOn
                self.defaultFormulaTemperature  = formulaTemperature
                self.defaultTemperature         = temperature
            else:
               SmarterErrorOld(KettleFailedStoreSettings,"Could not store kettle machine settings")
        else:
            raise SmarterErrorOld(KettleNoMachineStoreSettings,"You need a Kettle machine to store settings")


    def kettle_settings(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleSettings)
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle machine to get its settings")


    def kettle_heat(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandHeatDefault)
        else:
            raise SmarterError(KettleNoMachineHeat,"You need a kettle to heat it")


    def kettle_formula_heat(self,formulaTemperature = 75,keepwarm = 0):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandHeatFormula)
        else:
            raise SmarterError(KettleNoMachineHeatFormula,"You need a kettle to heat in formula mode")


    def kettle_stop(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleStop)
        else:
            raise SmarterError(KettleNoMachineStop,"You need a kettle to stop heating")


    def kettle_history(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandKettleHistory)
        else:
            raise SmarterError(KettleNoMachineHistory,"You need a kettle machine to get its history")



    #------------------------------------------------------
    # COMMANDS: SmarterCoffee 
    #------------------------------------------------------


    def coffee_settings(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeSettings)
        else:
            raise SmarterError(CoffeeNoMachineSettings,"You need a coffee machine to get its settings")


    def coffee_history(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeHistory)
        else:
            raise SmarterError(CoffeeNoMachineHistory,"You need a coffee machine to get its history")


    def coffee_stop(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeStop)
        else:
            raise SmarterError(CoffeeNoMachineStop,"You need a coffee machine to stop brewing coffee")


    def coffee_single_cup_mode(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandSingleCupMode)
        else:
            raise SmarterError(CoffeeNoMachineSingleCupMode,"You need a coffee machine to get its single cup status")


    def coffee_carafe(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCarafe)
        else:
            raise SmarterError(CoffeeNoMachineCarafe,"You need a coffee machine to get its carafe status")


    def coffee_store_settings(self,cups = 1,strength = 1,hotplate = False,grinder = 0):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCoffeeStoreSettings,Smarter.strength_to_raw(strength),Smarter.cups_to_code(cups),Smarter.bool_to_raw(grinder),Smarter.hotplate_to_raw(hotplate))

            if self.commandStatus == Smarter.StatusSucces:
                self.defaultCups = cups
                self.defaultStrength = strength
                self.defaultGrinder = grinder
                self.defaultHotPlate = hotplate
            else:
                raise SmarterError(CoffeeFailedStoreSettings,"Could not store coffee machine settings")

        else:
            raise SmarterError(CoffeeNoMachineStoreSettings,"You need a coffee machine to store settings")
    

    def coffee_brew(self):
        #  cups strength hotplate grinder
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandBrew)
        else:
            raise SmarterError(CoffeeNoMachineBrew,"You need a coffee machine to brew coffee")


    def coffee_hotplate_off(self):
        if self.fast or self.isCoffee == True:
            self.send_command(Smarter.CommandHotplateOff)
        else:
            raise SmarterError(CoffeeNoMachineHotplateOff,"You need a coffee machine to turn off the hotplate")
 

    def coffee_hotplate_on(self, timer=0):
        if self.fast or self.isCoffee == True:
            if timer == 0:
                self.send_command(Smarter.CommandHotplateOff)
            else:
                self.send_command(Smarter.CommandHotplateOn,Smarter.hotplate_to_raw(timer))
            self.hotplate = timer
        else:
            raise SmarterError(CoffeeNoMachineHotplateOn,"You need a coffee machine to turn on the hotplate")


    def coffee_grinder(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandGrinder)
        
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to grind beans")


    def coffee_cups(self,cups=1):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandCups,Smarter.cups_to_raw(cups))
            self.cups = cups
        else:
            raise SmarterError(CoffeeNoMachineCups,"You need a coffee machine to select the number of cups to brew")


    def coffee_strength(self,strength="medium"):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandStrength ,Smarter.strength_to_raw(Smarter.string_to_strength(strength)))
            self.strength = strength
        else:
            raise SmarterError(CoffeeNoMachineStrength,"You need a coffee machine to select the coffee strength")



    #------------------------------------------------------
    # STRING/PRINT SMARTER INFO
    #------------------------------------------------------


    def print_info(self):
        print Smarter.device_info(self.deviceId,self.version)


    def print_singlecupmode(self):
        print "Single cup mode: " + str(self.singlecup)


    def print_carafe(self):
        print "Carafe present: " + str(self.carafe)


    def print_watersensor_base(self):
        print "Watersensor calibration base value: " + str(self.waterSensorBase)


    def print_wireless_networks(self):
        print
        print "         Signal   Wireless Network"
        for i in range(0,len(self.Wifi)):
            
            quality = Smarter.dbm_to_quality(self.Wifi[i][1])
            
            s = ""
            for x in range(quality / 10,10):
                s += " "
            for x in range(0,quality / 10):
                s += "█"

            print "     " + s + "   " + self.Wifi[i][0]
        print


    def print_wifi_firmware(self):
        print
        print self.WifiFirmware
        print
    
    
    def print_settings(self):
        if self.isKettle:
            self.print_kettle_settings()
        elif self.isCoffee:
            self.print_coffee_settings()
            
            
    def print_coffee_settings(self):
        print "Not yet implemented"


    def print_kettle_settings(self):
        print Smarter.string_kettle_settings(self.defaultTemperature,self.defaultFormula, self.defaultFormulaTemperature,self.defaultKeepWarmTime)


    def print_coffee_history(self):
        if not self.historySuccess:
            print "No history available"
            return
        print "Not yet implemented"


    def print_history(self):
        if self.isKettle:
            self.print_kettle_history()
        elif self.isCoffee:
            self.print_coffee_history()


    def print_kettle_history(self):
        # fix this
        if not self.historySuccess:
            print "No history available"
            return
        print "Not yet implemented"
            #print s + Smarter.string_kettle_settings(self.historyTemperature, self.historyFormulaTemperature , self.historyFormulaTemperature,self.historyKeepWarmTime)


    def print_short_kettle_status(self):
        if self.onBase:
            print Smarter.status_kettle_description(self.kettleStatus) + " on base: Temperature " + Smarter.temperature_to_string(self.temperature) + ", watersensor " + str(self.waterSensor)
        else:
            print Smarter.status_kettle_description(self.kettleStatus) + " off base"


    def print_short_status(self):
        if self.isKettle:
            self.print_short_kettle_status()
        elif self.isCoffee:
            self.print_short_coffee_status()


    def print_short_coffee_status(self):
        print Smarter.status_coffee_description(self.coffeeStatus) + ": Water level: " + str(self.waterLevel) + ", setting: " + Smarter.strength_to_string(self.strength) + " " + Smarter.cups_to_string(self.cups)


    def print_kettle_status(self):
        if self.onBase:
            print "Status          " + Smarter.status_kettle_description(self.kettleStatus)
            print "Temperature     " + Smarter.temperature_to_string(self.temperature)
            print "Water sensor    " + str(self.waterSensor) + " (calibration base " + str(self.waterSensorBase) + ")"
        else:
            print "Status          Off base"
        print "Default heating " + Smarter.string_kettle_settings(self.defaultTemperature,self.defaultFormula, self.defaultFormulaTemperature,self.defaultKeepWarmTime)

    def print_coffee_status(self):
        print "Status          " + Smarter.status_coffee_description(self.coffeeStatus)
        print "Water level     " + str(self.waterLevel)
        print "Setting         " + Smarter.strength_to_string(self.strength) + " " + Smarter.cups_to_string(self.cups)


    def print_status(self):
        print
        if self.isKettle:
            self.print_kettle_status()
        elif self.isCoffee:
            self.print_coffee_status()
        print


    def string_connect_status(self):
        return "Connected to [" + self.host + "] " + Smarter.device_info(self.deviceId,self.version)


    def print_connect_status(self):
        print self.string_connect_status()
    
    
    def print_message_send(self,message):
        print "Message Send:     [" + Smarter.message_description(Smarter.raw_to_number(message[0])) + "] [" + Smarter.message_to_codes(message) + "]"


    def print_message_read(self,message):
        id = Smarter.raw_to_number(message[0])
        print "Message Received: [" + Smarter.message_description(id) + "] [" + Smarter.message_to_codes(message) + "]"
        if   id == Smarter.ResponseCommandStatus:   print "Command replied: " + Smarter.status_command(self.commandStatus)
        elif id == Smarter.ResponseWirelessNetworks: self.print_wireless_networks()
        elif id == Smarter.ResponseWifiFirmware:    self.print_wifi_firmware()
        elif id == Smarter.ResponseKettleHistory:   self.print_kettle_history()
        elif id == Smarter.ResponseCoffeeHistory:   self.print_coffee_history()
        elif id == Smarter.ResponseKettleSettings:  self.print_kettle_settings()
        elif id == Smarter.ResponseCarafe:          self.print_carafe()
        elif id == Smarter.ResponseSingleCupMode:   self.print_singlecupmode()
        elif id == Smarter.ResponseDeviceInfo:      self.print_info()
        elif id == Smarter.ResponseBase:            self.print_watersensor_base()
        elif id == Smarter.ResponseKettleStatus:    self.print_short_kettle_status()
        elif id == Smarter.ResponseCoffeeStatus:    self.print_short_coffee_status()
        else:                                       print "Unknown Reply Message"

