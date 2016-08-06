# -*- coding: utf8 -*-

#------------------------------------------------------
# iBrew PROTOCOL
#
# Protocol information to iKettle 2.0 or Smarter Coffee
#------------------------------------------------------
#
#    References:
#    https://github.com/Jamstah/libsmarteram2/wiki/Protocol-documentation
#    https://github.com/ian-kent/ikettle2/tree/master/protocol
#    https://github.com/athombv/am.smarter/blob/master/node_modules/ikettle2.0/ikettle2.0.js
#    https://github.com/athombv/am.smarter/blob/master/node_modules/coffee/index.js
#    https://github.com/AdenForshaw/smarter-coffee-api/blob/master/smarter-coffee-api.py
#    https://www.pentestpartners.com/blog/hacking-a-wi-fi-coffee-machine-part-1/
#    https://www.hackster.io/lahorde/from-a-14-kettle-to-an-ikettle-d2b3f7
#    https://github.com/nanab/smartercoffee/blob/master/sendcommand.py
#
#
#

iBrewVersion = "White Tea Edition v0.07 © 2016 TRiXWooD"

# protocol information

iBrewMessageWorking = [[0,"Unknown"],
                      [1,"iKettle 2.0 only"],
                      [2,"SmarterCoffee only"],
                      [3,"iKettle 2.0 & Smarter Coffee"],
                      [4,"iKettle 2.0 (Smarter Cofee unknown)"],
                      [5,"Smarter Cofee (iKettle unknown)"],
                     ]

iBrewMessageType = [[False,"Command"],
                    [True, "Response"],
                   ]

iBrewMessages = [[0x02,0x00,False,4,"Set device time"],
                 [0x03,0xff,True ,3,"Command status"],
                 [0x05,0x00,False,4,"Set WiFi network SSID"],
                 [0x07,0x00,False,4,"Set WiFi network password"],
                 [0x0c,0x00,False,4,"Connect to WiFi network"],
                 [0x0d,0x0e,False,4,"Scan for WiFi networks"],
                 [0x0e,0xff,True ,4,"List of WiFi networks"],
                 [0x0f,0x00,False,4,"Reset Wifi networks"],
                 [0x10,0x00,False,4,"Working unknown command (reset?)"],
                 [0x14,0xff,True ,3,"Device status"],
                 [0x15,0x00,False,4,"Turn on kettle"],
                 [0x16,0x00,False,4,"Turn off kettle"],
                 [0x19,0x00,False,4,"Working unknown command"],
                 [0x20,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x21,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x22,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x23,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x28,0x29,False,4,"Working unknown command"],
                 [0x29,0xff,True ,4,"working unknown reply 28"],
                 [0x2a,0x00,False,4,"Working unknown command"],
                 [0x2b,0x2d,False,4,"Get watersensor base value"],
                 [0x2c,0x2d,False,4,"Calibrate watersensor"],
                 [0x2d,0xff,True ,4,"Watersensor base value"],
                 [0x30,0x00,False,4,"Working unknown command"],
                 [0x32,0x00,False,0,"Working unknown command"],
                 [0x33,0x00,False,0,"Working unknown command"],
                 [0x35,0x00,False,2,"Set strength of the coffee to brew"],
                 [0x36,0x00,False,2,"Set number of cups to brew"],
                 [0x37,0x00,False,2,"Working unknown command"],
                 [0x3c,0x00,False,2,"Toggle grinder"],
                 [0x3e,0x00,False,2,"Turn on hotplate"],
                 [0x40,0x00,False,2,"Working unknown command"],
                 [0x41,0x00,False,2,"Working unknown command"],
                 [0x43,0x00,False,2,"Working unknown command"],
                 [0x4a,0x00,False,2,"Turn off hotplate"],
                 [0x64,0x65,False,3,"Get Identify of device"],
                 [0x65,0xff,True ,3,"Identify of device"],
                 [0x69,0x00,False,4,"Working unknown command"],
                 [0x6a,0x6b,False,4,"Get WiFi firmware info"],
                 [0x6b,0xff,True ,4,"Wifi firmware Info"],
                 [0x6d,0x00,False,4,"Firmware upgrade"],
                ]

                #  /|\  /|\  /|\ /|\  /|\
                #   |    |    |   |    |
                #   |    |    |   |
                #   |    |    |   |   Message Description
                #   |    |    |
                #   |    |    |  Message Working
                #   |    |
                #   |    |   Message Type
                #   |
                #   |   Message Response ID ( 0xff no reply or response message, 0x00 unknown)
                #
                #  Message ID


