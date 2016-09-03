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


def threadsafe_function(fn):
    """decorator making sure that the decorated function is thread safe"""
    lock = threading.Lock()
    def new(*args, **kwargs):
        
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            #print(traceback.format_exc())
            #print str(e)
            raise e
        finally:
            lock.release()
        return r
    return new

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
        self.historySuccess             = 0
        
        # device info
        self.device                     = "None"
        self.deviceId                   = 0
        self.version                    = 0
    
        # kettle
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
        self.coffeeStatus               = 0 # unknown
        self.cups                       = 1
        self.strength                   = Smarter.CoffeeMedium
        self.carafe                     = False
        self.hotPlate                   = False
        self.grinder                    = False
        self.cupsBit                    = False
        self.waterEnough                = False

        self.ready                      = False
        self.heating                    = False
        self.hotPlateOn                 = False
        self.grinderOn                  = False
        self.working                    = False
        
        self.singlecup                  = False
        self.carafeMode                 = False
        
        self.defaultCups                = 1
        self.defaultStrength            = 1
        self.defaultGrinder             = False
        self.defaultHotPlate            = 0
        
        self.waterLevel                 = 0
        
 
        # Wifi
        self.Wifi                       = []
        self.WifiFirmware               = "None"
        isDirect                        = False

        self.isKettle                   = False
        self.isCoffee                   = False

        self.writeLock                  = threading.Lock()
        self.socketLock                 = threading.Lock()

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
        self.writeLock                  = threading.Lock()
        self.socketLock                 = threading.Lock()
        self.connected                  = False
        self.monitor                    = None
        self.socket                     = None
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
            self.kettle_calibrate_base()
        elif self.isCoffee:
            self.coffee_settings()
            #self.coffee_single_cup_mode()
            #self.coffee_carafe()


    def monitor_device(self):
        if self.dump:
            print "[" + self.host + "] Monitor Running"
        previousResponse = ""
        previousWaterSensor = self.waterSensor
        
        prevPreviousTemperature = self.temperature
        previousTemperature = self.temperature
        previousAverage = self.temperature
        
        self.waterSensorStable  = self.waterSensor
        self.temperatureStable  = self.temperature
        
        monitorCount = 0
   
        timeout = 40
        self.run = True
        while self.run:
                try:
                    self.writeLock.acquire()
                except:
                    self.disconnect()
                    #print(traceback.format_exc())
 
                    break
                    raise SmarterErrorOld("Monitor Error")
                try:
                    if not self.connected:
                        #print(traceback.format_exc())
                        break
                    
                    response = self.read()
                    monitorCount += 1
                    if previousResponse != response:
                        previousResponse = response
                        # call monitor function
                        # ...else got one! yeah! print it!
  
                except:
                    #print(traceback.format_exc())
                    if self.writeLock.locked():
                        self.writeLock.release()
                    self.disconnect()
                    break
                    raise SmarterErrorOld("Monitor Error")
                
                self.writeLock.release()
                
                dump = self.dump
                
                if self.dump_status:
                    self.dump = True;
                else:
                    self.dump = False;


                try:
                    if monitorCount % timeout == timeout - 9:
                        if self.isKettle:   self.kettle_calibrate_base()
                    #    if self.isCoffee:   self.coffee_carafe()

                    #if monitorCount % timeout == timeout - 9:
                    #    if self.isCoffee:   self.coffee_single_cup_mode()

                    if monitorCount % timeout == timeout - 19:
                        self.device_settings()

                    if monitorCount % timeout == timeout - 29:
                        self.device_history()
                except:
                    #print(traceback.format_exc())
                    self.disconnect()
                    self.dump = dump
                    break
                    raise SmarterErrorOld("Monitor Error")


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
        if self.dump:
            print "[" + self.host + "] Monitor Stopped"
 
     #------------------------------------------------------
    # TRANSMISSION
    #------------------------------------------------------


    # MESSAGE READ
    def read_message(self):
        try:
            message = ""
            raw = self.socket.recv(1)
            id = Smarter.raw_to_number(raw)
            # debug
            #print "[" + Smarter.number_to_code(id) + "]",
            minlength = Smarter.message_response_length(id)

            i = 1
            while raw != Smarter.number_to_raw(Smarter.MessageTail) or (minlength > 0 and raw == Smarter.number_to_raw(Smarter.MessageTail) and i < minlength):
                message += raw
                raw = self.socket.recv(1)
                # debug
                #print "[" + Smarter.raw_to_code(raw) + "]",
                i += 1
            message += raw
            self.readMessage = message
            
            self.readCount += 1
            self.readBytesCount += i
            if id in self.responseCount:
                self.responseCount[id] += 1
            else:
                self.responseCount[id] = 1
 
            return message

        except socket.error, msg:
            raise SmarterErrorOld("Could not read message") # (" + msg + ")")


    # MESSAGE READ PROTOCOL
    def read(self):
        if not self.connected:
            raise SmarterErrorOld("Could not read message not connected")
   
    
        try:
            self.socketLock.acquire()
        except:
            raise SmarterErrorOld("Could not read message")
    
        if self.connected:
     
            message = self.read_message()
            id = Smarter.raw_to_number(message[0])
            try:
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
            except:
                print(traceback.format_exc())
 
            if self.dump:
                if self.dump_status:
                    self.print_message_read(message)
                else:
                    #fix
                    if id != Smarter.ResponseCoffeeStatus and id != Smarter.ResponseKettleStatus:
                        self.print_message_read(message)
        
            self.socketLock.release()
            return message
        else:
            self.socketLock.release()
            raise SmarterErrorOld("Could not read message disconnected")


    # MESSAGE SEND
    def send_message(self,message):
        if len(message) == 0:
            raise SmarterErrorOld("Cannot send an empty message")
    
        try:
            self.socket.send(message)
        except socket.error, msg:
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
        if not self.connected:
            raise SmarterErrorOld("Could not write message not connected")
        
        try:
            self.writeLock.acquire()
        except:
            raise SmarterErrorOld("Could not write message")

        try:
            self.socketLock.acquire()
        except:
            raise SmarterErrorOld("Could not write message")

        if self.connected:
            try:
                self.send_message(message)
            except:
                self.socketLock.release()
                self.writeLock.release()
                self.disconnect()
                raise SmarterErrorOld("Could not send message")
            
            self.socketLock.release()
        
            if self.shout:
                self.writeLock.release()
                return

            try:
                self.read()
            except:
                self.disconnect()
                #print(traceback.format_exc())
                raise SmarterErrorOld("Could not write message (no response)")
            
            data = Smarter.raw_to_number(self.readMessage[0])
            
            while (data == Smarter.ResponseKettleStatus) or (data == Smarter.ResponseCoffeeStatus):
                try:
                    self.read()
                except:
                    self.writeLock.release()
                    self.disconnect()
                    raise SmarterErrorOld("Could not write message (no response)")
                
                data = Smarter.raw_to_number(self.readMessage[0])
             
            self.responseMessage = self.readMessage

            if self.fast:
                self.writeLock.release()
                return
            
            # Smarter.message_connection(raw_to_number(self.readMessage[0])[0]
            try:
                self.read()
            except:
                self.disconnect()
                self.writeLock.release()
                raise SmarterErrorOld("Could not write message (no response)")
            

            data = Smarter.raw_to_number(self.readMessage[0])
            while (data != Smarter.ResponseKettleStatus) and (data != Smarter.ResponseCoffeeStatus):
                try:
                    self.read()
                except:
                    self.disconnect()
                    self.writeLock.release()
                    raise SmarterErrorOld("Could not write message (no response)")
                data = Smarter.raw_to_number(self.readMessage[0])

        else:
            self.writeLock.release()
            raise SmarterErrorOld("Could not read message disconnected")
        self.writeLock.release()
        
        
 
    @threadsafe_function
    def connect(self):
        #print "CONNECT " + self.host
        self.init()
        
        if self.host == "":
            self.host = Smarter.DirectHost
  
        from wireless import Wireless
        wireless = Wireless()
        wirelessname = wireless.current()
        if wirelessname is not None:
            if (wirelessname[0:14] == "Smarter Coffee" or wirelessname[0:11] == "iKettle 2.0") and self.host == Smarter.DirectHost:
                self.isDirect = True
            else:
                self.isDirect = False
        else:
            self.isDirect = False
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.connectCount += 1
        except socket.error, msg:
            raise SmarterErrorOld("Could not connect to + " + self.host + " (" + str(msg) + ")")

        if not self.fast and not self.monitor:
            import threading
            try:
                self.monitor = threading.Thread(target=self.monitor_device)
                self.monitor.start()
            except:
                raise SmarterErrorOld("Could not start monitor")
                


    @threadsafe_function
    def disconnect(self):
        #print "DISCONNECT "+self.host
        self.run = False
        if self.connected:
            self.connected = False
            try:
                if self.monitor:
                    if self.writeLock.locked():
                        self.writeLock.release()
                    if self.socketLock.locked():
                        self.socketLock.release()
            except:
                raise SmarterError(SmarterClientFailedStopThread,"Could not disconnect from " + self.host)

            self.monitor = None
            try:
                if self.socket:
                    self.socket.close()
                    self.socket = None
            # FIX: Also except thread exceptions..
            except socket.error, msg:
                self.socker = None
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
            cs.settimeout(4)

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
        self.defaultStrength      = Smarter.raw_to_strength(message[2])
        self.defaultGrinder       = Smarter.raw_to_bool(message[3])
        self.defaultHotPlate      = Smarter.raw_to_hotplate(message[4])


    def decode_ResponseKettleStatus(self,message):
        isKettle = True
        self.statusMessage       = message
        self.kettleStatus        = Smarter.raw_to_number(message[1])
        self.temperature         = Smarter.raw_to_temperature(message[2])
        self.waterSensor         = Smarter.raw_to_watersensor(message[3],message[4])
        self.onBase              = Smarter.is_on_base(message[2])
        #self.unknown5            = Smarter.raw_to_number(message[5])


    def decode_ResponseCoffeeStatus(self,message):
    
        def is_set(x, n):
            return x & 2**n != 0
        
        isCoffee = True
        self.statusMessage       = message
        self.coffeeStatus        = Smarter.raw_to_number(message[1])
        
        self.carafe              = is_set(self.coffeeStatus,0)
        self.grinder             = is_set(self.coffeeStatus,1)
        self.ready               = is_set(self.coffeeStatus,2)
        self.heating             = is_set(self.coffeeStatus,4)
        self.working             = is_set(self.coffeeStatus,6)
        self.hotPlateOn          = is_set(self.coffeeStatus,5)
        self.grinderOn           = is_set(self.coffeeStatus,3)
        #self.unknown2            = is_set(self.coffeeStatus,7)
        
        self.waterLevel          = Smarter.raw_to_waterlevel(message[2])
        self.waterEnough         = Smarter.raw_to_waterlevel_bit(message[2])
        self.strength            = Smarter.raw_to_strength(message[4])
        self.cups                = Smarter.raw_to_cups(message[5])
        self.cupsBit             = Smarter.raw_to_cups_bit(message[5])
        #self.unknown3            = Smarter.raw_to_number(message[3])


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


    def decode_ResponseCarafe(self,message):
        isCoffee = True
        self.carafeMode = Smarter.raw_to_number(message[1])


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
                self.historySuccess = Smarter.raw_to_bool(message[i*32+13])
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
        self.fast = False
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
    # COMMANDS: Kettle Calibrate
    #------------------------------------------------------


    def kettle_calibrate(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandCalibrate)
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle to calibrate")


    def kettle_calibrate_base(self):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandBase)
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle to get its calibration base value")


    def kettle_calibrate_store_base(self,base = 1000):
        if self.fast or self.isKettle:
            self.send_command(Smarter.CommandStoreBase,Smarter.watersensor_to_raw(base))
            self.waterSensorBase = base
        else:
            raise SmarterErrorOld(KettleNoMachineSettings,"You need a Kettle to set its calibration base value")



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
            self.send_command(Smarter.CommandCoffeeStoreSettings,Smarter.strength_to_raw(strength)+Smarter.cups_to_raw(cups)+Smarter.bool_to_raw(grinder)+Smarter.hotplate_to_raw(hotplate))

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
            self.send_command(Smarter.CommandBrewDefault)
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
            self.hotPlate = timer
        else:
            raise SmarterError(CoffeeNoMachineHotplateOn,"You need a coffee machine to turn on the hotplate")


    def coffee_grinder_toggle(self):
        if self.fast or self.isCoffee:
            self.send_command(Smarter.CommandGrinder)
        
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to toggle the grinder")


    def coffee_filter(self):
        if self.isCoffee and self.grinder:
            self.send_command(Smarter.CommandGrinder)
        else:
            raise SmarterError(CoffeeNoMachineGrinder,"You need a coffee machine to use the filter")


    def coffee_grinder(self):
        if self.isCoffee and not self.grinder:
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
        print "Carafe present: " + str(self.carafeMode)


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
        print Smarter.string_coffee_settings(self.defaultCups, self.defaultStrength, self.defaultGrinder, self.defaultHotPlate)


    def print_kettle_settings(self):
        print Smarter.string_kettle_settings(self.defaultTemperature, self.defaultFormula, self.defaultFormulaTemperature, self.defaultKeepWarmTime)


    def print_coffee_history(self):
        # fix this
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
        print Smarter.string_coffee_status(self.ready, self.working, self.heating, self.hotPlateOn, self.carafe, self.grinderOn) + ", Water " + Smarter.waterlevel(self.waterLevel) + ", setting: " + Smarter.string_coffee_settings(self.cups, self.strength, self.grinder, self.hotPlate)
        print "Bits            [cups:" + str(self.cupsBit) + "] [water level:" + str(self.waterEnough) + "]"


    def print_kettle_status(self):
        if self.onBase:
            print "Status          " + Smarter.status_kettle_description(self.kettleStatus)
            print "Temperature     " + Smarter.temperature_to_string(self.temperature)
            print "Water sensor    " + str(self.waterSensor) + " (calibration base " + str(self.waterSensorBase) + ")"
        else:
            print "Status          Off base"
        print "Default heating " + Smarter.string_kettle_settings(self.defaultTemperature,self.defaultFormula, self.defaultFormulaTemperature,self.defaultKeepWarmTime)


    def print_coffee_status(self):
        print "Status          " + Smarter.string_coffee_status(self.ready, self.working, self.heating, self.hotPlateOn, self.carafe, self.grinderOn)
        print "Water level     " + Smarter.waterlevel(self.waterLevel)
        print "Setting         " + Smarter.string_coffee_settings(self.cups, self.strength, self.grinder, self.hotPlate)
        print "Default Setting " + Smarter.string_coffee_settings(self.defaultCups, self.defaultStrength, self.defaultGrinder, self.defaultHotPlate)
        print "Bits            [cups:" + str(self.cupsBit) + "] [water level:" + str(self.waterEnough) + "]"


    def print_status(self):
        print
        if self.isKettle:
            self.print_kettle_status()
        elif self.isCoffee:
            self.print_coffee_status()
        print


    def string_connect_status(self):
        if self.connected:
            s = ""
            if self.isDirect:
                s = " directly"
            return "Connected" + s + " to [" + self.host + "] " + Smarter.device_info(self.deviceId,self.version)
        return "Not connected"


    def print_connect_status(self):
        print self.string_connect_status()
    

    def print_devices_found(self,devices):
        for i in range(0,len(devices)):
            print "Found " + Smarter.device_info(devices[i][1],devices[i][2]) + " [" + devices[i][0] + "]"
        if len(devices) == 0:
            print "No coffee machine or kettle found"


    def print_message_send(self,message):
        print "[" + self.host + "] Message Send     [" + Smarter.message_description(Smarter.raw_to_number(message[0])) + "] [" + Smarter.message_to_codes(message) + "]"


    def print_message_read(self,message):
        id = Smarter.raw_to_number(message[0])
        print "[" + self.host + "] Message Received [" + Smarter.message_description(id) + "] [" + Smarter.message_to_codes(message) + "]"
        if   id == Smarter.ResponseCommandStatus:   print "Command replied: " + Smarter.status_command(self.commandStatus)
        elif id == Smarter.ResponseWirelessNetworks: self.print_wireless_networks()
        elif id == Smarter.ResponseWifiFirmware:    self.print_wifi_firmware()
        elif id == Smarter.ResponseKettleHistory:   self.print_kettle_history()
        elif id == Smarter.ResponseCoffeeHistory:   self.print_coffee_history()
        elif id == Smarter.ResponseKettleSettings:  self.print_kettle_settings()
        elif id == Smarter.ResponseCoffeeSettings:  self.print_coffee_settings()
        elif id == Smarter.ResponseCarafe:          self.print_carafe()
        elif id == Smarter.ResponseSingleCupMode:   self.print_singlecupmode()
        elif id == Smarter.ResponseDeviceInfo:      self.print_info()
        elif id == Smarter.ResponseBase:            self.print_watersensor_base()
        elif id == Smarter.ResponseKettleStatus:    self.print_short_kettle_status()
        elif id == Smarter.ResponseCoffeeStatus:    self.print_short_coffee_status()
        else:                                       print "Unknown Reply Message"

