# -*- coding: utf8 -*-

from SmarterProtocol import *

#------------------------------------------------------
# SMARTER PROTOCOL HELP
#
# Python help interface to iKettle 2.0 & SmarterCoffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Kettle Rattle (rev 6)
#------------------------------------------------------



#------------------------------------------------------
# PRINT PROTOCOL HELP
#------------------------------------------------------


class SmarterProtocolHelp:


    def message(self,id):
        print
        print
        print "  " + Smarter.message_is_type(id) + " Message " + Smarter.number_to_code(id) + ": " + Smarter.message_description(id)
        print "  ─────────────────────────────────────────────────────────────────────────"
        s = ""
        if Smarter.message_is_known(id):
            for i, iid in enumerate(Smarter.message_connection(id)):
                s = s + "[" + Smarter.number_to_code(iid) + "," + Smarter.message_description(iid) + "] "
            if Smarter.message_connection(id):
                if Smarter.message_is_response(id):
                    print "  In response to command message: " + s
                elif Smarter.message_is_command(id):
                    print "  Response message: " + s
            if Smarter.message_is_response(id):
                length = Smarter.message_response_length(id)
                if length > 0:
                    print "  Message Size: " + str(length) + " bytes"
            print
            print "  " + Smarter.message_kettle_supported(id) + " iKettle 2.0   " + Smarter.message_coffee_supported(id) + " SmarterCoffee "
        print

        if id == Smarter.CommandDeviceTime:
            print "  Set the time on the device, is used in history reply messages."
            print "  Unknown is Day of week index?"
            print
            print "  Arguments: <SECONDS><MINUTES><HOURS><??><DAY><MONTH><CENTURY><YEAR>"
            print
            print "  SECONDS"
            print "    00..3b"
            print
            print "  MINUTES"
            print "    00..3b"
            print
            print "  HOURS"
            print "    00..17"
            print
            print "  DAY"
            print "    00..1e"
            print
            print "  MONTH"
            print "    00..0b"
            print
            print "  CENTURY"
            print "    13..15"
            print
            print "  YEAR"
            print "    00..63"
            print
            print "  Example: 02 12 13 03 01 05 02 14 10 ???"
            
        elif id == Smarter.ResponseCommandStatus:
            print "  Response: <STATUS>"
            print
            print "  STATUS"
            print "    00 Success"
            print "    01 Busy"
            print "    02 No Carafe (Coffee unverified)"
            print "    03 No Water (Coffee unverified)"
            print "    04 Failed"
            print "    05 No Carafe"
            print "    06 No Water"
            print "    69 Invalid Command"
            print
            print "  The response status of the coffee can be bit encoded (see response 14)"
            
        elif id == Smarter.CommandWifiNetwork:
            print "  Argument: <SSID>{0,32}"
            print "  Just normal ascii"
            
        elif id == Smarter.CommandWifiPassword:
            print "  Argument: <PASSWORD>{0,32}"
            print "  Just normal ascii"
            
        elif id == Smarter.CommandWifiJoin:
            print "  Sending this command without previous SSID/password messages will reset the wifi"
            print "  to factory settings."
            print
            print "  Send:"
            print "    " + Smarter.message_description(Smarter.CommandWifiNetwork)
            print "    " + Smarter.message_description(Smarter.CommandWifiPassword)
            print "    " + Smarter.message_description(Smarter.CommandWifiJoin)
            print
            print "  Read all the command status ssuccess"
            print
            print "  The apps actually sends: 0c 7e 00 00 00 00 00 00"

        elif id == Smarter.CommandWifiScan:
            print "  Example raw code: 0d 7e"
            
        elif id == Smarter.ResponseWirelessNetworks:
            print "  DB is the signal strength in dBm format."
            print
            print "  Response: <SSID>{0,32}<\",-\"><DB>{2}<\"}\">"
            print
            print "  Examples: MyWifi,-56}"
            print "            MyWifi,-56}OtherWifi,-82}"
            
        elif id == Smarter.CommandWifiLeave:
            print "  Leaves wireless network and reset wifi to default"
            print
            print "  Example raw code: 0f 7e"
            print "  It actually sends: 0f 7e 6d 7e"
            
        elif id == Smarter.CommandResetSettings:
            print "  For the kettle these are the default user settings:"
            print "  keepwarm 0 minutes (0x00), temperature 100ºC (0x64)"
            print "  formula mode off (0x00) and formula temperature 75ºC (0x4b)"
            print
            print "  The SmarterCoffee  it will probably reset the number of cups and strength"
            print
            print "  Example raw code: 10 7e"
            
        elif id == Smarter.ResponseKettleStatus:
            print "  There is correlation between the temperature the watersensor and the base. How higher"
            print "  the temperature how higher the watersensor with the same volume of water."
            print
            print "  Response iKettle: <STATUSKETTLE><TEMPERATURE><WATERSENSORBITSHIGH><WATERSENSORBITSLOW><??>"
            print
            print "  Response SmarterCoffee : <STATUSCOFFEE><WATERLEVEL><WIFISTRENGTH???/WATERSENSORBITSLOW???>"
            print "                           <STRENGTH><CUPS>"
            print
            print "  STATUSKETTLE"
            print "    00 Ready"
            print "    01 Boiling"
            print "    02 Keep Warm"
            print "    03 Cycle Finished"
            print "    04 Baby Cooling"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print "    7f      Kettle Off Base"
            print
            print "  WATERSENSOR = WATERSENSORHIGHBITS * 256 + WATERSENSORLOWBITS  [0..4095]"
        
        elif id == Smarter.CommandHeat:
            print "  if it's warming you have to send an off command to boil again"
            print "  if it's not on temp it boils first before warming..."
            print
            print "  Argument: <TEMPERATURE><KEEPWARMTIME>"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  KEEPWARMTIME"
            print "    00      Default off"
            print "    05..1e  Keep Warm in Minutes"
            print
            print "  Example: 15 32 00 7e"
            
        elif id == Smarter.CommandKettleStop:
            print "  Example: 16 7e"
            
        elif id == Smarter.CommandHeatFormula:
            print "  Boil water to (default user temperature)"
            print  " and cool until the formula temperature and then keep it warm."
            print
            print "  Arguments: <FORMULATEMPERATURE><KEEPWARMTIME>"
            print
            print "  KEEPWARMTIME"
            print "    00      Default off"
            print "    05..1e  Keep Warm in Minutes"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  FORMULATEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  Example: 19 32 19 7e"
            
        elif id == Smarter.CommandKettleStoreSettings:
            print "  Default user defaults message is 1f 00 64 00 4b 7e"
            print
            print "  Arguments: <KEEPWARMTIME><TEMPERATURE><FORMULA><FORMULATEMPERATURE>"
            print
            print "  KEEPWARMTIME"
            print "    00      Default off"
            print "    05..1e  Keep Warm in Minutes"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  FORMULA"
            print "    00 Do not use as default"
            print "    01 Use as default"
            print
            print "  FORMULATEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  Example: 1f 19 64 01 22 7e"
            print
            print
            
        elif id == Smarter.Command20:
            print "  This setting ignores the user setting and boils till 100C"
            print
            print "  Example raw code: 20 7e"
            
        elif id == Smarter.CommandHeat:
            print "  If no arguments are given it uses its default."
            print
            print "  Arguments: <[<TEMPERATURE><[KEEKWARMTIME]>]>"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  KEEPWARMTIME"
            print "    00      Default off"
            print "    05..1e  Keep Warm in Minutes"
            print
            print "  Examples: 21 50 05 7e"
            print "            21 44 7e"
            print "            21 7e"
            print
            print "  Heat up till 90 if default is 80"
            
        elif id == Smarter.Command22:
            print "  Example: 22 7e"
            
        elif id == Smarter.Command23:
            print "  Example: 23 7e"
            
        elif id == Smarter.CommandKettleHistory:
            print "  When called will erase this history."
            print
            print "  Example: 28 7e"

        elif id == Smarter.CommandCoffeeHistory:
            print "  When called will erase this history."
            print
            print "  Example: 46 7e"
        
        elif id == Smarter.ResponseCoffeeHistory:
            print "  The payload is generated everytime the coffee machine brews. The actioncounter increases with every boil"
            print "  Formula temperature is above 0 then it was boilded with formula temperature enabled. There seems to be some"
            print "  packed time available."
            print
            print "  Payload maximum is 8. So if 8 check again, if there is more history"
            print "  month checked only accepts value from 1..0c"
            print
            print "  Response: <COUNTER> [<PAYLOAD>{COUNTER}]"
            print
            print "  COUNTER"
            print "    00..08"
            print
            print "  PAYLOAD"
            print "    <??><??><??><DEFAULT/CUPS?><DEFAULT/CUPS?><SECONDS??>"
            print "    <HOURS???><MINUTES???><DAY??><MONTH><YEAR80???><STATE><??>{19}"
            print
            print "  CUPS"
            print "    00..0c"
            print
            print "  SECONDS"
            print "    00..3b"
            print
            print "  MINUTES"
            print "    00..3b"
            print
            print "  HOURS"
            print "    00..17"
            print
            print "  DAY"
            print "    00..1e"
            print
            print "  MONTH"
            print "    00..0b"
            print
            print "  YEAR80"
            print "    00..FF  YEAR = YEAR80 + 1980"
            print
            print "  STATE"
            print "    00 Stopped"
            print "    01 Success"
            print
            print "  Example: 47 02 01 00 00 02 02 00 19 00 01 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d"
            print "                 01 00 00 0c 0c 00 19 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e"
           
        elif id == Smarter.ResponseKettleHistory:
            print "  The payload is generated everytime the kettle stops boiling. The actioncounter increases with every boil"
            print "  Formula temperature is above 0 then it was boilded with formula temperature enabled. There seems to be some"
            print "  packed time available."
            print
            print "  Payload maximum is 8. So if 8 check again, if there is more history"
            print "  month checked only accepts value from 1..0c"
            print
            print "  Response: <COUNTER> [<PAYLOAD>{COUNTER}]"
            print
            print "  PAYLOAD"
            print "    <??><TEMPERATURE><KEEPWARMTIME><FORMULATEMPERATURE><ACTIONCOUNTER>"
            print "    <SECONDS??><HOURS?><MINUTES?><DAY?><MONTH><YEAR80?><STATE><??>{19}"
            print
            print "  COUNTER"
            print "    00..08"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  KEEPWARMTIME"
            print "    00      Default off"
            print "    05..1e  Keep Warm in Minutes"
            print
            print "  FORMULATEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  ACTIONCOUNTER"
            print "    00..ff  Amount of boils before off base"
            print
            print "  SECONDS"
            print "    00..3b"
            print
            print "  MINUTES"
            print "    00..3b"
            print
            print "  HOURS"
            print "    00..17"
            print
            print "  DAY"
            print "    00..1e"
            print
            print "  MONTH"
            print "    00..0b"
            print
            print "  YEAR80"
            print "    00..FF  YEAR = YEAR80 + 1980"
            print
            print "  STATE"
            print "    00 Stopped"
            print "    01 Success"
            print
            print "  Example: 29 02 01 5f 00 00 0f 00 09 03 15 0a 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d"
            print "                 01 64 19 32 10 00 09 0e 15 0a 19 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e"
        
        elif id == Smarter.CommandStoreBase:
            print "  Arguments: <BASELHIGHBITS><BASELOWBITS>"
            print
            print "  BASE = BASELHIGHBITS * 256 + BASELOWBITS [0..4095]"
            print "  Example: 2a 04 03"
            print
            print "  This can contain the tail 7e, so check for length here!"

        elif id == Smarter.CommandBase:
            print "  Example: 2b 7e"
            
        elif id == Smarter.CommandCalibrate:
            print "  Example: 2c 7e"
            print
            print "  Returns also a command success response message after the base repsonse message"
            
        elif id == Smarter.ResponseBase:
            print "  Response: <BASELHIGHBITS><BASELOWBITS>"
            print
            print "  BASE = BASELHIGHBITS * 256 + BASELOWBITS [0..4095]"
            print
            print "  This can contain the tail 7e, so check for length here!"
            
        elif id == Smarter.CommandCoffeeSettings:
            print "  Also return 00 message in an unconfigured state.???? CHECK"
            print
            print "  Example: 48 7e"


        elif id == Smarter.CommandKettleSettings:
            print "  Also return 00 message in an unconfigured state.??? CHECK"
            print
            print "  Example: 2e 7e"


        elif id == Smarter.ResponseCoffeeSettings:
            print "  Response: <CUPS><STRENGTH><GRINDER><HOTPLATE>"
            print
            print "  CUPS"
            print "    00..0c"
            print
            print "  STRENGTH"
            print "    00 Weak"
            print "    01 Medium"
            print "    02 Strong"
            print
            print "  GRINDER <BOOLEAN>"
            print
            print "  HOTPLATE"
            print "    05..28 5 .. 40 minutes"
            print "    05     5 Minutes (Default)"
            print

        elif id == Smarter.ResponseKettleSettings:
            print "  Response: <KEEPWARMTIME><TEMPERATURE><FORMULATEMPERATURE>"
            print
            print "  KEEPWARMTIME"
            print "    00      Default off"
            print "    05..1e  Keep Warm in Minutes"
            print
            print "  TEMPERATURE"
            print "    00..64  0..100ºC"
            print
            print "  FORMULATEMPERATURE"
            print "    00..64  0..100ºC"
            
        elif id == Smarter.Command30:
            print "  Arguments: <[UNKNOWN]>{?}"
            print
            print "  Example: 30 7e"
                        
        elif id == Smarter.Command4b:
            print "  Arguments: <[UNKNOWN]>{?}"
            print
            print "  Example: 4b ?? 7e"
        
        elif id == Smarter.Command4e:
            print "  Arguments: <[UNKNOWN]>{?}"
            print
            print "  Example: 4e ?? 7e"
        
        elif id == Smarter.CommandBrew:
            print "  Example: 33 .. .. .. 7e"
            
        elif id == Smarter.CommandStrength:
            print "  Sets the strength of the coffee to be brewed. Use command 37 to brew"
            print "  Argument: <STRENGTH>"
            print
            print "  STRENGTH"
            print "    00 Weak"
            print "    01 Medium"
            print "    02 Strong"
            print
            print "  Example: 35 01 7e"
            
        elif id == Smarter.CommandCups:
            print "  Sets the number of cups to be brewed, range between 1 and 12."
            print "  Use command 37 to brew"
            print
            print "  Argument: <CUPS>"
            print
            print "  CUPS"
            print "    00..0c"
            print
            print "  Example: 36 03 7e"
            
        elif id == Smarter.CommandBrewDefault:
            print "  Example: 37 7e"
            
        elif id == Smarter.CommandGrinder:
            print "  Example: 3c 7e"
            
        elif id == Smarter.CommandHotplateOn:
            print "  Sets on the hotplate, you can specify how many minutes before it switch off."
            print "  Range between 5 and 40, the app sends 5 on default"
            print
            print "  Argument: <[KEEPWARMTIME]>"
            print
            print "  KEEPWARMTIME"
            print "    05..28 5 .. 40 minutes"
            print "    05     5 Minutes (Default)"
            print
            print "  Example: 3e 05 7e"
            
        elif id == Smarter.Command40:
            print "  Updating schedules"
            print "  No information available on message"
            
        elif id == Smarter.Command41:
            print "  Requesting schedules"
            print "  No information available on message"
            
        elif id == Smarter.Command43:
            print "  Schedules"
            print "  No information available on message"
            
        elif id == Smarter.CommandHotplateOff:
            print "  Example: 4a 7e"
            
        elif id == Smarter.CommandDeviceInfo:
            print "  Get the type of the device connected to and it's firmware. It is used for"
            print "  auto discovery over UDP broadcast (after device setup is complete?)"
            print "  This fails on some routers, which don't propagate UDP broadcasts"
            print
            print "  Example: 64 7e"
            
        elif id == Smarter.ResponseDeviceInfo:
            print "  Response: <TYPE><VERSION>"
            print
            print "  TYPE:"
            print "    01 iKettle 2.0"
            print "    02 SmarterCoffee "
            print
            print "  VERSION:"
            print "    13 Firmware v19 of iKettle 2.0"
            print
            print "  Example: 65 01 13 7e"
            
        elif id == Smarter.Command69:
            print "  Without argumens it returns failed otherwise it returns success."
            print
            print "  Arguments: <UNKNOWN>{?}"
            print
            print "  Example: 69 7e"
            
        elif id == Smarter.CommandWifiFirmware:
            print "  Example: 6a 7e"
            
        elif id == Smarter.ResponseWifiFirmware:
            print "  The firmware of the wifi module in text with control chars as new line."
            print "  The iKettle 2.0 returns (without control chars):"
            print
            print "  Response: <FIRMWARE>{?}"
            print
            print "  AT+GMR"
            print "  AT version:0.40.0.0(Aug  8 2015 14:45:58)"
            print "  SDK version:1.3.0"
            print "  compile time:Aug  8 2015 17:19:38"
            print "  OK"
            
        elif id == Smarter.CommandUpdate:
            print "  Disables wifi and creates a 'iKettle Update' wireless network and opens port 6000."
            print "  A hard device reset (hold power button for 10 seconds) is sometimes required to fix this state,"
            print "  or just unplug the power for a moment."
            print
            print "  Example: 6d 7e"

        elif id == Smarter.ResponseCarafe:
            print "  Response: <BOOLEAN>"

        elif id == Smarter.ResponseSingleCupMode:
            print "  Response: <BOOLEAN>"

        elif id == Smarter.ResponseCoffeeStatus:
            print "  I do not have a smarter coffee, but I suspect that the WIFISTRENGTH is just"
            print "  the WATERSENSORBITSLOW part of the waterlevel sensor."
            print
            print "  Response: <STATUSCOFFEE><WATERLEVEL><WIFISTRENGTH???/WATERSENSORBITSLOW???><STRENGTH><CUPS>"
            print
            print "  STATUSKETTLE"
            print "    00 Ready"
            print "    01 Boiling"
            print "    02 Keep Warm"
            print "    03 Cycle Finished"
            print "    04 Baby Cooling"
            print
            print "  WATERSENSOR = WATERSENSORHIGHBITS * 256 + WATERSENSORLOWBITS"
            print
            print "  STATUSCOFFEE (unverified)"
            print "    04 Filter, ?                      #  00000100"
            print "    05 Filter, OK to start            #  00000101"
            print "    06 Filter, OK to start            #  00000110"
            print "    07 Beans, OK to start             #  00000111"
            print "    20 Filter, No carafe              #  00100000"
            print "    22 Beans, No carafe               #  00100010"
            print "    45 Filter, Done                   #  01000101 <-- from here actions"
            print "    47 Beans, Done                    #  01000111"
            print "    53 Boiling                        #  01010011"
            print "    60 Filter, No carafe, Hotplate On #  01100000"
            print "    61 Filter, Hotplate On            #  01100001"
            print "    62 Beans, No carafe, Hotplate On  #  01100010"
            print "    63 Beans, Hotplate On             #  01100011"
            print "    51 Descaling in progress          #  01010001"
            print "                                           HB RBC"
            print "                                           OO EEA"
            print "                                           TI AAR"
            print "                                           PL DNA"
            print "                                           LI YSF"
            print "                                           AN   E"
            print "                                           TG"
            print "                                           E"
            print
            print "  These are guesses I do not own a smarter coffee..."
            print "  BIT 0 = UNKNOWN/UNUSED?"
            print "  BIT 1 = ACTION???"
            print "  BIT 2 = HOTPLATE"
            print "  BIT 3 = Boiling & Descaling (USES BIT 6)"
            print "  BIT 4 = UNKNOWN/UNUSED?"
            print "  BIT 5 = READY/BUSY (OK TO START, FINISHED = 1 else 0)"
            print "  BIT 6 = FILTER/BEANS"
            print "  BIT 7 = CARAFE OFFBASE/ONBASE"
            print 
            print "  WATERLEVEL"
            print "    00 Not enough water"
            print "    01 Low"
            print "    02 Half"
            print "    12 Half"
            print "    13 Full"
            print
            print "  STRENGTH"
            print "    00 Weak"
            print "    01 Medium"
            print "    02 Strong"
            print
            print "  CUPS"
            print "    00..0c"

        elif id == Smarter.CommandCarafe:
            print " NEW"

        elif id == Smarter.CommandSingleCupMode:
            print " NEW"

        elif id == Smarter.CommandCoffeeStop:
            print "  Example 33 7e "

        elif id == Smarter.CommandCoffeeStoreSettings:
            print "  Arguments: <STRENGTH><CUPS><GRINDER><HOTPLATE>"
            print
            print "  STRENGTH"
            print "    00 Weak"
            print "    01 Medium"
            print "    02 Strong"
            print
            print "  CUPS"
            print "    00..0c"
            print
            print "  GRINDER <BOOLEAN>"
            print
            print "  HOTPLATE"
            print "    05..28 5 .. 40 minutes"
            print "    05     5 Minutes (Default)"
            print
        
        else:
            print "  No information available on message: " + Smarter.number_to_code(id)
            
        print
        print


    def messages(self):
        print
        print
        print "  Smarter iKettle 2.0 & SmarterCoffee  Messages"
        print "  _____________________________________________"
        print
        print
        print "    k c ID Command Message"
        print "    ___________________________________________"
        for id in range(0,255):
            if Smarter.message_is_command(id):
                print "    " + Smarter.message_kettle_supported(id) + " " + Smarter.message_coffee_supported(id) + " " + Smarter.number_to_code(id) + " " + Smarter.message_description(id)
        print
        print "    k c ID Response Message"
        print "    _______________________________"
        for id in range(0,255):
            if Smarter.message_is_response(id):
                print "    " + Smarter.message_kettle_supported(id) + " " + Smarter.message_coffee_supported(id) + " " + Smarter.number_to_code(id) + " " + Smarter.message_description(id)
        print
        print "    Legend:"
        print "      k iKettle 2"
        print "      c SmarterCoffee "
        print
        print


    def structure(self):
        print """
       
       
  Smarter iKettle 2.0 & SmarterCoffee  Protocol
  _____________________________________________

    Smarter uses a binary message protocol, either via UDP or TCP on port 2081

    Messages (commands and responses) use the syntax:

     <ID>[ARGUMENTS]<TAIL>

    Arguments use this syntax:

      <ARGUMENT>     is a single mandatory byte
      <[ARGUMENT]>   is a single optional byte
      <ARGUMENT>{x}  is mandatory, between 1 and x bytes
 
    The tail is always 7e or ~ in ASCII, everything else are ASCII literals
    
    There are some value's like the watersensor that can contains the tail
    so check the length of the response message!
    
              """
    

    def notes(self):
        print """


  Smarter iKettle 2.0 & SmarterCoffee  Notes
  __________________________________________
    
  WaterSensor Calibration:

    If the kettle is on the base during calibration, the numbers change to be higher,
    but the differences between levels seem the same. This means that the water level
    detection is probably weight based and that calibration is done at the base,
    which then remembers the weight for \'off base\'. To detect an empty kettle,
    the connecting device must account for the weight of the kettle.
    
    (yeah, not! the watersensor becomes higher if the temperature becomes higher...)


  Wireless Network:

    If the device (coffee?) is configured to access an wifi access point which is not available
    It will try to connect to it every so minutes. If it tries to connect it beeps three
    times the wifi access point of the device will remain active but unreachable,
    if it fails to access the access point it beeps once, and it opens up its own default
    open unencrypted wifi access point.access

    If connected to the kettle tcp 192.168.4.1:2081 is the default connection.

    The iKettle2.0 creates an access point with the name iKettle2.0:c0 where c0 is part
    of the mac address of the kettle. When connected directly to the kettle its connection is very flacky.


  Device Detection:
  
    To detect a device broadcast a device info command (message 64) on UDP. It will reply
    if the router permits it with a device info response (message 65) and being UDP 
    with its IP address!
    
    
  Capturing the protocol using WireShark:

     OSX:  (Home Network Only)
           Step 1: Download wireshark (https://www.wireshark.org/) for mac and install it.
           Step 2: Setup your kettle or coffee machine to use your home network.
           Step 3: Connect you mac to your network NOT using the build in wifi adapter.
                   Use either a cable (ethernet recommended) or a second wifi adapter.
           Step 4: Enable and setup internet sharing in system preferences, sharing.
           Step 5: Connect with your phone to the internet sharing wireless access point.
           Step 6: Run wiresharp it and select your build in wifi adapter and start the capture.
           Step 7: Look for connection with messages ending in 7e

    iOS & OSX: (Home network & Direct mode)
           Step 1: Connect your iOS device to your Mac via USB.
           Step 2: Get the <udid> for the connected device from iTunes (click on the serial).
           Step 3: Open terminal in your Mac and run the following commands, which creates a virtual network
                   adapter mirroring the iOS network, which we can dump and inspect:
           Step 4: rvictl -s <udid>
           Step 5: tcpdump -i rvi0 -w ~/Desktop/output.pcap
           Step 6: Connect to kettle's wifi network (or your home network if already setup) on the iOS device.
           Step 7: Run setup for smarter device setup, or any commands
           Step 8: When done or the device setup disconnected to switch to your home network, disconnect with ctrl-c
           Step 9: rvictl -x <udid>
           Step A: Download wireshark (https://www.wireshark.org/) for mac and install it.
           Stap B: Open ~/Desktop/output.pcap with Wireshark
           Step C: Look for connection with messages ending in 7e
 

  Security:

    iKettle 2.0:
         *  It will boil empty, making the lights bulbs to flikker.
         *  You can easily knock out it's connection to the wireless network,
            if it fails to connect it creates an default open unencrypted wifi access point 
            (check!, could be that wifi was not connecting, then this is rubbish ;-).

            Attack Vectors
            1. Repeat sending heat to 100ºC temperature commands, if we're lucky
               there is no water and it will boil empty, if not it will take a while.
               plus the kettle will get warmer and warmer. If you do not expect that when touching.
            2. Alternating heat and stop commands.
            3. (Check) Wait until the owner of the kettle log in on the kettle, since its an
               open access point and the password are send in the open you can read it.


  Coffee Brewing:

    Between setting the number of cups, the strength of the coffee and start of brewing
    atleast 500ms is recommended.
    

  Water Boiling:
  
    From smarter website the temperature that can be set is between 20 and 100. We still need to read lower 
    values for cold water in the kettle
     
 
              """

    def all(self):
        for id in range(0,255):
            if Smarter.message_is_known(id):
                self.message(id)


    def protocol(self):
        self.structure()
        self.messages()
        self.all()
        self.notes()


SmarterHelp = SmarterProtocolHelp()