iBrewPort = 2081

iBrewCommandInfo             = '\x64'
    
# Coffee Commands (not tested)
iBrewCommandGrinder          = '\x3c'
iBrewCommandHotplateOff      = '\x4a'
iBrewCommandHotplateOn       = '\x3e'
iBrewCommandNumberOfCups     = '\x36'
iBrewCommandStrength         = '\x35'
    
# iKettle Commands
iBrewCommandCalibrate        = '\x2c'
iBrewCommandCalibrateBase    = '\x2b'
iBrewCommandOff              = '\x16'
iBrewCommandOn               = '\x21'

# Response messages
iBrewResponeStatus           = '\x03'
iBrewResponeWifiList         = '\x0e'
iBrewResponeUnknown          = '\x29'
iBrewResponeCalibrationBase  = '\x2d'
iBrewResponeStatusDevice     = '\x14'
iBrewResponeDeviceInfo       = '\x65'
iBrewResponeWifiFirmware     = '\x6b'
    
iBrewTail    = '\x7e'
iBrewOffBase = '\x7f'
    
iBrewStatusKettle = {
    0x00 : "Ready",
    0x01 : "Boiling",
    0x02 : "Keep Warm",
    0x03 : "Cycle Finished",
    0x04 : "Baby Cooling",
}
    
iBrewStatusCommand = {
    0x00 : "Success",
    0x01 : "Busy",
    0x02 : "No Carafe",
    0x03 : "No Water",
    0x04 : "Failed",
    0x05 : "No Carafe",  # which one?
    0x06 : "No Water",   # which one?
    0x69 : "Invalid Command",
    0xff : "Unknown"
}

