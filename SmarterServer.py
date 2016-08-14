# -*- coding: utf8 -*-

import socket
import os
import sys
import * from SmarterProtocol

#------------------------------------------------------
# SMARTER SERVER INTERFACE
#
# Python interface to iKettle 2.0 & Smarter Coffee Devices
#
# https://github.com/Tristan79/iBrew
#
# 2016 Copyright © 2016 Tristan (@monkeycat.nl)
#
# White Tea Leaf Edition (rev 4)
#------------------------------------------------------



#------------------------------------------------------
# SERVER INTERFACE CLASS
#------------------------------------------------------


class SmarterServer:

    protocol = SmarterProtocol()

    def init(self):
        # network
        self.host                       = "192.168.4.1"
        self.port                       = 2081
        self.running                    = False
        
        # device
        self.commandStatus              = protocol.StatusSucces
        self.sendMessage                = Null
        self.readMessage                = Null
        
        # device info
        self.device                     = protocol.DeviceKettle
        self.version                    = 19
    
        # kettle
        self.isKettle                   = True
        self.kettleStatus               = protocol.KettleReady
        self.temperature                = 23
        self.onBase                     = True
        self.defaultTemperature         = 100
        self.defaultKeepWarmTime        = 0
        self.defaultFormula             = False
        self.defaultFormulaTemperature  = 50
        

        
        # coffee
        self.isCoffee                   = False
        self.coffeeStatus               = 0 # unknown
        self.cups                       = 1
        self.strength                   = protocol.CoffeeMedium
        
        self.hotplate                   = False
        self.grinder                    = False
        
        # watersensor
        self.waterSensorBase            = 1114
        self.waterSensor                = 2119
 
        # Wifi
        self.Wifi                       = ["WirelessNetwork,-53}"]
        self.WifiFirmware               = "AT+GMR\nAT version:0.40.0.0(Aug  8 2015 14:45:58)\nSDK version:1.3.0\ncompile time:Aug  8 2015 17:19:38\nOK"


    def __init__(autospawn = "True"):
        self.init()
        self.autocspawn = autospawn
        self.host = host
        if self.autospawn:
            self.spawn()


    def __del__(self):
        self.disconnect()



    #------------------------------------------------------
    # CONNECTION
    #------------------------------------------------------


    def spawn(self):
        try:
            networksocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            networksocket.bind(("",self.port))
        except socket.error, msg:
            raise SmarterError("Could not bind (" + msg[1] + ")")
        self.socket = networksocket
        self.running = True


    def disconnect(self):
        if self.running:
            self.init()
            try:
                self.socket.close()
            except socket.error, msg:
                raise SmarterError("Could not disconnect " + self.host + " (" + msg[1] + ")")



    #------------------------------------------------------
    # MESSAGE RESPONSE ENCODERS
    #------------------------------------------------------


    def encode_ResponseSettings(self,message):
        pass
    
    
    def encode_ResponseCommandStatus(self,status):
        if self.is_status_command(status):
        pass


    def encode_ResponseDeviceInfo(self,message):
        pass
    

    def encode_ResponseCalibrationBase(self,base):
        self.send(protocol.ResponseCalibrationBase + protocol.raw_to_watersensor(base)
        pass


    def encode_ResponseStatus(self,message):
        pass


    def encode_ResponseWifiList(self,message):
        pass


    def encode_ResponseWifiFirmware(self,message):
        pass


    def encode_ResponseHistory(self,message):
        pass



    #------------------------------------------------------
    # MESSAGE COMMAND DECODERS
    #------------------------------------------------------


    def send_succes(self):
        send(encode_ResponseStatus(protocol.StatusSucces))


    def send_failure(self):
        send(encode_ResponseStatus(protocol.StatusFailure))

    def decode_CommandDeviceTime(self,message):
        # arg 00 00 00 00 00 00 00 00
        # return time
        pass


    def decode_CommandReset(self,message):
        pass


    def decode_CommandStop(self,message):
        pass


    def decode_CommandHistory(self,message):
        pass


    def decode_CommandInfo(self,message):
        pass


    def decode_CommandUpdate(self,message):
        pass


    def decode_CommandWifiName(self,message):
        pass


    def decode_CommandWifiPassword(self,message):
        pass


    def decode_CommandWifiConnect(self,message):
        pass


    def decode_CommandWifiScan(self,message):
        pass


    def decode_CommandWifiReset(self,message):
        pass


    def decode_CommandWifiFirmware(self,message):
        self.send(self.encode_ResponseWifiFirmware())
        pass


    def decode_CommandBrew(self,message):
        pass


    def decode_CommandStrength(self,message):
        #self.cups = protocol.raw_to_cups(message[1])
        self.send_succes()
        pass


    def decode_CommandCups(self,message):
        self.cups = protocol.raw_to_cups(message[1])
        self.send_succes()


    def decode_CommandBrewDefault(self,message):
        pass


    def decode_CommandGrinder(self,message):
        self.grinder = not self.grinder
        self.send_succes()


    def decode_CommandHotplateOn(self,message):
        self.hotplate = True
        self.send_succes()


    def decode_CommandHotplateOff(self,message):
        self.hotplate = False
        self.send_succes()


    def decode_CommandHeat(self,message):
        pass


    def decode_CommandHeatFormula(self,message):
        pass


    def decode_CommandHeatDefault(self,message):
        
        pass


    def decode_CommandStoreSettings(self,message):
        self.defaultKeepWarmTime       = protocol.raw_to_timer(message[1])
        self.defaultTemperature        = protocol.raw_to_temperature(message[2])
        self.defaultFormula            = protocol.raw_to_bool(message[3])
        self.defaultFormulaTemperature = protocol.raw_to_temperature(message[4])
        self.send_succes()
        pass


    def decode_CommandSettings(self,message):
        
        # protocol.CommandStoreSettings
        pass


    def decode_CommandStoreBase(self,message):
        self.base = protocol.raw_to_watersensor(message[2],message[2])
        self.send_succes()
  

    def decode_CommandBase(self,message):
        send(encode_ResponseCalibrationBase(self.base))


    def decode_CommandCalibrate(self,message):
        send(encode_ResponseCalibrationBase(self.base))


    def decode_Command20(self,message):
        self.send_failure()


    def decode_Command22(self,message):
        self.send_failure()


    def decode_Command23(self,message):
        self.send_failure()


    def decode_Command30(self,message):
        self.send_failure()


    def decode_Command32(self,message):
        self.send_failure()


    def decode_Command40(self,message):
        self.send_failure()


    def decode_Command41(self,message):
        self.send_failure()


    def decode_Command43(self,message):
        self.send_failure()


    def decode_Command69(self,message):
        self.send_failure()

    #------------------------------------------------------
    # TRANSMISSION
    #------------------------------------------------------


    # MESSAGE READ
  
    def read_message(self):
        try:
            message = ""
            raw = self.socket.recv(1)
            while raw != protocol.MessageTail:
                message += raw
                raw = self.socket.recv(1)
            message += data
            self.readMessage = message
            return message

        except socket.error, msg:
            raise SmarterError("Could not read message (" + msg[1] + ")")


    # MESSAGE READ PROTOCOL

    def read(self):
        message = self.read_message()
        if   message[0] == protocol.CommandDeviceTime        self.decode_CommandDeviceTime(message)
        elif message[0] == protocol.CommandReset             self.decode_CommandReset(message)
        elif message[0] == protocol.CommandStop              self.decode_CommandStop(message)
        elif message[0] == protocol.CommandHistory           self.decode_CommandHistory(message)
        elif message[0] == protocol.CommandInfo              self.decode_CommandInfo(message)
        elif message[0] == protocol.CommandUpdate            self.decode_CommandUpdate(message)
        elif message[0] == protocol.CommandWifiName          self.decode_CommandWifiName(message)
        elif message[0] == protocol.CommandWifiPassword      self.decode_CommandWifiPassword(message)
        elif message[0] == protocol.CommandWifiConnect       self.decode_CommandWifiConnect(message)
        elif message[0] == protocol.CommandWifiScan          self.decode_CommandWifiScan(message)
        elif message[0] == protocol.CommandWifiReset         self.decode_CommandWifiReset(message)
        elif message[0] == protocol.CommandWifiFirmware      self.decode_CommandWifiFirmware(message)
        elif message[0] == protocol.CommandBrew              self.decode_CommandBrew(message)
        elif message[0] == protocol.CommandStrength          self.decode_CommandStrength(message)
        elif message[0] == protocol.CommandCups              self.decode_CommandCups(message)
        elif message[0] == protocol.CommandBrewDefault       self.decode_CommandBrewDefault(message)
        elif message[0] == protocol.CommandGrinder           self.decode_CommandGrinder(message)
        elif message[0] == protocol.CommandHotplateOn        self.decode_CommandHotplateOn(message)
        elif message[0] == protocol.CommandHotplateOff       self.decode_CommandHotplateOff(message)
        elif message[0] == protocol.CommandHeat              self.decode_CommandHeat(message)
        elif message[0] == protocol.CommandHeatFormula       self.decode_CommandHeatFormula(message)
        elif message[0] == protocol.CommandHeatDefault       self.decode_CommandHeatDefault(message)
        elif message[0] == protocol.CommandStoreSettings     self.decode_CommandStoreSettings(message)
        elif message[0] == protocol.CommandSettings          self.decode_CommandSettings(message)
        elif message[0] == protocol.CommandStoreBase         self.decode_CommandStoreBase(message)
        elif message[0] == protocol.CommandBase              self.decode_CommandBase(message)
        elif message[0] == protocol.CommandCalibrate:        self.decode_CommandCalibrate(message)
        elif message[0] == protocol.Command20:               self.decode_Command20(message)
        elif message[0] == protocol.Command22:               self.decode_Command22(message)
        elif message[0] == protocol.Command23:               self.decode_Command23(message)
        elif message[0] == protocol.Command30:               self.decode_Command30(message)
        elif message[0] == protocol.Command32:               self.decode_Command32(message)
        elif message[0] == protocol.Command40:               self.decode_Command40(message)
        elif message[0] == protocol.Command41:               self.decode_Command41(message)
        elif message[0] == protocol.Command43:               self.decode_Command43(message)
        elif message[0] == protocol.Command69:               self.decode_Command69(message)
        else:
            self.send_message(encode_ResponseCommandStatus(protocol.StatusInvalid))
       

    # MESSAGE SEND PROTOCOL

    def send(self,message):
        try:
            if len(message) > 0 and message[len(message)-1] == iBrewTail:
                self.socket.send(message)
            elif len(message) > 0:
                self.socket.send(message+self.MessageTail)
            else:
                raise SmarterError("Cannot send an empty message")
                return
        except socket.error, msg:
            raise SmarterError("Could not read message (" + msg[1] + ")")
        else
            self.sendMessage = message