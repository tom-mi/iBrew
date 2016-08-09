# -*- coding: utf8 -*

import sys
import random

from iBrewProtocol import *
from iBrewInterface import *

#------------------------------------------------------
# iBrew VERSION INFORMATION
#------------------------------------------------------

iBrewApp = "iBrew: iKettle 2.0 & Smarter Coffee Interface"
iBrewVersion1 = "\'Bean Grinder\' v0.03 © 2016 Tristan Crispijn"
iBrewVersion2 = "White Tea Leaf Edition v0.10 © 2016 Tristan Crispijn"
iBrewVersion3 = "Tea Noir Suite v0.30 © 201x Tristan Crispijn"
iBrewVersion  = "White Tea Leaf Edition v0.10 © 2016 Tristan (@monkeycat.nl)"
iBrewDonate   = "Please donate (for) a (working) Smarter Coffee (interface)"

# ??? conversion hell
#int = int(hexstring,16)
#hexstring = print " " + hex(12)[2:4] if 12 < 16 else hex(int)[2:4]

class iBrewConsole:

    #------------------------------------------------------
    # iBrew MONITOR
    #------------------------------------------------------

    def monitor(self):
        print "iBrew: Press ctrl-c to stop"
        lastResponse = ""
        while True:
            try:
                response = self.client.read()
                if lastResponse == response:
                    pass
                else:
                    lastResponse = response
                    self.client.print_short_status()
            except:
                break
    #------------------------------------------------------
    # iBrew SWEEP
    #------------------------------------------------------

    def sweep(self,start=1):
        if int(start) <= 0 or start > 256:
            print 'iBrew: sweep start out of range [00..ff]'
            return
        print "iBrew: Press ctrl-c to stop"
 
        dump = self.client.dump
        self.client.dump = True

        for i in range(int(start),256):
            try:
                # known command/message?
                m = iBrew_message_o(hex(i))
                
                # know command for other device except itself?
                if m == 0 or (self.client.isKettle2 and not iBrew_message_kettle(hex(i))) or (self.client.isSmarterCoffee and not iBrew_message_kettle(hex(i))):
                
                    # add zero here...
                    print "iBrew: Testing Command: " + iBrew_raw_to_hex(i)

                    # button pressed quit...
                    x = self.client.send(struct.pack('B',i))
                    if self.client.statusCommand != 0x69:
                        print "iBrew: New Command Found: " + hex(i)[2:4]
                    self.client.dump = False
                    self.client.stop()
                    self.client.dump = True
            except:
                break;
        self.client.dump = dump

    #------------------------------------------------------
    # iBrew Console MAIN LOOP
    #------------------------------------------------------

    def __init__(self,host,command=""):
        client = iBrewClient(host)
        self.client = client
        client.print_connect_status()
        client.print_status()
        
        if command == "":
            self.app_info()
            self.joke()
            self.intro()
            
        cursor = client.host + ":" + client.device + "$"
        lastreply = ""
        client.dump = True
        loop = True
        while loop:
            try:
                # are we command line or console?
                if (command==""):
                    input = raw_input(cursor).lower().strip()
                else:
                    input = command.lower().strip()
                    loop = False
                    
                # iKettle 2.0 Commands
                
                if input == "heat":
                    #"fix me"
                    client.heat()
                elif input == "formula":
                    #"fixme"
                    client.formula()
                elif input == "default":
                    client.store_settings()
                elif input[0:8] == "default ":
                    pass
                    """
                    # decode temp
                    t
                    # decode ...
                    w
                    # decode ...
                    f
                    # decmode ...
                    ft
                    client.default(t,w,f,ft)
                    
                    FIX ME
                    """
                elif input == "calibrate" or input == "watersensor calibrate":
                    client.calibrate()
                elif input == "watersensor base" or input == "base" :
                    client.calibrate_base()
                    client.print_watersensor_base()
                elif input[0:11] == "store base ":
                 # or input[0:23] == "watersensor store base ":
                    client.store_calibrate_base(int(input[11:15]))

                # WiFi Commands
                
                elif input == "wifi firmware" or input == "firmware":
                    client.wifi_firmware()
                elif input == "wifi reset" or input == "reset":
                    client.wifi_reset()
                elif input == "wifi connect" or input == "connect":
                    client.wifi_connect()
                elif input == "wifi scan" or input == "scan wifi" or input == "scan":
                    client.wifi_scan()
                elif input[0:13] == "wifi password":
                    client.wifi_password(str(input[13:len(input)]))
                elif input[0:9] == "password ":
                    client.wifi_password(str(input[9:len(input)]))
                elif input[0:10] == "wifi name ":
                    client.wifi_name(str(input[10:len(input)]))
                elif input[0:5] == "name ":
                    client.wifi_name(str(input[5:len(input)]))
                elif input == "wifi setup" or input == "setup":
                    print "iBrew: Not Fully Implemented"
                
                # Smarter Commands
                
                # Hotplate
                elif input[0:11] == "hotplate on":
                    print "iBrew: Not Fully Implemented"
                    # FIX THIS
                    client.hotplate_on()
                elif input == "hotplate off":
                    client.hotplate_off()
                elif input[0:8] == "hotplate":
                    print "iBrew: Use on or off as argument"
                
                # Grinder
                elif input == "grinder":
                    client.grinder()

                # Brew
                elif input == "brew":
                    client.brew()
                
                # Strength
                elif input[0:9] == "strength ":
                    if input[9:14] == "weak":
                        client.coffee_strength("weak")
                    elif input[9:16] == "strong":
                        client.coffee_strength("strong")
                    elif input[9:16] == "medium" or input[9:16] == "normal":
                        client.coffee_strength("medium")
                    else:
                        print "iBrew: Use weak, medium or strong as argument"
                elif input[0:8] == "strength":
                    print "iBrew: Use weak, medium or strong as argument"

                # Cups
                elif input[0:5] == "cups ":
                    try:
                        x = int(input[5:len(input)])
                        if x < 0 or x > 12:
                            raise ValueError('Conversion Error')
                    except:
                        print "iBrew: Use 1..12 as range in argument cups"
                        continue
                    client.coffee_cups(x)
                elif input[0:4] == "cups":
                    print "iBrew: Use 1..12 as range in argument cups"
        
                # Console Commands
                elif input == "exit" or input == "quit":
                    break
                elif input == "monitor":
                    self.monitor()
                elif input == "sweep":
                    self.sweep()
                elif input[0:6] == "sweep ":
                    try:
                        x = int(input[6:8],16)
                        if x < 0 or x > 255:
                            raise ValueError('Conversion Error')
                    except:
                        print "iBrew: Invalid Start Command"
                        continue
                    self.sweep(x)
                elif input == "joke" or input == "quote":
                    print
                    self.joke()
                    print
                elif input == "help" or input == "?":
                    self.help()
                elif input == "smarter":    
                    iBrewProtocol().security()
                    iBrewProtocol().wireshark()
                    iBrewProtocol().structure()
                    iBrewProtocol().messages()
                    iBrewProtocol().messages_all()
                    return
                elif input == "dump" or input == "raw" or input == "messages dump" or input == "messages raw":
                    if client.dump:
                        client.dump = False
                        print "iBrew: Dump raw messages disabled"
                    else:
                        client.dump = True
                        print "iBrew: Dump raw messages enabled"
                elif input == "examples" or input ==  "help examples":
                    self.examples()
                elif input == "protocol" or input == "help protocol" :
                    iBrewProtocol().structure()
                elif input == "messages" or input == "help messages":
                    iBrewProtocol().messages()
                elif input[0:8] == "message ":
                    iBrewProtocol().message(input[8:11])
                elif input[0:13] == "help message ":
                    iBrewProtocol().message(input[13:16])

                # iKettle 2.0 & Smarter Coffee Commands
                elif input == "on" or input == "start"  :
                    if client.isKettle2:
                        client.heat()
                    elif client.isSmarterCoffee:
                        client.brew()
                elif input == "stop" or input == "off":
                    client.stop()
                elif input == "info":
                    client.info()
                    client.print_info()
                elif len(input) > 0 and input != "status":
                    client.send(client.string_to_message(str(input)))
                client.read()
                if input == "status":
                    client.print_status()
                else:
                    client.print_short_status()
            except:
                break
        print