class iBrewProtocol:
    def base(self):
        print
        print "Smarter iKettle 2.0 & Smarter Coffee Protocol"
        print "_____________________________________________"
        print
        print "Smarter uses a binary message protocol,"
        print "either via UDP or TCP on port 2081"
        print
        print "Messages (commands and responses) use the syntax:"
        print
        print "    <ID>[ARGUMENTS]<TAIL>"
        print
        print ""
        print "The tail is always 7e or ~ in ASCII"
        print
        print "Arguments use this syntax:"
        print
        print "    <ARGUMENT>   is a single mandatory byte"
        print "    <[ARGUMENT]> is a single optional byte"
        print "    <ARGUMENT>{0,32} is mandatory, between 0 and 32 bytes"
        print
        print "Everything else, including spurious } characters, are ASCII literals"
        print
        print "Use messages command to list all messages"
        print

    def messages(self):
        print
        print "♨ ☕ ID Command Message Description"
        print "____________________________________"
        print "♨   02 Set the machine time"
        print "♨   05 Set network SSID"
        print "♨   07 Set WiFi password"
        print "✕   07 Start brewing Coffee???)"
        print "♨   0c Hangs (Connect to Wifi)"
        print "♨   0d Scan for WiFi networks"
        print "♨   0f Reset Wifi networks"
        print "    10 Reset ???"
        print "♨   15 Turn on"
        print "♨   16 Turn off"
        print "♨   19 ????"
        print "♨   20 Boiling Turn on"
        print "♨   21 Boiling Turn on"
        print "♨   22 Boiling Turn on"
        print "♨   23 Boiling Turn on ???"
        print "♨   28 ???"
        print "♨   2a ???"
        print "♨   2b Calibrate Base Value"
        print "♨   2c Calibrate Water Sensor"
        print "♨   30 ???"
        print "    32 ???"
        print "✕ ☕ 35 Set strength of the coffee to brew"
        print "✕ ☕ 36 Set number of cups to brew"
        print "✕ ☕ 37 ???"
        print "✕ ☕ 3c Toggle the Grinder on/off"
        print "✕ ☕ 3e Turn on the hotplate"
        print "✕ ☕ 40 Updating schedules ???"
        print "✕ ☕ 41 Requesting schedules ???"
        print "✕ ☕ 43 Schedules ???"
        print "✕ ☕ 4a Turn off the hot plate"
        print "♨ ☕ 64 Get Identify of device"
        print "♨   69 ???"
        print "♨   6a Get Firmware Info WiFi module"
        print "    6d Firmware Update"
        print
        print "♨ ☕ ID Response Message Description"
        print "___________________________________"
        print "♨ ☕ 03 Status"
        print "♨   0e List of WiFi networks"
        print "♨   29 ???"
        print "♨   14 Device status"
        print "♨   2d Calibrate base value"
        print "♨ ☕ 65 Identify of device"
        print "♨ ☕ 6b Firmware Indo WiFi module"
        
        print
        print "Legend:"
        print "  ♨ iKettle 2"
        print "  ☕ Smarter Coffee"
        print

    def calibration(self):
        print
        print "Calibration:"
        print
        print "      If the kettle is on the base during calibration, the numbers change to be higher,"
        print "      but the differences between levels seem the same. This means that the water level"
        print "      detection is probably weight based and that calibration is done at the base,"
        print "      which then remembers the weight for \'off base\'. To detect an empty kettle,"
        print "      the connecting device must account for the weight of the kettle itself."

    def wifi(self):
        print
        print "WiFi:"
        print
        print "      If the device is configured to access an WiFi access point which is bot available"
        print "      It will try to connect to it every so minutes, if it fails it sets up its default"
        print "      open unencrypted WiFi access point."

        print "This "

    def coffeeBrewing(self):
        print
        print "Coffee Brewing:"
        print
        print "      Between setting the number of cups, the strength of the coffee and start of brewing"
        print "      atleast 500ms is recommended."


    def message(self,id):
        print "________________________________________________"
        if id == '02':
            print "Message 02: Set Time"
            print "  ?"
            print
            print "Arguments: <Seconds><Minutes><Hours><Unknown><Day><Month><Century><Year>"
            print "Note: Unknown is Day of week index?"
        
        elif id == '03':
            #Fix
            print "d"
        elif id == '05':
            print "Message 05: Set network SSID"
            print "  ?"
            print
            print "Argument: <SSID>{0,32}"
            print "Note: SSID is between 0 and 32 characters"
            self.wifi()
        elif id == '07':
            print "Message 07: Set WiFi password"
            print "  ?"
            print
            print "Argument: <password>{0,32}"
            print "Note: password is between 0 and 32 characters"
            print
            print "Message 07: Start brewing Coffee???"
            print " ?"
            self.wifi()
        elif id == '0c':
            print "Message 0c: WiFi setup finished"
            print "  ?"
            print
            print "No information available on message"
            self.wifi()
        elif id == '0d':
            print "Message 0d: Scan for WiFi networks"
            print "  ?"
            print
            print "Returns: Message 0e"
            print
            print "Example raw code: 0d 7e"
            self.wifi()
        elif id == '0e':
            print "Message 0e: List of WiFi network"
            print "  ?"
            print
            print "Arguments: <SSID>{0,32},-<db>{2}}"
            print "Note: SSID is between 0 and 32 characters"
            print "      Sending message 0c without previous SSID/password messages will reset WiFi to factory settings"
            print "      -db is the signal strength in dBm format"
            print
            print "Examples: MyWifi,-56}"
            print "          MyWifi,-56}OtherWifi,-82}"
            self.wifi()
        elif id == '0f':
            print "Message 0d: Reset WiFi networks"
            print "  ?"
            print
            print "Returns: Message 0f"
            print
            print "Example raw code: 0f 7e"
        elif id == '10':
            print "Message 10: Reset ???"
            print "  ?"
            print
            print "No information available on message"
        elif id == '14':
            print "Message 14: Device status"
            print " ?"
            print
            print "Arguments: <status><temperature><waterHighbits><waterLowbits><unknown>"
            self.calibration()
            
            #FIX
        
        #    1	0x00	Device Status. 0=Ready. 1=Boiling. 2=Keep warm. 3=Cycle finished. 4=Baby cooling.
        #    2	0x28	Temperature in Celsius. 0x7f = Not on base.
        #    3	0x07	Water level (high bits), see below.
        #    4	0xf7	Water level (low bits), see below.
        #    5	0x00	Unknown, possibly reserved. Only seen 0x00 on the iKettle 2.0
        
        elif id == '15':
            print "Message 15: Turn On"
            print "  ?"
            print
            print "Argument: <temperature>"
            print
            print "Example raw code: 15 ?? 7e"
        elif id == '16':
            print "Message 16: Turn Off"
            print "  ♨ iKettle 2.0"
            print
            print "Example raw code: 16 7e"
        elif id == '19':
            print "Message 19: ???"
            print "  ♨ iKettle 2.0"
            print
            print "Example raw code: 19 7e"
        elif id == '20':
            print "Message 20: Turn On"
            print "  ♨ iKettle 2.0"
            print
            print "Example raw code: 20 7e"
        elif id == '21':
            print "Message 21: Turn On"
            print "  ♨ iKettle 2.0"
            print
            print "Arguments: <[<temperature><[time]>]>"
            print
            print "Keep Warm between 5 and 20 minutes, 0 for normal on"
            print
            print "Example raw code: 21 7e"
            print "                  21 50 00 7e"
            print "                  21 30 05 7e"
            print "                  21 44 7e"
        elif id == '22':
            print "Message 22: Turn On"
            print "  ♨ iKettle 2.0"
            print
            print "Example raw code: 22 7e"
        elif id == '23':
            print "Message 23: Turn On"
            print "  ♨ iKettle 2.0"
            print
            print "Example raw code: 23 7e"
        elif id == '28':
            print "Message 28: ???"
            print "  ♨ iKettle 2.0"
            print
            print "No information available on message"
        elif id == '29':
            print "Message 29: Reply on 28???"
            print "  ♨ iKettle 2.0"
            print
            print "29 00 7e"
            print "29 08 01 5f .. .. xx 7e"
            print "29 01 01 5f 00 00 10 00 19 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e"
            print
            print "No information available on message"
        elif id == '2a':
            print "Message 2a: ???"
            print "  ♨ iKettle 2.0"
            print
            print "No information available on message"
        elif id == '2c':
            print "Message 2c: Calibrate Water Sensor"
            print "  ♨ iKettle 2 Only"
            print
            print "Example raw code: 2c 7e"
            self.calibration()
        elif id == '2d':
            print "Message 2c: Calibrate finished"
            print "  ♨ iKettle 2 Only"
            print
            print "Arguments: <unkownArgument><unkownArgument>"
            print
            print "Example raw code: 2c ?? ?? 7e"
            self.calibration()
        elif id == '3c':
            print "Message 3c: Toggle the Grinder on/off"
            print "  ☕ Smarter Coffee Only"
            print
            print "Example raw code: 3c 7e"
        elif id == '30':
            print "Message 30: ???"
            print "  ?"
            print
        elif id == '35':
            print "Message 35: Set strength of the coffee to brew"
            print "  ☕ Smarter Coffee Only"
            print
            print "Argument: <strength>"
            print
            print "strength:"
            print "00 Weak"
            print "01 Medium"
            print "02 Strong"
            print
            print "Example code: 35 01 7e"
            self.coffeebrewing()
        elif id == '36':
            print "Message 36: Set number of cups to brew"
            print "  ☕ Smarter Coffee Only"
            print
            print "Argument: <numberOfCups>"
            print "Note: numberOfCups must be between 1 and 12"
            print
            print "Example code: 36 03 7e"
            self.coffeeBrewing()
        elif id == '37':
            print "Message 37: ???"
            print "  ☕ Smarter Coffee Only"
            print
            print "No information available on message"
        elif id == '3c':
            print "Message 3c: Toggle the Grinder on/off"
            print "  ☕ Smarter Coffee Only"
            print
            print "Example raw code: 3c 7e"
        elif id == '3e':
            print "Message 3e: Turn on the hotplate"
            print "  ☕ Smarter Coffee Only"
            print
            print "Argument: <numberOfMinutes>"
            print "Note: It is hardcoded in app with 5"
            print "      valid values are 0 to 30???"
            print
            print "unknownArgument:"
            print "05 Default"
            print
            print "Example raw code: 3e 05 7e"
        elif id == '40':
            print "Message 40: Updating schedules ???"
            print "  ☕ Smarter Coffee Only"
            print
            print "No information available on message"
        elif id == '41':
            print "Message 41: Requesting schedules ???"
            print "  ☕ Smarter Coffee Only"
            print
            print "No information available on message"
        elif id == '43':
            print "Message 43: schedules ???"
            print "  ☕ Smarter Coffee Only"
            print
            print "No information available on message"
        elif id == '4a':
            print "Message 4a: Turn off the hotplate"
            print "  ☕ Smarter Coffee Only"
            print
            print "Example raw code: 4a 7e"
        elif id == '64':
            print "Message 64: Identify Device"
            print "  ♨ iKettle 2.0 & ☕ Smarter Coffee"
            print
            print "Note: Is used for auto discovery over UDP broadcast (after device setup is complete)"
            print "      This fails on some/most routers, which don't propagate UDP broadcasts"
            print
            print "Example raw code: 64 7e"
        elif id == '65':
            print "Message 65: Response Identify Device"
            print "  ♨ iKettle 2.0 & ☕ Smarter Coffee"
            print
            print "Arguments: <deviceType> <sdkVersion>"
            print
            print "deviceType:"
            print "01 iKettle 2.0"
            print "02 iSmarter Coffee"
            print
            print "sdkVersion:"
            print "13 Firmware v19 (?)"
            print
            print "Example raw code: 65 01 13 7e"
        elif id == 69:
            print "Message 69: ???"
            print "  ♨ iKettle 2.0"
            print
            print "returns with 0 arguments 03 04 7e"
            print "returns with 1 argument 03 00 7e"
        elif id == '6a':
            print "Message 6a: Get firmware version of WiFi module"
            print "  ♨ iKettle 2.0"
            print
            print "Example raw code: 6a 7e"
            self.wifi()
        elif id == '6b':
            print "Message 6b: Firmware version of WiFi module"
            print "  ♨ iKettle 2.0"
            print
            print "Note: iKettle 2.0 returns:"
            print "      AT+GMRAT version:0.40.0.0(Aug  8 2015 14:45:58)SDK version:1.3.0compile time:Aug  8 2015 17:19:38OK"
            self.wifi()
        elif id == '6d':
            print "Message 6d: Firmware Update"
            print "  ?"
            print
            print "Note: Disables wifi and creates a 'iKettle Update' network"
            print "      a hard device reset (hold power button for 10 seconds) required to fix"
            print " opens up a port at 6000"
            print
            print "Example raw code: 6d 7e"
        else:
            print 'No information available on message ID: ', id
        print

    def all(self):
        self.base()
        self.messages()
        self.message("02")
        self.message("03")
        self.message("05")
        self.message("07")
        self.message("0c")
        self.message("0d")
        self.message("0e")
        self.message("0f")
        self.message("10")
        self.message("13")
        self.message("14")
        self.message("15")
        self.message("16")
        self.message("19")
        self.message("21")
        self.message("20")
        self.message("22")
        self.message("23")
        self.message("28")
        self.message("29")
        self.message("2a")
        self.message("2b")
        self.message("2c")
        self.message("2d")
        self.message("30")
        self.message("32")
        self.message("35")
        self.message("36")
        self.message("37")
        self.message("3c")
        self.message("3e")
        self.message("40")
        self.message("41")
        self.message("43")
        self.message("4a")
        self.message("64")
        self.message("65")
        self.message("69")
        self.message("6a")
        self.message("6b")
        self.message("6d")
