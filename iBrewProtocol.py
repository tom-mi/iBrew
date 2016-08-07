# -*- coding: utf8 -*-

import struct

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

iBrewVersion = "White Tea Edition v0.07 © 2016 TRiXWooD"

# protocol information

iBrewMessageWorking = [[0,"? iKettle 2.0  ? SmarterCoffee"],
                       [1,"✓ iKettle 2.0  ✕ SmarterCoffee"],
                       [2,"✕ iKettle 2.0  ✓ SmarterCoffee"],
                       [3,"✓ iKettle 2.0  ✓ SmarterCoffee"],
                       [4,"✓ iKettle 2.0  ? SmarterCoffee"],
                       [5,"? iKettle 2.0  ✓ SmarterCoffee"],
                       [6,"✕ iKettle 2.0  ✕ SmarterCoffee"],
                       [7,"✕ iKettle 2.0  ? SmarterCoffee"],
                       [8,"? iKettle 2.0  ✕ SmarterCoffee"],
                      ]

iBrewMessageWorkingIcon = [[0,"? ?"],
                           [1,"✓ ✕"],
                           [2,"✕ ✓"],
                           [3,"✓ ✓"],
                           [4,"✓ ?"],
                           [5,"? ✓"],
                           [6,"✕ ✕"],
                           [7,"✕ ?"],
                           [8,"? ✕"],
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
                 [0x15,0x00,False,4,"Turn on"],
                 [0x16,0x00,False,4,"Turn off"],
                 [0x19,0x00,False,4,"Working unknown command"],
                 [0x20,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x21,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x22,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x23,0x00,False,4,"Working unknown command (turn on?)"],
                 [0x28,0x29,False,4,"Working unknown command"],
                 [0x29,0xff,True ,4,"Working unknown reply"],
                 [0x2a,0x00,False,4,"Working unknown command"],
                 [0x2b,0x2d,False,4,"Get watersensor base value"],
                 [0x2c,0x2d,False,4,"Calibrate watersensor"],
                 [0x2d,0xff,True ,4,"Watersensor base value"],
                 [0x30,0x00,False,4,"Working unknown command"],
                 [0x32,0x00,False,2,"Working unknown command"],
                 [0x33,0x00,False,2,"Start coffee brewing"],
                 [0x35,0x00,False,2,"Set strength of the coffee to brew"],
                 [0x36,0x00,False,2,"Set number of cups to brew"],
                 [0x37,0x00,False,2,"Start coffee brewing using default"],
                 [0x3c,0x00,False,2,"Toggle grinder"],
                 [0x3e,0x00,False,2,"Turn on hotplate"],
                 [0x40,0x00,False,2,"Working unknown command"],
                 [0x41,0x00,False,2,"Working unknown command"],
                 [0x43,0x00,False,2,"Working unknown command"],
                 [0x4a,0x00,False,2,"Turn off hotplate"],
                 [0x64,0x65,False,3,"Get identify of device"],
                 [0x65,0xff,True ,3,"Identify of device"],
                 [0x69,0x00,False,4,"Working unknown command"],
                 [0x6a,0x6b,False,4,"Get WiFi firmware info"],
                 [0x6b,0xff,True ,4,"WiFi firmware info"],
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

def iBrew_raw_to_hex(data):
    h = hex(data)[2:4]
    if data < 0x10:
        return '0' + h
    return h

def iBrew_message(id):
    for i in range(0,len(iBrewMessages)):
        if iBrewMessages[i][0] == int(id,16):
            return iBrewMessages[i]
    return [0x00,0x00,False,6,""]

def iBrew_message_description(id):
    return iBrew_message(id)[4]

def iBrew_message_command(id):
    print iBrew_message(id)[0]
    return iBrew_message(id)[0]

def iBrew_message_type(id):
    return iBrewMessageType[iBrew_message(id)[2]][1]

def iBrew_message_response_code(id):
    return iBrew_message(id)[1]

def iBrew_message_response(id):
    d = iBrew_message_response_code(id)
    if (d == 0xff or d == 0x00):
        return ""
    else:
        return iBrew_raw_to_hex(d)

def iBrew_message_command_code(id):
    m = []
    for i in range(0,len(iBrewMessages)):
        if iBrewMessages[i][1] == int(id,16):
            m = m + [iBrewMessages[i][0]]
    return m

def iBrew_message_device(id):
    return iBrewMessageWorking[iBrew_message(id)[3]][1]

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
iBrewOffBase = 0x7f
    
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

    def structure(self):
        print
        print "  Smarter iKettle 2.0 & Smarter Coffee Protocol Structure"
        print "  _______________________________________________________"
        print
        print "  Smarter uses a binary message protocol,"
        print "  either via UDP or TCP on port 2081"
        print
        print "  Messages (commands and responses) use the syntax:"
        print
        print "    <ID>[ARGUMENTS]<TAIL>"
        print
        print "  The tail is always 7e or ~ in ASCII"
        print
        print "  Arguments use this syntax:"
        print
        print "    <ARGUMENT>   is a single mandatory byte"
        print "    <[ARGUMENT]> is a single optional byte"
        print "    <ARGUMENT>{0,32} is mandatory, between 0 and 32 bytes"
        print
        print "  Everything else, including spurious } characters, are ASCII literals"
        print
        print "  Is connected locally it will send a command response message"
        print "  as reply to a command before any other response message"
        print
    
    def messages_short(self,messageType):
        for i in range(0,len(iBrewMessages)):
            if messageType == iBrewMessages[i][2]:
                print "  " + iBrewMessageWorkingIcon[iBrewMessages[i][3]][1] + " " + iBrew_raw_to_hex(iBrewMessages[i][0]) + " " + iBrewMessages[i][4]

    def messages(self):
        print
        print "  k c ID Command Message"
        print "  ___________________________________________"
        self.messages_short(False)
        print
        print "  k c ID Response Message"
        print "  _______________________________"
        self.messages_short(True)
        print
        print "  Legend:"
        print "    k iKettle 2"
        print "    c Smarter Coffee"
        print

    def calibration(self):
        print
        print "  Calibration:"
        print
        print "      If the kettle is on the base during calibration, the numbers change to be higher,"
        print "      but the differences between levels seem the same. This means that the water level"
        print "      detection is probably weight based and that calibration is done at the base,"
        print "      which then remembers the weight for \'off base\'. To detect an empty kettle,"
        print "      the connecting device must account for the weight of the kettle itself."

    def wifi(self):
        print
        print "  WiFi:"
        print
        print "      If the device is configured to access an WiFi access point which is not available"
        print "      It will try to connect to it every so minutes. If it tries to connect it beeps three"
        print "      times the WiFi access point of the device will remain active but unreachable,"
        print "      if it fails to access the access point it beeps once, and it opens up its own default"
        print "      open unencrypted WiFi access point"

    def coffeeBrewing(self):
        print
        print "  Coffee Brewing:"
        print
        print "      Between setting the number of cups, the strength of the coffee and start of brewing"
        print "      atleast 500ms is recommended."

    def message(self,id):
        print
        print "  "+ iBrew_message_type(id) + " Message: " + str(id) + " " + iBrew_message_description(id)
        print "  ─────────────────────────────────────────────────────────────────────────"
        print "  " + iBrew_message_device(id)
        print
        s = iBrew_message_response(id)
        if s != "":
            print "  Response Message: " + s  + " " + iBrew_message_description(s)
            print

        s = iBrew_message_command_code(id)
        
        if s != []:
            m = iBrew_raw_to_hex(s[0])
            print "  Command Message: " + m + " " + iBrew_message_description(m)
            for i in range(1,len(s)):
                m = iBrew_raw_to_hex(s[i])
                print "                   " + m + " " + iBrew_message_description(m)
            print


        if id == '02':
            print "  Arguments: <Seconds><Minutes><Hours><Unknown><Day><Month><Century><Year>"
            print "  Note: Unknown is Day of week index?"
        elif id == '03':
            #Fix
            print "d"
        elif id == '05':
            print "  Argument: <SSID>{0,32}"
            print "  Note: SSID is between 0 and 32 characters"
            self.wifi()
        elif id == '07':
            print "  Argument: <password>{0,32}"
            print "  Note: password is between 0 and 32 characters"
            print
            print "  Message 07: Start brewing Coffee???"
            print " ?"
            self.wifi()
        elif id == '0c':
            print "  No information available on message"
            self.wifi()
        elif id == '0d':
            print "  Example raw code: 0d 7e"
            self.wifi()
        elif id == '0e':
            print "  Arguments: <SSID>{0,32},-<db>{2}}"
            print "  Note: SSID is between 0 and 32 characters"
            print "        Sending message 0c without previous SSID/password messages will reset WiFi to factory settings"
            print "        -db is the signal strength in dBm format"
            print
            print "  Examples: MyWifi,-56}"
            print "            MyWifi,-56}OtherWifi,-82}"
            self.wifi()
        elif id == '0f':
            print "  Returns: Message 0f"
            print
            print "  Example raw code: 0f 7e"
        elif id == '10':
            print "  No information available on message"
        elif id == '14':
            print "  Arguments: <status><temperature><waterHighbits><waterLowbits><unknown>"
            self.calibration()
            
            #FIX
        
        #    1	0x00	Device Status. 0=Ready. 1=Boiling. 2=Keep warm. 3=Cycle finished. 4=Baby cooling.
        #    2	0x28	Temperature in Celsius. 0x7f = Not on base.
        #    3	0x07	Water level (high bits), see below.
        #    4	0xf7	Water level (low bits), see below.
        #    5	0x00	Unknown, possibly reserved. Only seen 0x00 on the iKettle 2.0
        
        elif id == '15':
            print "  Argument: <temperature>"
            print
            print "  Example raw code: 15 ?? 7e"
        elif id == '16':
            print "  Example raw code: 16 7e"
        elif id == '19':
            print "  Example raw code: 19 7e"
        elif id == '20':
            print "  Example raw code: 20 7e"
        elif id == '21':
            print "  Arguments: <[<temperature><[time]>]>"
            print
            print "  Keep Warm between 5 and 20 minutes, 0 for normal on"
            print
            print "  Example raw code: 21 7e"
            print "                  21 50 00 7e"
            print "                  21 30 05 7e"
            print "                  21 44 7e"
        elif id == '22':
            print "  Example raw code: 22 7e"
        elif id == '23':
            print "  Example raw code: 23 7e"
        elif id == '28':
            print "  No information available on message"
        elif id == '29':
            print "  29 00 7e"
            print "  29 08 01 5f .. .. xx 7e"
            print "  29 01 01 5f 00 00 10 00 19 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e"
            print
            print "  No information available on message"
        elif id == '2a':
            print "  No information available on message"
        elif id == '2c':
            print "  Example raw code: 2c 7e"
            self.calibration()
        elif id == '2d':
            print "  Arguments: <unkownArgument><unkownArgument>"
            print
            print "  Example raw code: 2c ?? ?? 7e"
            self.calibration()
        elif id == '3c':
            print "  Example raw code: 3c 7e"
        elif id == '30':
            print
        elif id == '35':
            print "  Argument: <strength>"
            print
            print "  strength:"
            print "  00 Weak"
            print "  01 Medium"
            print "  02 Strong"
            print
            print "  Example code: 35 01 7e"
            self.coffeeBrewing()
        elif id == '36':
            print "  Argument: <numberOfCups>"
            print "  Note: numberOfCups must be between 1 and 12"
            print
            print "  Example code: 36 03 7e"
            self.coffeeBrewing()
        elif id == '37':
            print "  No information available on message"
        elif id == '3c':
            print "  Example raw code: 3c 7e"
        elif id == '3e':
            print "  Argument: <numberOfMinutes>"
            print "  Note: valid values are 5 to 30 (30 not sure)"
            print
            print "  unknownArgument:"
            print "  05 Default"
            print
            print "  Example raw code: 3e 05 7e"
        elif id == '40':
            print "  Message 40: Updating schedules ???"
            print "  No information available on message"
        elif id == '41':
            print "  Message 41: Requesting schedules ???"
            print "  No information available on message"
        elif id == '43':
            print "  Message 43: schedules ???"
            print "  No information available on message"
        elif id == '4a':
            print "  Example raw code: 4a 7e"
        elif id == '64':
            print "  Note: Is used for auto discovery over UDP broadcast (after device setup is complete)"
            print "        This fails on some/most routers, which don't propagate UDP broadcasts"
            print
            print "  Example raw code: 64 7e"
        elif id == '65':
            print "  Arguments: <deviceType> <sdkVersion>"
            print
            print "  deviceType:"
            print "  01 iKettle 2.0"
            print "  02 iSmarter Coffee"
            print
            print "  sdkVersion:"
            print "  13 Firmware v19 (?)"
            print
            print "  Example raw code: 65 01 13 7e"
        elif id == '69':
            print "  returns with 0 arguments 03 04 7e"
            print "  returns with 1+ argument 03 00 7e"
        elif id == '6a':
            print "  Example raw code: 6a 7e"
            self.wifi()
        elif id == '6b':
            print "  Note: iKettle 2.0 returns:"
            print "        AT+GMRAT version:0.40.0.0(Aug  8 2015 14:45:58)SDK version:1.3.0compile time:Aug  8 2015 17:19:38OK"
            self.wifi()
        elif id == '6d':
            print "  Note: Disables wifi and creates a 'iKettle Update' network"
            print "        a hard device reset (hold power button for 10 seconds) required to fix"
            print "        opens up a port at 6000"
            print
            print "  Example raw code: 6d 7e"
        else:
            print "  No information available on message " + id
        print

    def all(self):
        self.structure()
        self.messages()
        for i in range(0,len(iBrewMessages)):
            self.message(iBrew_raw_to_hex(iBrewMessages[i][0]))