#------------------------------------------------------
# iBrew Console PRINT
#------------------------------------------------------
    def app_info(self):
        print iBrewApp
        print iBrewVersion
        print
        print iBrewDonate
        print

    def intro(self):
        print
        print "For list of commands type: help and press enter"
        print "Press enter for status update and press ctrl-c to quit"
        print

    def intro_cl(self):
        print
        print "Usage: iBrew [arguments] (host)"
        print

    def help(self):
        print
        print "  iKettle 2.0 & Smarter Coffee Commands"
        print "  info                   Device info"
        print "  start                  Start the device"
        print "  status                 Show status"
        print "  stop                   Stop the device"
        print "  [data]                 Send raw data to device"
        print
        print "  iKettle 2.0 Commands"
        print "  base                   Show watersensor base value"
        print "  calibrate              Calibrates watersensor"
        print "  default                Set default settings"
        print "  formula ()()           Heat kettle in formula mode"
        print "  heat ()()              Heat kettle"
        print "  settings               Set user settings"
        print "  store base [base]      Store watersensor base value"
        print
        print "  Smarter Coffee Commands"
        print "  brew                   Brew coffee"
        print "  cups [number]          Set number of cups [1..12]"
        print "  grinder                Toggle grinder"
        print "  hotplate off           Turn hotplate off"
        print "  hotplate on            Turn hotplate on"
        print "  strength [strength]    Set strength coffee [weak, medium or strong]"
        print
        print "  WiFi Commands"
        print "  connect                Connect to wireless network"
        print "  firmware               Show firmware WiFi"
        print "  name [name]            Set wireless network name to access"
        print "  password [password]    Set password of wireless network to access"
        print "  reset                  Reset WiFi"
        print "  scan                   Scan wireless networks"
