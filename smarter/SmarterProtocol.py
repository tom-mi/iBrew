# -*- coding: utf8 -*-

import traceback
import struct

#------------------------------------------------------
# SMARTER PROTOCOL INTERFACE
#
# Python protocol interface to iKettle 2.0 & SmarterCoffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Out of order! (rev 7)
#------------------------------------------------------



#------------------------------------------------------
# EXCEPTION CLASS
#------------------------------------------------------


KettleNoMachineHeat             = 30
KettleNoMachineOff              = 31
KettleNoMachineSettings         = 32
KettleNoMachineStoreSettings    = 33
KettleNoMachineHistory          = 34
CoffeeNoMachineStrength         = 50
CoffeeNoMachineGrinder          = 51
CoffeeNoMachineCups             = 52
CoffeeNoMachineHotplateOn       = 53
CoffeeNoMachineHotplateOff      = 54
CoffeeNoMachinesBrew            = 55
CoffeeNoMachineOff              = 56
CoffeeNoMachineSettings         = 57
CoffeeNoMachineStoreSettings    = 58
CoffeeNoMachineHistory          = 59
CoffeeNoMachineSingleCupMode    = 60
CoffeeNoMachineCarafe           = 61
KettleFailedStoreSettings       = 70
CoffeeFailedStoreSettings       = 90

ConvertRawNumber                = 110
ConvertNumberRaw                = 111
ConvertCodeNumber               = 112
ConvertNumberCode               = 113

WebServerListen                 = 120
WebServerStartFailed            = 121

WebServerStopMonitor            = 122
WebServerStopMonitorWeb         = 123
WebServerStopWeb                = 124

SmarterClientFailedStop         = 125
SmarterClientFailedStopThread   = 126


class SmarterError(Exception):

    def __init__(self, err, msg):
        #print(traceback.format_exc())
        #print str(msg)
        self.msg = msg
        self.err = err


class SmarterErrorOld(Exception):
    def __init__(self, msg):
        #print str(msg)
        #print(traceback.format_exc())
        self.msg = msg


#------------------------------------------------------
# PROTOCOL CLASS
#------------------------------------------------------


