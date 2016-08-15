# -*- coding: utf8 -*-

import socket
import os
import sys
from SmarterProtocol import *

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


    def init(self):
        # network
        self.host                       = "192.168.4.1"
        self.port                       = 2081
        self.running                    = False
        
        # device
        self.commandStatus              = Smarter.StatusSucces
        self.sendMessage                = Null
        self.readMessage                = Null
        
        # device info
        self.device                     = Smarter.DeviceKettle
        self.version                    = 19
    
        # kettle
        self.isKettle                   = True
        self.kettleStatus               = Smarter.KettleReady
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
        self.strength                   = Smarter.CoffeeMedium
        
        self.hotplate                   = False
        self.grinder                    = False
        
        # watersensor
        self.waterSensorBase            = 1114
        self.waterSensor                = 2119
 
        # Wifi
        self.Wifi                       = ["WirelessNetwork,-53}"]
        self.WifiFirmware               = "AT+GMR\nAT version:0.40.0.0(Aug  8 2015 14:45:58)\nSDK version:1.3.0\ncompile time:Aug  8 2015 17:19:38\nOK"


    def __init__():
        self.init()
        self.host = host
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
                raise SmarterError("Could not disconnect server (" + msg[1] + ")")


    def run(self):
        while True:
            r, _, _ = select.select([self.socket], [], [])
            if r:
                data = self.read_message()
                self.read(data)


    #------------------------------------------------------
    # MESSAGE RESPONSE ENCODERS
    #------------------------------------------------------


    def encode_ResponseSettings(self,message):
        # ORDER BUG BUG HERE WIRESHARK AGAIN!!!!
        # isKettle?
        message = Smarter.encode_ResponseSettings+Smarter.temperature_to_raw(self.defaultTemperature)+Smarter.keepwarm_to_raw(self.defaultKeepWarmTime)+Smarter.temperature_to_raw(self.defaultFormulaTemperature)
        message = message + '\x7e\x00\x03\x00'
        self.send(message)
    
    
    def encode_ResponseCommandStatus(self,status):
        self.send(Smarter.ResponseCommandStatus+Smarter.number_to_raw(status))


    def encode_ResponseDeviceInfo(self,message):
        self.send(Smarter.ResponseDeviceInfo+Smarter.number_to_raw(self.device)+Smarter.number_to_raw(self.version))
   
   
    def encode_ResponseCalibrationBase(self,base):
        # isKettle?
        self.send(Smarter.ResponseCalibrationBase + Smarter.watersensor_to_raw(base))
 

    def encode_ResponseWifiList(self):
        self.send(Smarter.encode_ResponseWifiList + Smarter.text_to_raw(self.Wifi))


    def encode_ResponseWifiFirmware(self):
        self.send(Smarter.encode_ResponseWifiFirmware + Smarter.text_to_raw(self.WifiFirmware))


    def encode_ResponseStatus(self,status):
        message = Smarter.ResponseStatus
        if isKettle:
            message = message + Smarter.number_to_raw(self.kettleStatus) +  Smarter.temperature_to_raw(self.temperature) + Smarter.watersensor_to_raw(self.waterSensor) + '\x00'
        elif isCoffee:
            message = Smarter.number_to_raw(self.coffeeStatus) + Smarter.watersensor_to_raw(self.waterSensor) + Smarter.cups_to_raw(self.cups) + Smarter.number_to_raw(self.strength)
        self.send(message)
    

    def encode_ResponseHistory(self,message):
        self.send(Smarter.ResponseHistory + Smarter.number_to_raw(0))


    #------------------------------------------------------
    # MESSAGE COMMAND DECODERS
    #------------------------------------------------------


    def send_succes(self):
        encode_ResponseStatus(Smarter.StatusSucces)


    def send_failure(self):
        send(encode_ResponseStatus(Smarter.StatusFailure))


    def send_invalid(self):
        send(encode_ResponseStatus(Smarter.StatusInvalid))


    def decode_CommandDeviceTime(self,message):
        seld.send_succes()
        # arg 00 00 00 00 00 00 00 00
        # return time


    def decode_CommandReset(self,message):
        # reset to default settings...
        self.send_succes()
 

    def decode_CommandStop(self,message):
        self.kettleStatus = Smarter.KettleReady
        self.coffeeStatus = '\x04'
        self.send_succes()

    def decode_CommandHistory(self,message):
        send.encode_ResponseHistory()


    def decode_CommandDeviceInfo(self,message):
        self.encode_ResponseDeviceInfo()


    def decode_CommandUpdate(self,message):
        self.send_invalid()


    def decode_CommandWifiName(self,message):
        self.send_succes()


    def decode_CommandWifiPassword(self,message):
        self.send_succes()


    def decode_CommandWifiConnect(self,message):
        # but disconnect anyway....
        pass


    def decode_CommandWifiScan(self,message):
        encode_ResponseWifiList()


    def decode_CommandWifiReset(self,message):
        self.send_succes()
        # set to default
        # disconnect send this!!!


    def decode_CommandWifiFirmware(self,message):
        self.encode_ResponseWifiFirmware()


    def decode_CommandBrew(self,message):
        self.coffeeStatus = Smarter.CoffeeBoiling
        self.send_succes()


    def decode_CommandStrength(self,message):
        self.cups = Smarter.raw_to_strength(message[1])
        self.send_succes()


    def decode_CommandCups(self,message):
        self.cups = Smarter.raw_to_cups(message[1])
        self.send_succes()


    def decode_CommandBrewDefault(self,message):
        self.coffeeStatus = Smarter.CoffeeBoiling
        self.send_succes()


    def decode_CommandGrinder(self,message):
        self.grinder = not self.grinder
        self.send_succes()


    def decode_CommandHotplateOn(self,message):
        # decode timer
        self.hotplate = True
        self.send_succes()


    def decode_CommandHotplateOff(self,message):
        self.hotplate = False
        self.send_succes()


    def decode_CommandHeat(self,message):
        self.kettleStatus = Smarter.KettleBoiling
        self.send_succes()


    def decode_CommandHeatFormula(self,message):
        self.kettleStatus = Smarter.KettleBoiling
        self.send_succes()


    def decode_CommandHeatDefault(self,message):
        self.kettleStatus = Smarter.KettleBoiling
        self.send_succes()


    def decode_CommandStoreSettings(self,message):
        try:
            self.defaultKeepWarmTime       = Smarter.raw_to_keepwarm(message[1])
            self.defaultTemperature        = Smarter.raw_to_temperature(message[2])
            self.defaultFormula            = Smarter.raw_to_bool(message[3])
            self.defaultFormulaTemperature = Smarter.raw_to_temperature(message[4])
        except:
            self.send_failure()
        else:
            self.send_succes()


    def decode_CommandSettings(self,message):
        self.encode_ResponseSettings()


    def decode_CommandStoreBase(self,message):
        self.base = Smarter.raw_to_watersensor(message[2],message[1])
        self.send_succes()
  

    def decode_CommandBase(self,message):
        encode_ResponseCalibrationBase(self.base)
        self.send_succes()


    def decode_CommandCalibrate(self,message):
        self.base = 1020
        encode_ResponseCalibrationBase(self.base)
        self.send_succes()


    def decode_Command20(self,message):
        self.send_invalid()


    def decode_Command22(self,message):
        self.send_invalid()


    def decode_Command23(self,message):
        self.send_invalid()


    def decode_Command30(self,message):
        self.send_invalid()


    def decode_Command32(self,message):
        self.send_invalid()


    def decode_Command40(self,message):
        self.send_invalid()


    def decode_Command41(self,message):
        self.send_invalid()


    def decode_Command43(self,message):
        self.send_invalid()


    def decode_Command69(self,message):
        self.send_invalid()

    #------------------------------------------------------
    # TRANSMISSION
    #------------------------------------------------------


    # MESSAGE READ
  
    def read_message(self):
        try:
            message = ""
            raw = self.socket.recv(1)
            
            # need message length
            while raw != Smarter.MessageTail:
                message += raw
                raw = self.socket.recv(1)
            message += data
            self.readMessage = message
            return message

        except socket.error, msg:
            raise SmarterError("Could not read message (" + msg[1] + ")")


    # MESSAGE READ PROTOCOL

    def reads(self,message):
        if = Smarter.raw_to_number(message[0])
        if   id == Smarter.CommandDeviceTime        self.decode_CommandDeviceTime(message)
        elif id == Smarter.CommandReset             self.decode_CommandReset(message)
        elif id == Smarter.CommandStop              self.decode_CommandStop(message)
        elif id == Smarter.CommandHistory           self.decode_CommandHistory(message)
        elif id == Smarter.CommandDeviceInfo        self.decode_CommandDeviceInfo(message)
        elif id == Smarter.CommandUpdate            self.decode_CommandUpdate(message)
        elif id == Smarter.CommandWifiName          self.decode_CommandWifiName(message)
        elif id == Smarter.CommandWifiPassword      self.decode_CommandWifiPassword(message)
        elif id == Smarter.CommandWifiConnect       self.decode_CommandWifiConnect(message)
        elif id == Smarter.CommandWifiScan          self.decode_CommandWifiScan(message)
        elif id == Smarter.CommandWifiReset         self.decode_CommandWifiReset(message)
        elif id == Smarter.CommandWifiFirmware      self.decode_CommandWifiFirmware(message)
        elif id == Smarter.CommandBrew              self.decode_CommandBrew(message)
        elif id == Smarter.CommandStrength          self.decode_CommandStrength(message)
        elif id == Smarter.CommandCups              self.decode_CommandCups(message)
        elif id == Smarter.CommandBrewDefault       self.decode_CommandBrewDefault(message)
        elif id == Smarter.CommandGrinder           self.decode_CommandGrinder(message)
        elif id == Smarter.CommandHotplateOn        self.decode_CommandHotplateOn(message)
        elif id == Smarter.CommandHotplateOff       self.decode_CommandHotplateOff(message)
        elif id == Smarter.CommandHeat              self.decode_CommandHeat(message)
        elif id == Smarter.CommandHeatFormula       self.decode_CommandHeatFormula(message)
        elif id == Smarter.CommandHeatDefault       self.decode_CommandHeatDefault(message)
        elif id == Smarter.CommandStoreSettings     self.decode_CommandStoreSettings(message)
        elif id == Smarter.CommandSettings          self.decode_CommandSettings(message)
        elif id == Smarter.CommandStoreBase         self.decode_CommandStoreBase(message)
        elif id == Smarter.CommandBase              self.decode_CommandBase(message)
        elif id == Smarter.CommandCalibrate:        self.decode_CommandCalibrate(message)
        elif id == Smarter.Command20:               self.decode_Command20(message)
        elif id == Smarter.Command22:               self.decode_Command22(message)
        elif id == Smarter.Command23:               self.decode_Command23(message)
        elif id == Smarter.Command30:               self.decode_Command30(message)
        elif id == Smarter.Command32:               self.decode_Command32(message)
        elif id == Smarter.Command40:               self.decode_Command40(message)
        elif id == Smarter.Command41:               self.decode_Command41(message)
        elif id == Smarter.Command43:               self.decode_Command43(message)
        elif id == Smarter.Command69:               self.decode_Command69(message)
        else:
            self.send_invalid()
       

    # MESSAGE SEND PROTOCOL

    def send(self,message):
        try:
            if len(message) > 0 and message[len(message)-1] == Smarter.MessageTail:
                self.socket.send(message)
            elif len(message) > 0:
                self.socket.send(message+Smarter.number_to_raw(Smarter.MessageTail))
            else:
                raise SmarterError("Cannot send an empty message")
                return
        except socket.error, msg:
            raise SmarterError("Could not read message (" + msg[1] + ")")
        else
            self.sendMessage = message