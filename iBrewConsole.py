# -*- coding: utf8 -*

import sys
from iBrewProtocol import *
from iBrewClient import *

#------------------------------------------------------
# iBrew CONSOLE
#
# Console for iKettle 2.0 or Smarter Coffee Devices
#
# Note that the device status is the only message not
# printed in raw format...
#------------------------------------------------------

class iBrewConsole:

    def introduction(self):
        print
        print "For list of commands type: help and press enter"
        print "Press enter for status update and press ctrl-c to quit"
        print
    
    def help(self):
        print
        print "  [data]           Send raw data to device"
        print "  cups [nr]        ☕ Set number of cups"
        print "  calibrate        ♨ Calibrates waterlevel"
        print "  calibrate base   ♨ Show calibrates waterlevel base value"
        print "  examples         Show examples of commands"
        print "  grinder          ☕ Toggle grinder"
        print "  help             This help"
        print "  hotplate off     ☕ Turn hotplate off"
        print "  hotplate on      ☕ Turn hotplate on"
        print "  info             Device info"
        print "  joke             Show joke"
        print "  messages         List all protocol messages"
        print "  message [id]     List protocol messages detail"
        print "  off              Turn off"
        print "  on               Turn on"
        print "  protocol         Print protocol structure"
        print "  quit             Quit console"
        print "  status           Show status"
        print "  strength [s]     ☕ Set strength coffee (weak, medium or strong)"
        print
        print "  ☕ Smarter Coffee Only"
        print "  ♨ iKettle 2.0 Only"
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

    def joke(self):
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
                
        coffeeJokes =  [["Why are men are like coffee?"," The best ones are rich, hot, and can keep you up all night!"],
                        ["Why is a bad cup of coffee the end of a marriage?","Because it's GROUNDS for divorce!"],
                        ["What do you call sad coffee?","Despresso"],
                        ["Did you know it's a sin for a woman to make coffee?","In the bible it says He-brews"],
                        ["Why Coffee is better than a Woman?","Coffee goes down easier!"],
                        ["They call me \"coffee\"","Cause I grind so fine."],
                        ["Hold the sugar please","You're sweet enough for the both of us"],
                        ["So I've Been thinking about you a latte","Your coffee grinder"],
                        ["How do you look so good before coffee?","Your coffee machine"],
                       ]
        joke = random.choice(teaJokes+coffeeJokes)
        print "\n      \'" + joke[0] + "\'\n                  -- " + joke[1] + "\n"

    def __init__(self,host):
        client = iBrewClient(host)
        client.print_connect_status()
        client.print_status()
        self.joke()
        client.log = True
        self.introduction()
        cursor = client.host + ":" + client.device + "$"
        lastreply = ""
        while True:
            try:
                input = raw_input(cursor).lower()
                if input == "on":
                    client.on()
                elif input == "off":
                    client.off()
                elif input == "hotplate on":
                    # FIX THIS
                    client.hotplate_on()
                elif input == "hotplate off":
                    client.hotplate_off()
                elif input == "grinder":
                    client.grinder()
                elif input[0:9] == "strength ":
                    if input[9:14] == "weak":
                        client.coffee_strength("weak")
                    if input[9:16] == "strong":
                        client.coffee_strength("strong")
                    if input[9:16] == "medium":
                        client.coffee_strength("medium")
                elif input[0:5] == "cups ":
                    # FIX THIS
                    client.cups(3)
                elif input == "exit" or input =="quit":
                    sys.exit()
                elif input == "joke":
                    print
                    self.joke()
                    print
                elif input == "help":
                    self.help()
                elif input == "info":
                    client.info()
                elif input == "calibrate":
                    client.calibrate()
                elif input == "calibrate base":
                    client.calibrate_base()
                    # fix print
                elif input == "examples":
                    self.examples()
                elif input == "protocol":
                    iBrewProtocol().structure()
                elif input == "messages":
                    iBrewProtocol().messages()
                elif input[0:8] == "message ":
                    iBrewProtocol().message(input[8:11])
                elif len(input) > 0 and input != "status":
                    client.send(client.string_to_message(str(input)))
                client.read()
                if input == "status":
                    client.print_status()
                else:
                    client.print_short_status()
            except:
                print
                break