class SmarterProtocol:

    DirectHost = "192.168.4.1"
    Port       = 2081
    Fahrenheid = False

    #------------------------------------------------------
    # MESSAGES CONSTANTS
    #------------------------------------------------------

    MessageTail               = 0x7e
    MessagePayloadTail        = 0x7d
    MessageOffBase            = 0x7f



    #------------------------------------------------------
    # MESSAGE INFO
    #------------------------------------------------------


    # device
    CommandDeviceTime         = 0x02
    CommandResetSettings      = 0x10
    CommandDeviceInfo         = 0x64
    CommandUpdate             = 0x6d
    Command69                 = 0x69

    # wifi
    CommandWifiNetwork        = 0x05
    CommandWifiPassword       = 0x07
    CommandWifiJoin           = 0x0c
    CommandWifiScan           = 0x0d
    CommandWifiLeave          = 0x0f
    CommandWifiFirmware       = 0x6a

    # coffee
    CommandBrew               = 0x33
    CommandCoffeeStop         = 0x34
    CommandStrength           = 0x35
    CommandCups               = 0x36
    CommandBrewDefault        = 0x37
    CommandCoffeeSettings     = 0x48
    CommandCoffeeStoreSettings = 0x38
    CommandGrinder            = 0x3c
    CommandHotplateOn         = 0x3e
    CommandCoffeeHistory      = 0x46
    CommandHotplateOff        = 0x4a
    CommandCarafe             = 0x4c
    CommandSetCarafe          = 0x4b
    CommandSingleCupMode      = 0x4f
    CommandSetSingleCupMode   = 0x4e
    CommandStoreTimer         = 0x40
    CommandTimers             = 0x41
    CommandDisableTimer       = 0x43
 
    # kettle
    CommandHeat               = 0x15
    CommandKettleStop         = 0x16
    CommandHeatFormula        = 0x19
    CommandHeatDefault        = 0x21
    Command20                 = 0x20
    Command22                 = 0x22
    Command23                 = 0x23
    Command30                 = 0x30
    CommandKettleStoreSettings = 0x1f
    CommandKettleHistory      = 0x28
    CommandKettleSettings     = 0x2e
    CommandStoreBase          = 0x2a
    CommandBase               = 0x2b
    CommandCalibrate          = 0x2c
    


    # device
    ResponseCommandStatus     = 0x03
    ResponseWirelessNetworks  = 0x0e
    ResponseKettleHistory     = 0x29
    ResponseDeviceInfo        = 0x65
    ResponseWifiFirmware      = 0x6b

    # coffee
    ResponseCoffeeSettings    = 0x49
    ResponseCoffeeStatus      = 0x32
    ResponseTimers            = 0x42
    ResponseCoffeeHistory     = 0x47
    ResponseCarafe            = 0x4d
    ResponseSingleCupMode     = 0x50
    
    # kettle
    ResponseKettleStatus      = 0x14
    ResponseBase              = 0x2d
    ResponseKettleSettings    = 0x2f


    # format kettle? coffee? response to command, description
    CommandMessages = {
        CommandDeviceTime       : (True,True,[ResponseCommandStatus],"Set device time"),
        CommandWifiNetwork      : (True,True,[ResponseCommandStatus],"Set wireless network name"),
        CommandWifiPassword     : (True,True,[ResponseCommandStatus],"Set wireless network password"),
        CommandWifiJoin         : (True,True,[],"Join wireless network"),
        CommandWifiScan         : (True,True,[ResponseWirelessNetworks],"Scan for wireless networks"),
        CommandWifiLeave        : (True,True,[],"Leave wireless network"),
        CommandResetSettings    : (True,True,[ResponseCommandStatus],"Reset default user settings"),
        CommandHeat             : (True,False,[ResponseCommandStatus],"Heat kettle"),
        CommandKettleStop       : (True,False,[ResponseCommandStatus],"Stop heating kettle"),
        CommandHeatFormula      : (True,False,[ResponseCommandStatus],"Heat kettle using formula mode"),
        CommandKettleStoreSettings : (True,False,[ResponseCommandStatus],"Set kettle default user settings"),
        Command20               : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        CommandHeatDefault      : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        Command22               : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        Command23               : (True,False,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        CommandKettleHistory    : (True,False,[ResponseKettleHistory],"Get kettle history"),
        CommandStoreBase        : (True,False,[],"Set water sensor base value"),
        CommandBase             : (True,False,[ResponseBase,ResponseCommandStatus],"Get water sensor base value"),
        CommandCalibrate        : (True,False,[ResponseBase,ResponseCommandStatus],"Calibrate water sensor"),
        CommandKettleSettings   : (True,False,[ResponseKettleSettings],"Get default kettle user settings"),
        Command30               : (True,False,[ResponseCommandStatus],"Working unknown command"),
        CommandBrew             : (False,True,[ResponseCommandStatus],"Start coffee brewing"),
        CommandCoffeeStop       : (False,True,[ResponseCommandStatus],"Stop coffee brewing"),
        CommandStrength         : (False,True,[ResponseCommandStatus],"Set strength of the coffee to brew"),
        CommandCups             : (False,True,[ResponseCommandStatus],"Set number of cups to brew"),
        CommandBrewDefault      : (False,True,[ResponseCommandStatus],"Start coffee brewing using machine settings"),
        CommandCoffeeStoreSettings : (False,True,[],"Set coffee machine default user settings"),
        CommandGrinder          : (False,True,[ResponseCommandStatus],"Toggle grinder"),
        CommandHotplateOn       : (False,True,[ResponseCommandStatus],"Turn on hotplate"),
        CommandCarafe           : (False,True,[ResponseCoffeeStatus,ResponseCommandStatus],"Get coffee carafe required"),
        CommandSingleCupMode    : (False,True,[ResponseSingleCupMode,ResponseCommandStatus],"Get single coffee cup mode"),
        CommandStoreTimer       : (False,True,[ResponseCommandStatus],"Store timer"),
        CommandTimers           : (False,True,[ResponseTimers,ResponseCommandStatus],"Get timers"),
        CommandDisableTimer     : (False,True,[ResponseCommandStatus],"Timer event handled"),
        CommandSetCarafe        : (False,True,[ResponseCommandStatus],"Set coffee carafe required"),
        CommandSetSingleCupMode : (False,True,[ResponseCommandStatus],"Set single coffee cup mode"),
        CommandCoffeeSettings   : (False,True,[ResponseCoffeeSettings,ResponseCommandStatus],"Get default coffee machine user settings"),
        CommandCoffeeHistory    : (False,True,[ResponseCoffeeHistory],"Get coffee machine history"),
        CommandHotplateOff      : (False,True,[ResponseCommandStatus],"Turn off hotplate"),
        CommandDeviceInfo       : (True,True,[ResponseDeviceInfo],"Get device info"),
        Command69               : (True,True,[ResponseCommandStatus],"Working unknown command"),
        CommandWifiFirmware     : (True,True,[ResponseWifiFirmware],"Get wifi firmware info"),
        CommandUpdate           : (True,True,[],"Device firmware update")
    }



    def __con(self,coffee,kettle):
        if coffee and kettle:
            return [self.DeviceKettle,self.DeviceCoffee]
        if coffee and not kettle:
            return [self.DeviceCoffee]
        if not coffee and kettle:
            return [self.DeviceKettle]
        else:
            return []


    def CommandToJSON(self):
        json = dict()
        for command in self.CommandMessages:
            message = self.CommandMessages[command]
            json[command] = { 'device' : self.__con(message[0],message[1]), 'description' : self.message_description(command) }
        return json

    def ResponseToJSON(self):
        json = dict()
        for response in self.ResponseMessages:
            if self.message_is_response(response):
                message = self.ResponseMessages[response]
                json[response] = { 'device' : self.__con(message[0],message[1]), 'description' : self.message_description(response) }
        return json


    def StatusToJSON(self):
        return { self.ResponseKettleStatus : { 'device' : [Smarter.DeviceKettle], 'description' : self.message_description(self.ResponseKettleStatus) },
                 self.ResponseCoffeeStatus : { 'device' : [Smarter.DeviceCoffee], 'description' : self.message_description(self.ResponseCoffeeStatus) }
                }


    # format: kettle?, coffee? (None is unnknown), minimal length (0 = variable), response to command, description
    ResponseMessages = {
        #incomplete? ... chech the first one...
        ResponseCommandStatus   : (True,True,3,[CommandDeviceTime,CommandWifiNetwork,CommandWifiPassword,CommandResetSettings,CommandHeat,CommandKettleStop,CommandHeatFormula,CommandKettleStoreSettings,Command20,CommandHeatDefault,Command22,Command23,CommandBase,CommandCalibrate,Command69,CommandStoreTimer,CommandTimers,CommandDisableTimer,Command30,CommandSetCarafe,CommandSetSingleCupMode,CommandStrength,CommandCups,CommandGrinder,CommandHotplateOn,CommandSingleCupMode,CommandCarafe,CommandHotplateOff,CommandCoffeeSettings,CommandBrew,CommandCoffeeStop,CommandBrewDefault],"Command status"),
        ResponseWirelessNetworks: (True,True,0,[CommandWifiScan],"Wireless networks list"),
        ResponseKettleHistory   : (True,False,0,[CommandKettleHistory],"Kettle history"),
        ResponseCoffeeHistory   : (False,True,0,[CommandCoffeeHistory],"Coffee machine history"),
        ResponseBase            : (True,False,4,[CommandBase,CommandCalibrate],"Water sensor base value"),
        ResponseKettleSettings  : (True,False,9,[CommandKettleSettings],"Default kettle user settings"),
        ResponseKettleStatus    : (True,False,7,[],"Kettle status"),
        ResponseDeviceInfo      : (True,True,4,[CommandDeviceInfo],"Device info"),
        ResponseWifiFirmware    : (True,True,0,[CommandWifiFirmware],"Wifi firmware info"),
        ResponseCarafe          : (False,True,3,[CommandCarafe],"Carafe required"),
        ResponseCoffeeStatus    : (False,True,0,[],"Coffee machine status"),
        ResponseCoffeeSettings  : (False,True,6,[CommandCoffeeSettings],"Default coffee machine user settings"),
        ResponseSingleCupMode   : (False,True,3,[CommandSingleCupMode],"Single coffee cup mode"),
        ResponseTimers          : (False,True,0,[CommandTimers],"Stored timers")

    }


    def message_response_length(self,id):
        if self.message_is_response(id):
            return self.ResponseMessages[id][2]
        return 0
    
    
    def message_description(self,id):
        if self.message_is_response(id) or self.message_is_status(id):
            return self.ResponseMessages[id][4]
        elif self.message_is_command(id):
            return self.CommandMessages[id][3]
        else:
            return "Unknown message"


    def message_connection_type(self,id):
        if self.message_is_response(id):
            return "Command"
        elif self.message_is_command(id):
            return "Response"
        else:
            return ""

    def message_connection(self,id):
        if self.message_is_response(id):
            x = self.ResponseMessages[id][3]
            if x: x.sort()
            return x
        elif self.message_is_command(id):
            x = self.CommandMessages[id][2]
            if x: x.sort()
            return x
        else:
            return []


    def message_is_known(self,id):
        return self.message_is_response(id) or self.message_is_command(id) or self.message_is_status(id)


    def message_is_response(self,id):
        if id != self.ResponseKettleStatus and id != self.ResponseCoffeeStatus:
            return self.ResponseMessages.has_key(id)
        return False


    def message_is_status(self,id):
        if id == self.ResponseKettleStatus or id == self.ResponseCoffeeStatus:
            return True
        return False


    def message_is_command(self,id):
        return self.CommandMessages.has_key(id)


    def message_is_type(self,id):
        if self.message_is_command(id):
            return "Command"
        elif id == self.ResponseKettleStatus or id == self.ResponseCoffeeStatus:
            return "Status"
        else:
            return "Response"

    # internal use here only
    def message_supported(self,state):
        if state is None:
            return "?"
        if state:
            return "✓"
        else:
            return "✕"


    def message_kettle(self,id):
        if self.message_is_command(id):
            return self.CommandMessages[id][0]
        if self.message_is_response(id) or self.message_is_status(id):
            return self.ResponseMessages[id][0]


    def message_kettle_supported(self,id):
        return self.message_supported(self.message_kettle(id))


    def message_coffee_supported(self,id):
        return self.message_supported(self.message_coffee(id))


    def message_coffee(self,id):
        if self.message_is_command(id):
            return self.CommandMessages[id][1]
        if self.message_is_response(id) or self.message_is_status(id):
            return self.ResponseMessages[id][1]


    #------------------------------------------------------
    # RAW <-> BASIC TYPE
    #------------------------------------------------------

    def raw_to_number(self,raw):
        try:
            return struct.unpack('B',raw)[0]
        except:
            raise SmarterError(ConvertRawNumber,"Could not convert raw data to number")

    def number_to_raw(self,number):
        try:
            i = int(number)
        except:
            raise SmarterError(ConvertNumberRaw,"Could not convert number to raw data")
        
        if number < 0 or number > 256:
            raise SmarterError(ConvertNumberRaw,"Could not to convert number " + str(number) + " to raw data, because it is out of range [0..255]")
        try:
            return struct.pack('B',number)
        except:
            raise SmarterError(ConvertNumberRaw,"Could not convert number to raw data: " + str(number))


    def raw_to_code(self,raw):
        return self.number_to_code(self.raw_to_number(raw))


    def code_to_raw(self,code):
        return self.number_to_raw(self.code_to_number(code))


    def code_to_number(self,code):
        try:
            return int(code,16)
        except:
            raise SmarterError(ConvertCodeNumber,"Could not convert code to number: " + code )


    def number_to_code(self,number):
        try:
            code = hex(number)[2:4]
        except:
            raise SmarterError(ConvertNumberCode,"Could not convert number to code: " + str(number))
        if number < 16:
            return '0' + code
        return code


    def text_to_raw(self,text):
        return text
        # FIX ERROR CHECKING + CODE
        return 
        for i in range(0,len(text)):
            raw =+ number_to_raw(text[i])
        return raw


    def raw_to_text(self,raw):
        # FIX ERROR CHECKING + CODE
        for i in range(0,len(raw)):
            raw =+ raw_to_number(raw_[i])
        return raw


    #------------------------------------------------------
    # RAW HEX STRING <-> RAW
    #------------------------------------------------------

    # Convert raw data to hex string without 0x seperated by spaces
    def message_to_codes(self,message,space = False):
        raw = ""
        for i in range(0,len(message)):
            try:
                raw += self.raw_to_code(message[i])
            except:
                raise SmarterErrorOld("Could not decode message at position: " + str(i))
            if space and i != len(message)-1:
                raw += " "
        return raw


    # Convert hex string without 0x input maybe seperated by spaces or not
    def codes_to_message(self,string):
        message = ""
        code = string.strip()
        
        if len(code) <= 2:
            return self.code_to_raw(code)
        
        if len(code) % 2 == 0 and code[2] != " ":
            for i in range(0,len(code) / 2):
                try:
                    message += self.code_to_raw(code[i*2]+code[i*2+1])
                except:
                    raise SmarterErrorOld("Could not encode code \'" + code + "\' at position: " + str(i*2+1))
 
        elif len(code) % 3 == 2:
            for i in range(0,(len(code) / 3)+1):
                if i > 0:
                    if code[i*3-1] != ' ':
                        raise SmarterErrorOld("Expected space character in code  \'" + code + "\' at position: " + str(i*3)+1)
                try:
                    message += self.code_to_raw(code[i*3]+code[i*3+1])
                except:
                    raise SmarterErrorOld("Could not encode code \'" + code + "\' at position: " + str(i*3+1))
    
        else:
            raise SmarterErrorOld("Missing character in code \'" + code + "\'  at position: " + str(len(code)+1))

        return message
    

    #------------------------------------------------------
    # RAW <-> TYPE
    #------------------------------------------------------


    #------------------------------------------------------
    # DEVICE & FIRMWARE ARGUMENT WRAPPER
    #------------------------------------------------------

    DeviceKettle              = 0x01
    DeviceCoffee              = 0x02


    KettleFirmwareVerified    = [18,19]
    CoffeeFirmwareVerified    = [20,22]


    def is_kettle(self,device):
        return device == self.DeviceKettle


    def is_kettle_verified(self,firmware):
        return firmware in self.KettleFirmwareVerified
    
    
    def is_coffee_verified(self,firmware):
        return firmware in self.CoffeeFirmwareVerified
    
    
    def is_coffee(self,device):
        return device == self.DeviceCoffee


    def firmware_verified(self,device,firmware):
        if (device == self.DeviceCoffee and self.is_coffee_verified(firmware)) or (device == self.DeviceKettle and self.is_kettle_verified(firmware)):
            return "iBrew certified firmware"
        return "Unsupported firmware"


    def device_to_string(self,device):
        if self.is_kettle(device):
            return "iKettle 2.0"
        elif self.is_coffee(device):
            return "SmarterCoffee"
        else:
            return "Unknown"


    def device_info(self,device,firmware):
        return self.device_to_string(device)  + " (" + self.firmware_verified(device,firmware) + " v" + str(firmware) + ")"


    #------------------------------------------------------
    # STRENGTH ARGUMENT WRAPPER
    #------------------------------------------------------

    CoffeeWeak                = 0x00
    CoffeeMedium              = 0x01
    CoffeeStrong              = 0x02
    
    CoffeeGramsStrong         = 200
    CoffeeGramsMedium         = 150 #???
    CoffeeGramsWeak           = 100 #???


    def check_strength(self,strength):
        if strength == self.CoffeeMedium or strength == self.CoffeeStrong or strength == self.CoffeeWeak:
            return strength
        else:
            raise SmarterErrorOld("Invalid coffee strength [weak, medium, strong]: " + strength)


    def strength_to_raw(self,strength):
        return self.number_to_raw(self.check_strength(strength))


    def raw_to_strength(self,raw):
        return self.check_strength(self.raw_to_number(raw))
    
    
    def strength_to_string(self,number):
        if self.CoffeeWeak == number:
            return "weak"
        elif self.CoffeeMedium == number:
            return "normal"
        elif self.CoffeeStrong == number:
            return "strong"
        return self.StatusCoffeeStrength[self.check_strength(strength)]


    def string_to_strength(self,strength):
        if strength.strip().lower() == "weak":        
            return self.CoffeeWeak
        elif strength.strip().lower() == "medium":
            return self.CoffeeMedium
        elif strength.strip().lower() == "strong":
            return self.CoffeeStrong
        else:
            raise SmarterErrorOld("Invalid coffee strength [weak, medium, strong]: " + strength)


    #------------------------------------------------------
    # TEMPERATURE ARGUMENT WRAPPER
    #------------------------------------------------------

    def is_on_base(self,raw):
        return self.raw_to_number(raw) != self.MessageOffBase
 
 
    def string_base_on_off(self,onbase):
        if onbase:
            return "On"
        else:
           return "Off"
           
    def celsius_to_fahrenheid(self,temperature):
        return ((temperature * 9) / 5) + 32
    
    
    def fahrenheid_to_celsius(self,temperature):
        return ((temperature - 32) * 5) / 9
    
    
    def check_temperature_celsius(self,temperature):
        # if fahrenheid then converto...
        # if self.Fahrenheid
        if temperature < 0 or temperature > 100 and not self.is_on_base(self.number_to_raw(temperature)):
            if self.Fahrenheid:
                raise SmarterErrorOld("Temperature out of range ["+self.celsius_to_fahrenheid(0)+".."+self.celsius_to_fahrenheid(100)+"] ºK: " + str(temperature))
            else:
                raise SmarterErrorOld("Temperature out of range [0..100] ºC: " + str(temperature))
        return temperature
    
    
    def check_temperature(self,temperature):
        if self.Fahrenheid:
            return self.fahrenheid_to_celsius(temperature)
        else:
            return temperature


    def raw_to_temperature(self,raw):
        if self.is_on_base(raw):
            return self.check_temperature_celsius(self.raw_to_number(raw))
        return 0


    def temperature_to_raw(self,temperature):
        return self.number_to_raw(self.check_temperature_celsius(temperature))


    def temperature_to_string(self,temperature):
        if self.Fahrenheid:
            return str(temperature)+" ºF"
        else:
            return str(temperature)+" ºC"


    def temperature_symbol_to_string(self):
        if self.Fahrenheid:
            return "ºF"
        else:
            return "ºC"

    def temperature_metric_to_string(self):
        if self.Fahrenheid:
            return "fahrenheid"
        else:
            return "celsius"

    def string_to_temperature(self,temperature):
        try:
            if self.Fahrenheid:
                return self.fahrenheid_to_celsius(int(temperature))
            else:
                return int(temperature)
        except:
            raise SmarterErrorOld("Temperature is not a number: " + temperature)


    #------------------------------------------------------
    # HOTPLATE KEEPWARM ARGUMENT WRAPPER
    #------------------------------------------------------

    def string_to_hotplate(self,string):
        try:
            return int(string)
        except:
            raise SmarterErrorOld("Hotplate timer is not a number: " + string)

    def check_hotplate(self,timer):
        if timer != 0 and (timer < 5 or timer > 40):
            raise SmarterErrorOld("Hotplate timer out of range [0] or [5..40] minutes: " + str(timer))
        return timer


    def raw_to_hotplate(self,raw):
        return self.check_hotplate(self.raw_to_number(raw))


    def hotplate_to_raw(self,timer):
        return self.number_to_raw(self.check_hotplate(timer))


    #------------------------------------------------------
    # KEEPWARM ARGUMENT WRAPPER
    #------------------------------------------------------

    def string_to_keepwarm(self,string):
        try:
            return int(string)
        except:
            raise SmarterErrorOld("Keepwarm timer is not a number: " + string)


    def check_keepwarm(self,timer):
        if timer != 0 and (timer < 5 or timer > 20):
            raise SmarterErrorOld("Kettle keep warm timer out of range [0] or [5..20] minutes: " + str(timer))
        return timer


    def raw_to_keepwarm(self,raw):
        return self.check_hotplate(self.raw_to_number(raw))


    def keepwarm_to_raw(self,timer):
        return self.number_to_raw(self.check_keepwarm(timer))


    #------------------------------------------------------
    # WATERSENSOR ARGUMENT WRAPPER
    #------------------------------------------------------

    def check_watersensor(self, watersensor):
        if watersensor < 0 or watersensor > 4095:
            raise SmarterErrorOld("Watersensor out of range [0..4095]")
        return watersensor
        
    def raw_to_watersensor(self,raw_low,raw_high):
        return self.check_watersensor(self.raw_to_number(raw_low) * 256 + self.raw_to_number(raw_high))


    def watersensor_to_raw(self,watersensor):
        return self.number_to_raw(watersensor / 256) + self.number_to_raw(watersensor % 256)

    def string_to_watersensor(self,string):
        try:
            watersensor = int(string)
        except:
            raise SmarterErrorOld("Not a watersensor value")
        return self.check_watersensor(watersensor)
 
 
    #------------------------------------------------------
    # BOOLEAN ARGUMENT WRAPPER
    #------------------------------------------------------

    def raw_to_bool(self,raw):
        bool = self.raw_to_number(raw)
        if bool > 1:
            raise SmarterErrorOld("Not a boolean value: " + str(int))
        if bool == 1:
            return True
        return False
 
 
    def bool_to_raw(self,boolean):
        return self.number_to_raw(boolean)


    def string_to_bool(self,boolean):
        if boolean.lower() == "on" or boolean.lower() == "true" or boolean.lower() == "1":
            return True
        if boolean.lower() == "off" or boolean.lower() == "false" or boolean.lower() == "0":
            return False
        else:
            raise SmarterErrorOld("Unknown boolean [true/1/on/false/0/off]: " + str(boolean))

    #------------------------------------------------------
    # CUPS ARGUMENT WRAPPER
    #------------------------------------------------------

    def check_cups(self,cups_raw):
        cups = cups_raw % 16
        if cups < 1 or cups > 12:
            raise SmarterErrorOld("Unknown coffee cups [1..12]: " + str(cups))
        return cups


    def raw_to_cups_bit(self,cups_raw):
        return self.raw_to_number(cups_raw) / 16


    def raw_to_cups(self,raw):
        return self.check_cups(self.raw_to_number(raw))


    def cups_to_raw(self,cups):
        return self.number_to_raw(self.check_cups(cups))
    

    def string_to_cups(self,string):
        try:
            cups = int(string)
        except:
            raise SmarterErrorOld("Unknown coffee cups [1..12]: " + string)
        return self.check_cups(cups)


    def cups_to_string(self,cups):
        if cups == 1:
            return "a cup"
        else:
            return str(cups) + " cups"


    #------------------------------------------------------
    # WATERLEVEL ARGUMENT WRAPPER
    #------------------------------------------------------

    WaterLevel = {
        0x00 : "empty",
        0x01 : "low",
        0x02 : "half",
        0x03 : "full",
    }

    def waterlevel(self,level):
        if self.WaterLevel.has_key(level):
            return self.WaterLevel[level]
        else:
            return "unknown water level [0..3]: " + self.number_to_code(level)


    def check_waterlevel(self,waterlevel_raw):
        water = waterlevel_raw % 16
        if water < 0 or water > 3:
            raise SmarterErrorOld("Unknown waterlevel [0..3]: " + str(water))
        return water


    def raw_to_waterlevel(self,raw):
        return self.check_waterlevel(self.raw_to_number(raw))


    def raw_to_waterlevel_bit(self,raw):
        return self.raw_to_number(raw) / 16

   
    #------------------------------------------------------
    # COMMAND STATUS INFO WRAPPER
    #------------------------------------------------------

    StatusSucces              = 0x00
    StatusBusy                = 0x01
    StatusNoCarafe            = 0x02
    StatusNoWater             = 0x03
    StatusFailed              = 0x04
    StatusNoCarafeUnknown     = 0x05
    StatusNoWaterUnknown      = 0x06
    StatusNoWaterAborted      = 0x07 # i got low water for 3 cups... it gave this...
    StatusUnknown0d           = 0x0d
    StatusInvalid             = 0x69


    StatusCommand = {
        StatusSucces           : "success",
        StatusBusy             : "busy",
        StatusNoCarafe         : "no carafe",
        StatusNoWater          : "no water",
        StatusFailed           : "failed",
        StatusNoCarafeUnknown  : "no carafe",  # which one?
        StatusNoWaterUnknown   : "no water",   # which one?
        StatusNoWaterAborted   : "low water could not finish",
        StatusUnknown0d        : "response to 40 01",
        StatusInvalid          : "invalid command"
    }


    def status_command(self,status):
        if self.is_status_command(status):
            return self.StatusCommand[status]
        else:
            return "Unknown Command Status " + self.number_to_code(status)


    #------------------------------------------------------
    # KETTLE STATUS INFO WRAPPER
    #------------------------------------------------------

    KettleReady               = 0x00
    KettleHeating             = 0x01
    KettleKeepWarm            = 0x02
    KettleCycleFinished       = 0x03
    KettleBabyCooling         = 0x04


    StatusKettle = {
        KettleReady             : "ready",
        KettleHeating           : "heating",
        KettleKeepWarm          : "keep warm",
        KettleCycleFinished     : "cycle finished",
        KettleBabyCooling       : "baby cooling"
    }


    def status_kettle_description(self,status):
        if self.StatusKettle.has_key(status):
            return self.StatusKettle[status]
        else:
            return "Unknown Kettle Status " + self.number_to_code(status)


    def string_kettle_settings(self, temperature,  formula, formulatemperature, keepwarmtime):
        message = "Heat water to " + str(temperature) +  "ºC"
        if formula:
            sep = ""
            if keepwarmtime > 0:
                sep = ","
            else:
                sep = " and"
            message = message + sep + " let it cool down to " + Smarter.temperature_to_string(formulatemperature)
        if keepwarmtime > 0:
            message = message + " and keep it warm for " + str(keepwarmtime) + " minutes"
        return message

    def is_status_command(self,status):
        return self.StatusCommand.has_key(status)


    #------------------------------------------------------
    # COFFEE STATUS INFO WRAPPER
    #------------------------------------------------------

    CoffeeDescaling           = 0x51
    CoffeeHeating             = 0x53


    StatusCoffee = {
        0x04                   : "Filter, ?",
        0x05                   : "Filter, OK to start",
        0x06                   : "Filter, OK to start",
        0x07                   : "Beans, OK to start",
        0x20                   : "Filter, No carafe",
        0x22                   : "Beans, No carafe",
        0x45                   : "Filter, Done",
        0x47                   : "Beans, Done",
        CoffeeHeating          : "Heating water",
        0x60                   : "Filter, No carafe, Hotplate On",
        0x61                   : "Filter, Hotplate On",
        0x62                   : "Beans, No carafe, Hotplate On",
        0x63                   : "Beans, Hotplate On",
        CoffeeDescaling        : "Descaling in progress"
    }


    def status_coffee_description(self,status):
        if self.StatusCoffee.has_key(status):
            return self.StatusCoffee[status]
        else:
            return "Unknown Coffee Status " + self.number_to_code(status)


    def grind_to_string(self,grind):
        s = "filter"
        if grind:
            s = "beans"
        return s


    def string_to_grind(self,grind):
        s = grind.lower()
        if s == "beans":
            return True
        elif s == "filter":
            return False
        else:
           raise SmarterErrorOld("Unknown grind [beans/filter] " + grind)
           

    def string_coffee_settings(self, cups, strength, grind, hotplate):
        s = ""
        if hotplate >= 5 and hotplate <= 40:
            s = " and keep hotplate warm for " + str(hotplate) + " minutes"
        t = " " + self.grind_to_string(grind) + " coffee"
        if grind:
            t = self.strength_to_string(strength) + t
        return "Brew " + self.cups_to_string(cups) + " of " + t + s


    def string_coffee_status(self,ready,working,heating,hotPlateOn,carafe,grinderOn):
        s = ""
        if working:
            s += "working "
        if heating:
            s += "heating "
        if hotPlateOn:
            s += "hotplate warming "
        if grinderOn:
            s += "grinding "
        if ready:
            s += "ready "
        if carafe:
            s+= "carafe on base"
        else:
            s+= "no carafe"
        return s


    #------------------------------------------------------
    # TYPE -> TYPE
    #------------------------------------------------------

    def watersensor_to_level(self,watersensor):
        # Fix Check value's
        #   calibrate nokettlebase:       1120     measure: kettle off: 2010 kettle empty: 2070 kettle full: 2140  (div 890 950 1020)
        #   calibrate emptykettlebase:    1070     measure: kettle off: 1975 kettle empty: 2020 kettle full: 2085  (div 905 950 1015)
        #   calibrate fullkettlebase:     1010     measure: kettle off: 1875 kettle empty: 1950 kettle full: 2015  (div 865 940 1005)
        # div = measure - base
        # need temperature in calclation...
        #   1.8l
        # is this accurate??? nope...
        # sometimes if placed on base it gives wrong levels
        if isKettle:
            waterlevel = (1.800/72) * (watersensor - self.watersensorBase - 1000)
            if waterlevel < 0:
                return 0.0
            if waterlevel > 2:
                return 1.8
            else:
                return waterlevel
        elif self.isCoffee:
            return 0


    def dbm_to_quality(self,dBm):
        # takes as input a dBm string (e.g. "-23")
        # quality = 2 * (dBm + 100)  where dBm: [-100 to -50]
        # dBm = (quality / 2) - 100  where quality: [0 to 100]
        try:
            if dBm <= -100:
                return 0
            elif dBm >= -50:
                return 100
            else:
                return 2 * (dBm + 100)
        except:
            raise SmarterErrorOld("Unknown Wifi signal (dBm) strength: " + str(dBm))


    def bytes_to_human(self,size_bytes):
        
        # format a size in bytes into a 'human' file size, e.g. bytes, KB, MB, GB, TB, PB
        # Note that bytes/KB will be reported in whole numbers but MB and above will have greater precision
        # e.g. 1 byte, 43 bytes, 443 KB, 4.3 MB, 4.43 GB, etc
        
        if size_bytes == 1:
            # because I really hate unnecessary plurals
            return "1 byte"

        suffixes_table = [('bytes',0),('KB',0),('MB',1),('GB',2),('TB',2), ('PB',2)]

        num = float(size_bytes)
        for suffix, precision in suffixes_table:
            if num < 1024.0:
                break
            num /= 1024.0

        if precision == 0:
            formatted_size = "%d" % num
        else:
            formatted_size = str(round(num, ndigits=precision))

        return "%s %s" % (formatted_size, suffix)



Smarter = SmarterProtocol()