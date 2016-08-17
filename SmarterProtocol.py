# -*- coding: utf8 -*-

import struct

#------------------------------------------------------
# SMARTER PROTOCOL INTERFACE
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
# EXCEPTION CLASS
#------------------------------------------------------


class SmarterError(Exception):
    def __init__(self, arg):
        self.msg = arg


#------------------------------------------------------
# PROTOCOL CLASS
#------------------------------------------------------


class SmarterProtocol:


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
    CommandReset              = 0x10
    CommandStop               = 0x16
    CommandHistory            = 0x28
    CommandDeviceInfo         = 0x64
    CommandUpdate             = 0x6d

    # wifi
    CommandWifiNetwork        = 0x05
    CommandWifiPassword       = 0x07
    CommandWifiConnect        = 0x0c
    CommandWifiScan           = 0x0d
    CommandWifiReset          = 0x0f
    CommandWifiFirmware       = 0x6a

    # coffee
    CommandBrew               = 0x33
    CommandStrength           = 0x35
    CommandCups               = 0x36
    CommandBrewDefault        = 0x37
    CommandGrinder            = 0x3c
    CommandHotplateOn         = 0x3e
    CommandHotplateOff        = 0x4a

    # kettle
    CommandHeat               = 0x15
    CommandHeatFormula        = 0x19
    CommandHeatDefault        = 0x21

    # settings
    CommandStoreSettings      = 0x1f
    CommandSettings           = 0x2e

    # watersensor
    CommandStoreBase          = 0x2a
    CommandBase               = 0x2b
    CommandCalibrate          = 0x2c
    
    # unknown
    Command20                 = 0x20
    Command22                 = 0x22
    Command23                 = 0x23
    Command30                 = 0x30
    Command32                 = 0x32
    Command40                 = 0x40
    Command41                 = 0x41
    Command43                 = 0x43
    Command69                 = 0x69


    ResponseCommandStatus     = 0x03
    ResponseWifiList          = 0x0e
    ResponseHistory           = 0x29
    ResponseBase              = 0x2d
    ResponseSettings          = 0x2f
    ResponseStatus            = 0x14
    ResponseDeviceInfo        = 0x65
    ResponseWifiFirmware      = 0x6b


    # format kettle? coffee? response to command, description
    CommandMessages = {
        CommandDeviceTime       : (True,None,[],"Set device time"),
        CommandWifiNetwork      : (True,None,[],"Set WiFi network SSID"),
        CommandWifiPassword     : (True,None,[],"Set WiFi network password"),
        CommandWifiConnect      : (True,None,[],"Connect to WiFi network"),
        CommandWifiScan         : (True,None,[ResponseWifiList],"Scan for WiFi networks"),
        CommandWifiReset        : (True,None,[],"Reset Wifi networks"),
        CommandReset            : (True,None,[],"Working unknown command (reset?)"),
        CommandHeat             : (True,None,[],"Heat kettle"),
        CommandStop             : (True,None,[],"Stop heating kettle"),
        CommandHeatFormula      : (True,None,[],"Heat kettle using formula mode"),
        CommandStoreSettings    : (True,None,[],"Set Default Values"),
        Command20               : (True,None,[],"Working unknown command (turn on?)"),
        CommandHeatDefault      : (True,None,[],"Working unknown command (turn on?)"),
        Command22               : (True,None,[],"Working unknown command (turn on?)"),
        Command23               : (True,None,[],"Working unknown command (turn on?)"),
        CommandHistory          : (True,None,[ResponseHistory],"Get History Device"),
        CommandStoreBase        : (True,None,[],"Set water sensor base value"),
        CommandBase             : (True,None,[ResponseBase],"Get water sensor base value"),
        CommandCalibrate        : (True,None,[ResponseBase],"Calibrate water sensor"),
        CommandSettings         : (True,None,[ResponseSettings],"Get user settings"),
        Command23               : (True,None,[],"Working unknown command"),
        Command23               : (False,True,[],"Working unknown command (brew)"),
        CommandBrew             : (False,True,[],"Start coffee brewing"),
        CommandStrength         : (False,True,[],"Set strength of the coffee to brew"),
        CommandCups             : (False,True,[],"Set number of cups to brew"),
        CommandBrewDefault      : (False,True,[],"Start coffee brewing using default"),
        CommandGrinder          : (False,True,[],"Toggle grinder"),
        CommandHotplateOn       : (False,True,[],"Turn on hotplate"),
        Command40               : (False,True,[],"Working unknown command (schedule?)"),
        Command41               : (False,True,[],"Working unknown command (schedule?)"),
        Command43               : (False,True,[],"Working unknown command (schedule?)"),
        CommandHotplateOff      : (False,True,[],"Turn off hotplate"),
        CommandDeviceInfo       : (True,True,[ResponseDeviceInfo],"Get identify of device"),
        Command69               : (True,None,[],"Working unknown command"),
        CommandWifiFirmware     : (True,None,[ResponseWifiFirmware],"Get WiFi firmware info"),
        CommandUpdate           : (True,None,[],"Device firmware update")
    }


    # format: kettle?, coffee? (None is unnknown), minimal length (0 = variable), response to command, description
    ResponseMessages = {
        ResponseCommandStatus   : (True,None,3,[],"Command status"),
        ResponseWifiList        : (True,None,0,[CommandWifiScan],"List of WiFi networks"),
        ResponseHistory         : (True,None,0,[CommandHistory],"History Device"),
        ResponseBase            : (True,None,4,[CommandBase,CommandCalibrate],"Water sensor base value"),
        ResponseSettings        : (True,True,9,[CommandSettings],"User settings"),
        ResponseStatus          : (True,True,7,[],"Device status"),
        ResponseDeviceInfo      : (True,True,4,[CommandDeviceInfo],"Identify of device"),
        ResponseWifiFirmware    : (True,None,0,[CommandWifiFirmware],"WiFi firmware info")
    }


    def message_response_length(self,id):
        if self.message_is_response(id):
            return self.ResponseMessages[id][2]
        return 0
    
    def message_description(self,id):
        if self.message_is_response(id):
            return self.ResponseMessages[id][4]
        elif self.message_is_command(id):
            return self.CommandMessages[id][3]
        else:
            return "Unknown Message"


    def message_connection(self,id):
        if self.message_is_response(id):
            return self.ResponseMessages[id][3]
        elif self.message_is_command(id):
            return self.CommandMessages[id][2]
        else:
            return []


    def message_is_known(self,id):
        return self.message_is_response(id) or self.message_is_command(id)


    def message_is_response(self,id):
        return self.ResponseMessages.has_key(id)


    def message_is_command(self,id):
        return self.CommandMessages.has_key(id)


    def message_is_type(self,id):
        if self.message_is_command(id):
            return "Command"
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


    def message_kettle_supported(self,id):
        if self.message_is_command(id):
            return self.message_supported(self.CommandMessages[id][0])
        if self.message_is_response(id):
            return self.message_supported(self.ResponseMessages[id][0])


    def message_coffee_supported(self,id):
        if self.message_is_command(id):
            return self.message_supported(self.CommandMessages[id][1])
        if self.message_is_response(id):
            return self.message_supported(self.ResponseMessages[id][1])


   
    #------------------------------------------------------
    # STATUS INFO
    #------------------------------------------------------


    KettleReady               = 0x00
    KettleBoiling             = 0x01
    KettleKeepWarm            = 0x02
    KettleCycleFinished       = 0x03
    KettleBabyCooling         = 0x04


    StatusKettle = {
        KettleReady             : "Ready",
        KettleBoiling           : "Boiling",
        KettleKeepWarm          : "Keep Warm",
        KettleCycleFinished     : "Cycle Finished",
        KettleBabyCooling       : "Baby Cooling"
    }


    def status_kettle_description(self,status):
        if self.StatusKettle.has_key(status):
            return self.StatusKettle[status]
        else:
            return "Unknown Kettle Status " + self.number_to_code(status)


    def string_kettle_settings(self, temperature,  formula, formulatemperature, keepwarmtime):
        message = "Boil water to " + str(temperature) +  "ºC"
        if formula:
            sep = ""
            if keepwarmtime > 0:
                sep = ","
            else:
                sep = " and"
            message = message + sep + " let it cool down to " + str(formulatemperature) +  "ºC"
        if keepwarmtime > 0:
            message = message + " and keep it warm for " + str(keepwarmtime) + " minutes"
        return message
    def is_status_command(self,status):
        return self.StatusCommand.has_key(status)


    CoffeeDescaling           = 0x51
    CoffeeBoiling             = 0x53


    StatusCoffee = {
        0x04                   : "Filter, ?",
        0x05                   : "Filter, OK to start",
        0x06                   : "Filter, OK to start",
        0x07                   : "Beans, OK to start",
        0x20                   : "Filter, No carafe",
        0x22                   : "Beans, No carafe",
        0x45                   : "Filter, Done",
        0x47                   : "Beans, Done",
        CoffeeBoiling          : "Boiling",
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


    StatusSucces              = 0x00
    StatusBusy                = 0x01
    StatusNoCarafe            = 0x02
    StatusNoWater             = 0x03
    StatusFailed              = 0x04
    StatusNoCarafeUnknown     = 0x05
    StatusNoWaterUnknown      = 0x06
    StatusInvalid             = 0x69


    StatusCommand = {
        StatusSucces           : "Success",
        StatusBusy             : "Busy",
        StatusNoCarafe         : "No Carafe",
        StatusNoWater          : "No Water",
        StatusFailed           : "Failed",
        StatusNoCarafeUnknown  : "No Carafe",  # which one?
        StatusNoWaterUnknown   : "No Water",   # which one?
        StatusInvalid          : "Invalid Command"
    }


    def status_command(self,status):
        if self.is_status_command(status):
            return self.StatusCommand[status]
        else:
            return "Unknown Command Status " + self.number_to_code(status)



    #------------------------------------------------------
    # RAW <-> BASIC TYPE
    #------------------------------------------------------


    def raw_to_number(self,raw):
        try:
            return struct.unpack('B',raw)[0]
        except:
            raise SmarterError("Could not convert raw data to number")


    def number_to_raw(self,number):
        try:
            i = int(number)
        except:
            raise SmarterError("Could not convert number to raw data")
        
        if number < 0 or number > 256:
            raise SmarterError("Could not to convert number " + str(number) + " to raw data, because it is out of range [0..255]")
        try:
            return struct.pack('B',number)
        except:
            raise SmarterError("Could not convert number to raw data: " + str(number))


    def raw_to_code(self,raw):
        return self.number_to_code(self.raw_to_number(raw))


    def code_to_raw(self,code):
        return self.number_to_raw(self.code_to_number(code))


    def code_to_number(self,code):
        try:
            return int(code,16)
        except:
            raise SmarterError("Could not convert code to number")


    def number_to_code(self,number):
        try:
            code = hex(number)[2:4]
        except:
            raise SmarterError("Could not convert number to code: " + str(number))
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
                raise SmarterError("Could not decode message at position: " + str(i))
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
                    print SmarterError("Could not encode code \'" + code + "\' at position: " + str(i*2+1))
 
        elif len(code) % 3 == 2:
            for i in range(0,(len(code) / 3)+1):
                if i > 0:
                    if code[i*3-1] != ' ':
                        raise SmarterError("Expected space character in code  \'" + code + "\' at position: " + str(i*3)+1)
                try:
                    message += self.code_to_raw(code[i*3]+code[i*3+1])
                except:
                    raise SmarterError("Could not encode code \'" + code + "\' at position: " + str(i*3+1))
    
        else:
            raise SmarterError("Missing character in code \'" + code + "\'  at position: " + str(len(code)+1))

        return message
    


    #------------------------------------------------------
    # RAW <-> TYPE
    #------------------------------------------------------


    DeviceKettle              = 0x01
    DeviceCoffee              = 0x00

    
    def is_kettle(self,raw):
        return self.raw_to_number(raw) == self.DeviceKettle


    def is_coffee(self,raw):
        return self.raw_to_number(raw) == self.DeviceCoffee

        
    def raw_to_device(self,raw):
        if self.is_kettle(raw):
            return "iKettle 2.0"
        elif self.is_coffee(raw):
            return "Smarter Coffee"
        else:
            return "Unknown"


    CoffeeWeak                = 0x00
    CoffeeMedium              = 0x01
    CoffeeStrong              = 0x02


    def number_to_strength(self,raw):
        if raw == CoffeeWeak:
            return "weak"
        elif raw == CoffeeMedium:
            return "medium"
        elif raw == CoffeeStrong:
            return "strong"
        else:
            raise SmarterError("Invalid coffee strength [weak, medium, strong]: " + strength)

        self.check_strength(strength)
        return self.StatusCoffeeStrength[strength]


    def strength_to_number(self,strength):
        if strength.strip().lower == "weak":
            return self.CoffeeWeak
        elif strength.strip().lower == "medium":
            return self.CoffeeWeak
        elif strength.strip().lower == "strong":
            raw = self.CoffeeStrong
        else:
            raise SmarterError("Invalid coffee strength [weak, medium, strong]: " + strength)


    def is_on_base(self,raw):
        return self.raw_to_number(raw) != self.MessageOffBase
 
 
    def check_temperature(self,temperature):
        if temperature < 0 or temperature > 100 and not self.is_on_base(self.number_to_raw(temperature)):
            raise SmarterError("Temperature out of range [0..100] ºC: " + str(temperature))
        return temperature


    def raw_to_temperature(self,raw):
        if self.is_on_base(raw):
            return self.check_temperature(self.raw_to_number(raw))
        return 0


    def temperature_to_raw(self,temperature):
        self.check_temperature(temperature)
        return self.number_to_raw(temperature)


    def check_keepwarm(self,timer):
        if timer != 0 and (timer < 5 or timer > 20):
            raise SmarterError("Kettle keep warm timer out of range [0] or [5..20] minutes: " + str(timer))
        return timer


    def check_hotplate(self,timer):
        if timer != 0 and (timer < 5 or timer > 30):
            raise SmarterError("Hotplate timer out of range [0] or [5..30] minutes: " + str(timer))
        return timer


    def raw_to_hotplate(self,raw):
        return self.check_hotplate(self.raw_to_number(raw))


    def raw_to_keepwarm(self,raw):
        return self.check_hotplate(self.raw_to_number(raw))


    def hotplate_to_raw(self,timer):
        return self.number_to_raw(self.check_hotplate(timer))


    def keepwarm_to_raw(self,timer):
        return self.number_to_raw(self.check_keepwarm(timer))


    def raw_to_watersensor(self,raw_low,raw_high):
        return self.raw_to_number(raw_low) + self.raw_to_number(raw_high) * 256


    def watersensor_to_raw(self,watersensor):
        return self.number_to_raw(watersensor % 256) + self.number_to_raw(watersensor / 256)
 
 
    def raw_to_bool(self,raw):
        bool = self.raw_to_number(raw)
        if bool > 1:
            raise SmarterError("Not a boolean value: " + str(int))
        if bool == 1:
            return True
        return False
 
 
    def bool_to_raw(self,boolean):
        return self.number_to_raw(boolean)


    def check_cups(self,cups):
        if cups < 1 or cups > 12:
            raise SmarterError("Unknown coffee cups [1..12]: " + str(cups))
        return cups


    def raw_to_cups(self,raw):
        return self.check_cups(self.raw_to_number(raw))


    def cups_to_raw(self,cups):
        return self.number_to_raw(self.check_cups(cups))
    

    def string_cups(self,cups):
        if cups == 1:
            return "1 cup"
        else:
            return str(self.cups) + " cups"



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
            raise SmarterError("Unknown Wifi signal (dBm) strength: " + str(dBm))

Smarter = SmarterProtocol()
