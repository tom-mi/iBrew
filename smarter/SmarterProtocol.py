# -*- coding: utf8 -*-

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
# Kettle Rattle (rev 6)
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
    CommandSingleCupMode      = 0x4f

    # kettle
    CommandHeat               = 0x15
    CommandKettleStop         = 0x16
    CommandHeatFormula        = 0x19
    CommandHeatDefault        = 0x21
    # settings
    CommandKettleStoreSettings = 0x1f
    CommandKettleHistory      = 0x28
    CommandKettleSettings     = 0x2e
    # watersensor
    CommandStoreBase          = 0x2a
    CommandBase               = 0x2b
    CommandCalibrate          = 0x2c
    
    # unknown
    # kettle
    Command20                 = 0x20
    Command22                 = 0x22
    Command23                 = 0x23
    Command30                 = 0x30
    # coffee
    Command40                 = 0x40
    Command41                 = 0x41
    Command43                 = 0x43
    Command4b                 = 0x4b
    Command4e                 = 0x4e
    
    # ?
    Command69                 = 0x69


    # device
    ResponseCommandStatus     = 0x03
    ResponseWirelessNetworks  = 0x0e
    ResponseKettleHistory     = 0x29
    ResponseDeviceInfo        = 0x65
    ResponseWifiFirmware      = 0x6b

    # coffee
    ResponseCoffeeSettings    = 0x49
    ResponseCoffeeStatus      = 0x32
    ResponseCoffeeHistory     = 0x47
    ResponseCarafe            = 0x4d
    ResponseSingleCupMode     = 0x50
    
    # kettle
    ResponseKettleStatus      = 0x14
    ResponseBase              = 0x2d
    ResponseKettleSettings    = 0x2f


    # format kettle? coffee? response to command, description
    CommandMessages = {
        CommandDeviceTime       : (True,None,[ResponseCommandStatus],"Set device time"),
        CommandWifiNetwork      : (True,None,[ResponseCommandStatus],"Set wireless network name"),
        CommandWifiPassword     : (True,None,[ResponseCommandStatus],"Set wireless network password"),
        CommandWifiJoin         : (True,None,[],"Join wireless network"),
        CommandWifiScan         : (True,None,[ResponseWirelessNetworks],"Scan for wireless networks"),
        CommandWifiLeave        : (True,None,[],"Leave wireless network"),
        CommandResetSettings    : (True,None,[ResponseCommandStatus],"Reset default user settings"),
        CommandHeat             : (True,None,[ResponseCommandStatus],"Heat kettle"),
        CommandKettleStop       : (True,None,[ResponseCommandStatus],"Stop heating kettle"),
        CommandHeatFormula      : (True,None,[ResponseCommandStatus],"Heat kettle using formula mode"),
        CommandKettleStoreSettings : (True,None,[ResponseCommandStatus],"Set kettle default user settings"),
        Command20               : (True,None,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        CommandHeatDefault      : (True,None,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        Command22               : (True,None,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        Command23               : (True,None,[ResponseCommandStatus],"Working unknown command (turn on?)"),
        CommandKettleHistory    : (True,None,[ResponseKettleHistory],"Get kettle history"),
        CommandStoreBase        : (True,None,[],"Set water sensor base value"),
        CommandBase             : (True,None,[ResponseBase,ResponseCommandStatus],"Get water sensor base value"),
        CommandCalibrate        : (True,None,[ResponseBase,ResponseCommandStatus],"Calibrate water sensor"),
        CommandKettleSettings   : (True,None,[ResponseKettleSettings],"Get default kettle user settings"),
        Command30               : (True,None,[],"Working unknown command"),
        CommandBrew             : (False,True,[],"Start coffee brewing"),
        CommandCoffeeStop       : (False,True,[],"Stop coffee brewing"),
        CommandStrength         : (False,True,[],"Set strength of the coffee to brew"),
        CommandCups             : (False,True,[],"Set number of cups to brew"),
        CommandBrewDefault      : (False,True,[],"Start coffee brewing using default"),
        CommandCoffeeStoreSettings : (False,True,[],"Set coffee machine default user settings"),
        CommandGrinder          : (False,True,[],"Toggle grinder"),
        CommandHotplateOn       : (False,True,[],"Turn on hotplate"),
        CommandCarafe           : (False,True,[],"Get coffee carafe required"),
        CommandSingleCupMode    : (False,True,[],"Get single coffee cup mode"),
        Command40               : (False,None,[],"Working unknown command (schedule?)"),
        Command41               : (False,None,[],"Working unknown command (schedule?)"),
        Command43               : (False,None,[],"Working unknown command (schedule?)"),
        Command4b               : (False,True,[ResponseCommandStatus],"Working unknown command"),
        Command4e               : (False,True,[ResponseCommandStatus],"Working unknown command"),
        CommandCoffeeSettings   : (False,True,[ResponseCoffeeSettings],"Get default coffee machine user settings"),
        CommandCoffeeHistory    : (False,True,[ResponseCoffeeHistory],"Get coffee machine history"),
        CommandHotplateOff      : (False,True,[],"Turn off hotplate"),
        CommandDeviceInfo       : (True,True,[ResponseDeviceInfo],"Get device info"),
        Command69               : (True,None,[ResponseCommandStatus],"Working unknown command"),
        CommandWifiFirmware     : (True,None,[ResponseWifiFirmware],"Get wifi firmware info"),
        CommandUpdate           : (True,None,[],"Device firmware update")

    #
    }


    # format: kettle?, coffee? (None is unnknown), minimal length (0 = variable), response to command, description
    ResponseMessages = {
        ResponseCommandStatus   : (True,True,3,[CommandDeviceTime,CommandWifiNetwork,CommandWifiPassword,CommandResetSettings,CommandHeat,CommandKettleStop,CommandHeatFormula,CommandKettleStoreSettings,Command20,CommandHeatDefault,Command22,Command23,CommandBase,CommandCalibrate,Command69,Command4b,Command4e],"Command status"),
        ResponseWirelessNetworks: (True,None,0,[CommandWifiScan],"Wireless networks list"),
        ResponseKettleHistory   : (True,False,0,[CommandKettleHistory],"Kettle history"),
        ResponseCoffeeHistory   : (False,True,0,[CommandCoffeeHistory],"Coffee machine history"),
        ResponseBase            : (True,None,4,[CommandBase,CommandCalibrate],"Water sensor base value"),
        ResponseKettleSettings  : (True,True,9,[CommandKettleSettings],"Default kettle user settings"),
        ResponseKettleStatus    : (True,True,7,[],"Kettle status"),
        ResponseDeviceInfo      : (True,True,4,[CommandDeviceInfo],"Device info"),
        ResponseWifiFirmware    : (True,None,0,[CommandWifiFirmware],"Wifi firmware info"),
        ResponseCarafe          : (False,True,3,[CommandCarafe],"Carafe required"),
        ResponseCoffeeStatus    : (False,True,0,[],"Coffee machine status"),
        ResponseSingleCupMode   : (False,True,3,[CommandSingleCupMode],"Single coffee cup mode"),

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


    WaterLevel = {
        0x00 : "Empty",
        0x00 : "Low",
        0x02 : "Half",
        0x03 : "Full",
    }


    def water_level(self,level):
        if self.WaterLevel.has_key(level):
            return self.WaterLevel[level]
        else:
            return "Unknown water level " + self.number_to_code(level)


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
            message = message + sep + " let it cool down to " + Smarter.temperature_to_string(formulatemperature)
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


    #------------------------------------------------------
    # DEVICE & FIRMWARE ARGUMENT WRAPPER
    #------------------------------------------------------

    DeviceKettle              = 0x01
    DeviceCoffee              = 0x02


    KettleFirmwareVerified    = [18,19]
    CoffeeFirmwareVerified    = [22]


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
            return "SmarterCoffee "
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


    def check_strength(self,strength):
        if strength == self.CoffeeMedium or strength == self.CoffeeStrong or strength == self.CoffeeWeak:
            return strength
        else:
            raise SmarterError("Invalid coffee strength [weak, medium, strong]: " + strength)

    def strength_to_raw(self,strength):
        return self.number_to_raw(self.check_strength(strength))


    def raw_to_strength(self,raw):
        return self.check_strength(self.raw_to_number(raw))
    
    
    def strength_to_string(self,raw):
        return self.StatusCoffeeStrength[self.check_strength(strength)]


    def string_to_strength(self,strength):
        if strength.strip().lower() == "weak":        
            return self.CoffeeWeak
        elif strength.strip().lower() == "medium":
            return self.CoffeeWeak
        elif strength.strip().lower() == "strong":
            raw = self.CoffeeStrong
        else:
            raise SmarterError("Invalid coffee strength [weak, medium, strong]: " + strength)



    #------------------------------------------------------
    # TEMPERATURE ARGUMENT WRAPPER
    #------------------------------------------------------

    def is_on_base(self,raw):
        return self.raw_to_number(raw) != self.MessageOffBase
 
 
    def celsius_to_fahrenheid(self,temperature):
        return ((temperature * 9) / 5) + 32
    
    
    def fahrenheid_to_celsius(self,temperature):
        return ((temperature - 32) * 5) / 9
    
    
    def check_temperature_celsius(self,temperature):
        # if fahrenheid then converto...
        # if self.Fahrenheid
        if temperature < 0 or temperature > 100 and not self.is_on_base(self.number_to_raw(temperature)):
            if self.Fahrenheid:
                raise SmarterError("Temperature out of range ["+self.celsius_to_fahrenheid(0)+".."+self.celsius_to_fahrenheid(100)+"] ºK: " + str(temperature))
            else:
                raise SmarterError("Temperature out of range [0..100] ºC: " + str(temperature))
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
            return "Fahrenheid"
        else:
            return "Celsius"

    def string_to_temperature(self,string):
        try:
            if self.Fahrenheid:
                return self.fahrenheid_to_celsius(int(string))
            else:
                return int(temperature)
        except:
            raise SmarterError("Temperature is not a number: " + string)



    #------------------------------------------------------
    # HOTPLATE KEEPWARM ARGUMENT WRAPPER
    #------------------------------------------------------


    def string_to_hotplate(self,string):
        try:
            return int(string)
        except:
            raise SmarterError("Hotplate timer is not a number: " + string)

    def check_hotplate(self,timer):
        if timer != 0 and (timer < 5 or timer > 40):
            raise SmarterError("Hotplate timer out of range [0] or [5..40] minutes: " + str(timer))
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
            raise SmarterError("Keepwarm timer is not a number: " + string)


    def check_keepwarm(self,timer):
        if timer != 0 and (timer < 5 or timer > 20):
            raise SmarterError("Kettle keep warm timer out of range [0] or [5..20] minutes: " + str(timer))
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
            raise SmarterError("Watersensor out of range [0..4095]")
        return watersensor
        
    def raw_to_watersensor(self,raw_low,raw_high):
        return self.check_watersensor(self.raw_to_number(raw_low) * 256 + self.raw_to_number(raw_high))


    def watersensor_to_raw(self,watersensor):
        return self.number_to_raw(watersensor / 256) + self.number_to_raw(watersensor % 256)

    def string_to_watersensor(self,string):
        try:
            watersensor = int(string)
        except:
            raise SmarterError("Not a watersensor value")
        return self.check_watersensor(watersensor)
 
 
    #------------------------------------------------------
    # BOOLEAN ARGUMENT WRAPPER
    #------------------------------------------------------

    def raw_to_bool(self,raw):
        bool = self.raw_to_number(raw)
        if bool > 1:
            raise SmarterError("Not a boolean value: " + str(int))
        if bool == 1:
            return True
        return False
 
 
    def bool_to_raw(self,boolean):
        return self.number_to_raw(boolean)


    #------------------------------------------------------
    # CUPS ARGUMENT WRAPPER
    #------------------------------------------------------

    def check_cups(self,cups_raw):
        cups = cups_raw % 12
        if cups < 1 or cups > 12:
            raise SmarterError("Unknown coffee cups [1..12]: " + str(cups))
        return cups


    def raw_to_cups(self,raw):
        return self.check_cups(self.raw_to_number(raw))


    def cups_to_raw(self,cups):
        return self.number_to_raw(self.check_cups(cups))
    

    def string_to_cups(self,string):
        try:
            cups = int(string)
        except:
            raise SmarterError("Unknown coffee cups [1..12]: " + string)
        return self.check_cups(cups)


    def cups_to_string(self,cups):
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