#        print "  setup                  Select and connect wireless network"
        print
        print "  Help Commands"
        print "  examples               Show examples of commands"
        print "  messages               Show all known protocol messages"
        print "  message [id]           Show protocol message detail"
        print "  protocol               Show protocol structure"
        print "  smarter                Show protocol"
        print
        print "  Debug Commands"
        print "  dump                   Toggle \'dump raw messages\'"
        print "  monitor                Monitor incomming traffic"
        print "  sweep [startcommand]   Try (all) unknown command codes"
        print
        print "  Console Commands"
        print "  joke                   Show joke"
        print "  quit                   Quit console"
        print

    def examples(self):
        print
        print "Example:"
        print "  off            iKettle 2.0 Stop boiling"
        print "  messages       Show all protocol messages"
        print "  message 3e     Show protocol message 3a, turn hotplate on"
        print "  167E           Send iKettle 2.0 raw off"
        print "  21 30 05 7e    Send iKettle 2.0 raw on"
        print "  strength weak  Set SmarterCoffee coffee strength to weak"
        print "  cups 3         Set SmarterCoffee number of cups to brew"
        print

    teaJokes = [["What do you call a talkative drink?","Chai tea."],
                ["How long does it take to brew Chinese tea?","Oolong time."],
                ["When shouldn't you drink a hot beverage?","If it's not your cup of tea."],
                ["How does Moses make his tea?","Hebrews it."],
                ["What drink do goalies hate?","Penal-tea."],
                ["How do you ask a dinosaur to lunch?","Tea Rex?"],
                ["What does a worry wart drink?","Safe-Tea."],
                ["Why did the hipster burn his tongue?","Because he drank his tea before it was cool."],
                ["What drink brings you down to earth?","Gravi-Tea."],
                ["What do sophisticated fish drink?","Salt-Tea."],
                ["Why did the tea bag have to do it's laundry?","Because it was stained."],
                ["What kind of music do teapots like?","Jasmine."],
                ["Why must you be careful of tea at night?","Because it might mug you."],
                ["What does a tea bag do when it's tired?","It seeps."],
                ["Why did the teapot get in trouble?","Because he was naughtea."],
                ["What did the teapot wear to bed?","A nightea"],
                ["What happens when an old teapot laughs too hard?","It teas its pants."],
                ["It is time to get this par tea started!","Right?"],
                ["Hello Brew-TEA-Full!!!","Your kettle"],
                ["I love to drink tea each day","It brings out my inner tranquili-Tea"],
                ["Today!","Full of creativi-Tea"],
                ["It tends to break the ice very easily","Flirt-Tea."],
                ["When your kettle is too","Chat-Tea"],
                ["Where there is tea","There is hope!"],
                ["If tea is the drink of love","Then brew on!"],
                ["It really is a serious problem","If tea can’t fix it."],
                ]
    
    coffeeJokes =  [["Why is a bad cup of coffee the end of a marriage?","Because it's GROUNDS for divorce!"],
                ["What do you call sad coffee?","Despresso"],
                ["Did you know it's a sin for a woman to make coffee?","In the bible it says He-brews"],
                ["Why Coffee is better than a Woman?","Coffee goes down easier!"],
                ["They call me \"coffee\"","Cause I grind so fine."],
                ["Hold the sugar please","You're sweet enough for the both of us"],
                ["So I've Been thinking about you a latte","Your coffee grinder"],
                ["How do you look so good before coffee?","Your coffee machine"],
                ["Why are men are like coffee?"," The best ones are rich, hot, and can keep you up all night!"],
        ]

    def joke(self):
        joke = random.choice(self.teaJokes+self.coffeeJokes)
        print "\n      \'" + joke[0] + "\'\n                  -- " + joke[1] + "\n"

