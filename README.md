# iBrew Tea Noire Sweet
[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface

## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface and bridge to [Domoticz](http://domoticz.com). You can also use it in your own code. iKettle 2.0 v19 tested only. Please share you Smarter Coffee codes or any other discoveries you made.

This means your machine is free! You can connect it yourself and do whatever you want with it. You are in full control! You can also interface it with your favorite smarthome controller. A working bridge to domoticz is already included (which you can bridge with homekit or other fun stuff)!

   Signed TRiXWooD

#### Versions
 * v0.0 Bean Grinder Pack
 * v0.1 White Tealeaf Edition
 * v0.2 Tea Noire Sweet
 
#### Upcoming   
 * Better error handling
 * Final arguments
 * Auto reconnect
 
 v0.3 Kettle Rattle 
 
#### Donate
Please donate raw codes or donate (for) a (working) Smarter Coffee (interface), can not test without one or without help! Someone please run ```iBrew sweep``` on there coffee machines and post the results in the issues.


#### Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). Donations & other questions <tristan@monkeycat.nl>


## Installation

#### Software Requirements 
* python 2.7

#### Download
You can download and unpack the [source](https://github.com/Tristan79/iBrew/archive/master.zip) or
 download it from github using
```
git clone https://github.com/Tristan79/iBrew.git
```

## Usage

### Command Line Options

See the console section for the commands
 
```

  Usage: iBrew (dump) [command] (host)

    host                   host address (format: ip4, ip6, fqdn)
    dump                   dump message enabled
    command                action to take!


```

### Console
Start the console with the command `iBrew console`. The following commands are available within the console,
you can also use them on the command line as arguments:

```

  iKettle 2.0 & Smarter Coffee Commands
    info                   device info
    history                action history
    list                   list detected devices
    reset                  reset device to default
    start                  start the device
    status                 show status
    stop                   stop the device
    time [time]            set the device time
    [hexdata]              send raw data to device (e.g. '64 7e')

  iKettle 2.0 Commands
    base                   show watersensor base value
    base [base]            store watersensor base value
    calibrate              calibrates watersensor
    default                set default settings
    formula ()()           heat kettle in formula mode
    heat ()()              heat kettle
    settings               show user settings
    settings [] [] [] []   store user settings
    stop kettle            stops boiling

  Smarter Coffee Commands
    brew                   brew coffee
    cups [number]          set number of cups [1..12]
    grinder                toggle grinder
    hotplate off           turn hotplate off
    hotplate on (minutes)  turn hotplate on (time in minutes)
    strength [strength]    set strength coffee [weak, medium or strong]
    stop coffee            stops brewing

  Wireless Network Commands
    join [net] [pass]      connect to wireless network
    leave                  disconnect (and open direct mode)
    scan                   scan wireless networks

  Protocol Help Commands
    examples               show examples of commands
    messages               show all known protocol messages
    message [id]           show protocol message detail of message [id]
    notes                  show developer notes on the devices
    structure              show protocol structure information

  Bridge Commands
    domoticz               show domoticz bridge help

  Debug Commands
    dump                   toggle 'dump raw messages'
    console                start console [Command line only]
    firmware               show firmware Wifi
    monitor                monitor incomming traffic
    protocol               show all protocol information available
    sweep (id)             try (all or start with id) unknown command codes

  Console Commands
    joke                   show joke
    quit                   quit console [Console only]


```

### Examples

```

  Example:
    off            iKettle 2.0 Stop boiling
    messages       Show all protocol messages
    message 3e     Show protocol message 3a, turn hotplate on
    167E           Send iKettle 2.0 raw off
    21 30 05 7e    Send iKettle 2.0 raw on
    strength weak  Set SmarterCoffee coffee strength to weak
    cups 3         Set SmarterCoffee number of cups to brew


```

### Domoticz Bridge

Bridge to [Domoticz](http://domoticz.com). You are in full control!


iKettle Devices in Domoticz
![alt tag](https://raw.githubusercontent.com/Tristan79/iBrew/master/help/Domoticz.png)
   
```


  Domoticz Bridge
  _______________


  Bridge between iKettle 2.0 and domoticz. Its auto-creates 4 devices in domoticz, if not yet created,
  and monitors the kettle and update the domoticz devices accordingly.
  
    Water Temperature in ºC (temperature device)
    Water Height (custom device)
    Kettle on base (motion device)
    Kettle status (text device)
    
  Currently you have to create your boil, brew switches yourself (working on it), so:
  
    Place or link iBrew in your domoticz script folder or somewhere readable and reachable.
    Run iBrew in domoticz bridge mode to auto create the 'smarter' dummy hardware.
    Go to [SETUP] [HARDWARE] press 'create virtual sensors' on the dummy hardware called 'smarter'
    Give it a name (e.g. Kettle Boil) and select sensor type is switch.
    Go to [SWITCHES], scroll all the way down.
    Select 'edit' on your newly created device.
      Switch Icon, well heating is nice!
      On Action:  script://locationibrew/iBrew on kettleip
      Off Action: script://locationibrew/iBrew off kettleip
      
    You now have a functional boil/stop switch... 
    
    If you do not want a switch you can also create two push (on/off) buttons
    and fill in the action.
  
  If you use homebridge for domoticz (https://www.domoticz.com/forum/viewtopic.php?t=10272) you can use
  apple homekit with the kettle. You have to create extra virtual sensor (motion boil???) because the text sensor is not supported
  by homekit, all the other are.
  

  Usage:

    domoticz [domoticz] [basename] [kettle]

  Where:
  
    domoticz        Connection string to domoticz, [host:port] or [username:password@host:port]
    basename        Base name of your kettle devices in domoticz. The name may contain spaces.
    kettle          Connection string to iKettle 2.0, [host]
    host            Format: ip4, ip6, fqdn
    

  Notes:
  
    It will auto-create the devices in Domoticz
    Tested on Domoticz v3.52
    *** Currently iKettle 2.0 Only ***
  
  Examples:
  
    iBrew domoticz sofia:$ecrit@localhost:8080 Kettle Kitchen 192.168.4.1
    iBrew domoticz 10.0.0.1:9001 Kettle Office 192.168.10.13
    iBrew dump domoticz 10.0.0.1:9001 Kettle Office 192.168.10.13
    iBrew domoticz localhost:8080 Kettle 
  
              

```

Example keepalive LaunchAgent for macOS/OSX, i soft linked /usr/local/bin/ibrew to iBrew.
But you can change it to your normal copy, also change the working directory...

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Disabled</key>
	<false/>
	<key>KeepAlive</key>
	<true/>
	<key>Label</key>
	<string>com.domoticz.ikettle</string>
	<key>ProgramArguments</key>
	<array>
		<string>/usr/local/bin/ibrew</string>
		<string>domoticz</string>
		<string>10.0.0.1:8090</string>
		<string>Kettle</string>
		<string>10.0.0.99</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>WorkingDirectory</key>
	<string>/Users/Tristan/Smarthome/domoticz/scripts</string>
</dict>
</plist>
```

## Protocol

### Structure

```

       
       
  Smarter iKettle 2.0 & Smarter Coffee Protocol
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
    
              

```

### Messages Index

```


  Smarter iKettle 2.0 & Smarter Coffee Messages
  _____________________________________________


    k c ID Command Message
    ___________________________________________
    ✓ ? 02 Set device time
    ✓ ? 05 Set wireless network name
    ✓ ? 07 Set wireless network password
    ✓ ? 0c Join wireless network
    ✓ ? 0d Scan for wireless networks
    ✓ ? 0f Leave wireless network
    ✓ ✓ 10 Reset default user settings
    ✓ ? 15 Heat kettle
    ✓ ? 16 Stop heating kettle
    ✓ ? 19 Heat kettle using formula mode
    ✓ ? 1f Set kettle default user settings
    ✓ ? 20 Working unknown command (turn on?)
    ✓ ? 21 Working unknown command (turn on?)
    ✓ ? 22 Working unknown command (turn on?)
    ✓ ? 23 Working unknown command (turn on?)
    ✓ ? 28 Get History Device
    ✓ ? 2a Set water sensor base value
    ✓ ? 2b Get water sensor base value
    ✓ ? 2c Calibrate water sensor
    ✓ ? 2e Get default user settings
    ✓ ? 30 Working unknown command
    ✕ ✓ 33 Start coffee brewing
    ✕ ✓ 34 Stop coffee brewing
    ✕ ✓ 35 Set strength of the coffee to brew
    ✕ ✓ 36 Set number of cups to brew
    ✕ ✓ 37 Start coffee brewing using default
    ✕ ✓ 38 Set coffee machine default user settings
    ✕ ✓ 3c Toggle grinder
    ✕ ✓ 3e Turn on hotplate
    ✕ ✓ 40 Working unknown command (schedule?)
    ✕ ✓ 41 Working unknown command (schedule?)
    ✕ ✓ 43 Working unknown command (schedule?)
    ✕ ✓ 4a Turn off hotplate
    ✕ ✓ 4c Coffee Carafe Required Status
    ✕ ✓ 4f Coffee Single Mode Status
    ✓ ✓ 64 Get device info
    ✓ ? 69 Working unknown command
    ✓ ? 6a Get wifi firmware info
    ✓ ? 6d Device firmware update

    k c ID Response Message
    _______________________________
    ✓ ? 03 Command status
    ✓ ? 0e Wireless networks list
    ✓ ✓ 14 Kettle status
    ✓ ? 29 Device history
    ✓ ? 2d Water sensor base value
    ✓ ✓ 2f Default user settings
    ✕ ✓ 32 Coffee machine status
    ✕ ✓ 4d Carafe status
    ✕ ✓ 50 Single cup mode status
    ✓ ✓ 65 Device info
    ✓ ? 6b Wifi firmware info

    Legend:
      k iKettle 2
      c Smarter Coffee



```

### Message Information

```


  Command Message 02: Set device time
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Set the time on the device, is used in history reply messages.
  Unknown is Day of week index?

  Arguments: <SECONDS><MINUTES><HOURS><??><DAY><MONTH><CENTURY><YEAR>

  SECONDS
    00..3b

  MINUTES
    00..3b

  HOURS
    00..17

  DAY
    00..1e

  MONTH
    00..0b

  CENTURY
    13..15

  YEAR
    00..63

  Example: 00 00 00 00 00 00 00 00 ???




  Response Message 03: Command status
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [02,Set device time] [05,Set wireless network name] [07,Set wireless network password] [10,Reset default user settings] [15,Heat kettle] [16,Stop heating kettle] [19,Heat kettle using formula mode] [1f,Set kettle default user settings] [20,Working unknown command (turn on?)] [21,Working unknown command (turn on?)] [22,Working unknown command (turn on?)] [23,Working unknown command (turn on?)] [2b,Get water sensor base value] [2c,Calibrate water sensor] [69,Working unknown command] 
  Message Size: 3 bytes

  ✓ iKettle 2.0   ? Smarter Coffee

  Response: <STATUS>

  STATUS
    00 Success
    01 Busy
    02 No Carafe (Coffee unverified)
    03 No Water (Coffee unverified)
    04 Failed
    05 No Carafe
    06 No Water
    69 Invalid Command

  The response status of the coffee can be bit encoded (see response 14)




  Command Message 05: Set wireless network name
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Argument: <SSID>{0,32}
  Just normal ascii




  Command Message 07: Set wireless network password
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Argument: <PASSWORD>{0,32}
  Just normal ascii




  Command Message 0c: Join wireless network
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ? Smarter Coffee

  Sending this command without previous SSID/password messages will reset the wifi
  to factory settings.

  Send:
    Set wireless network name
    Set wireless network password
    Join wireless network

  Read all the command status ssuccess

  The apps actually sends: 0c 7e 00 00 00 00 00 00




  Command Message 0d: Scan for wireless networks
  ─────────────────────────────────────────────────────────────────────────
  Response message: [0e,Wireless networks list] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example raw code: 0d 7e




  Response Message 0e: Wireless networks list
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [0d,Scan for wireless networks] 

  ✓ iKettle 2.0   ? Smarter Coffee

  DB is the signal strength in dBm format.

  Response: <SSID>{0,32}<",-"><DB>{2}<"}">

  Examples: MyWifi,-56}
            MyWifi,-56}OtherWifi,-82}




  Command Message 0f: Leave wireless network
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ? Smarter Coffee

  Leaves wireless network and reset wifi to default

  Example raw code: 0f 7e
  It actually sends: 0f 7e 6d 7e




  Command Message 10: Reset default user settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✓ Smarter Coffee

  For the kettle these are the default user settings:
  keepwarm 0 minutes (0x00), temperature 100ºC (0x64)
  formula mode off (0x00) and formula temperature 75ºC (0x4b)

  The Smarter Coffee it will probably reset the number of cups and strength

  Example raw code: 10 7e




  Response Message 14: Kettle status
  ─────────────────────────────────────────────────────────────────────────
  Message Size: 7 bytes

  ✓ iKettle 2.0   ✓ Smarter Coffee

  There is correlation between the temperature the watersensor and the base. How higher
  the temperature how higher the watersensor with the same volume of water.

  Response iKettle: <STATUSKETTLE><TEMPERATURE><WATERSENSORBITSHIGH><WATERSENSORBITSLOW><??>

  Response Smarter Coffee: <STATUSCOFFEE><WATERLEVEL><WIFISTRENGTH???/WATERSENSORBITSLOW???>
                           <STRENGTH><CUPS>

  STATUSKETTLE
    00 Ready
    01 Boiling
    02 Keep Warm
    03 Cycle Finished
    04 Baby Cooling

  TEMPERATURE
    00..64  0..100ºC
    7f      Kettle Off Base

  WATERSENSOR = WATERSENSORHIGHBITS * 256 + WATERSENSORLOWBITS




  Command Message 15: Heat kettle
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  if it's warming you have to send an off command to boil again
  if it's not on temp it boils first before warming...

  Argument: <TEMPERATURE><KEEPWARMTIME>

  TEMPERATURE
    00..64  0..100ºC

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  Example: 15 32 00 7e




  Command Message 16: Stop heating kettle
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example: 16 7e




  Command Message 19: Heat kettle using formula mode
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Boil water to (default user temperature)
 and cool until the formula temperature and then keep it warm.

  Arguments: <FORMULATEMPERATURE><KEEPWARMTIME>

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  TEMPERATURE
    00..64  0..100ºC

  FORMULATEMPERATURE
    00..64  0..100ºC

  Example: 19 32 19 7e




  Command Message 1f: Set kettle default user settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Default user defaults message is 1f 00 64 00 4b 7e

  Arguments: <KEEPWARMTIME><TEMPERATURE><FORMULA><FORMULATEMPERATURE>

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  TEMPERATURE
    00..64  0..100ºC

  FORMULA
    00 Do not use as default
    01 Use as default

  FORMULATEMPERATURE
    00..64  0..100ºC

  Example: 1f 19 64 01 22 7e






  Command Message 20: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  This setting ignores the user setting and boils till 100C

  Example raw code: 20 7e




  Command Message 21: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  No information available on message: 21




  Command Message 22: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example: 22 7e




  Command Message 23: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example: 23 7e




  Command Message 28: Get History Device
  ─────────────────────────────────────────────────────────────────────────
  Response message: [29,Device history] 

  ✓ iKettle 2.0   ? Smarter Coffee

  When called will erase this history.

  Example: 28 7e




  Response Message 29: Device history
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [28,Get History Device] 

  ✓ iKettle 2.0   ? Smarter Coffee

  The payload is generated everytime the kettle stops boiling. The actioncounter increases with every boil
  Formula temperature is above 0 then it was boilded with formula temperature enabled. There seems to be some
  packed time available.

  Response: <COUNTER> [<PAYLOAD>{COUNTER}]

  PAYLOAD
    <??><TEMPERATURE><KEEPWARMTIME><FORMULATEMPERATURE><ACTIONCOUNTER>
    <ACTIONCOUNTER???/TIME???><TIME?><TIME?><DATE?><DATE?><???/DATE???><STATE><??>{19}

  TEMPERATURE
    00..64  0..100ºC

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  FORMULATEMPERATURE
    00..64  0..100ºC

  ACTIONCOUNTER
    00..ff

  TIME/DATE?

  STATE
    00 Stopped
    01 Boiled

  Example: 29 02 01 5f 00 00 0f 00 09 03 15 0a 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d
              01 64 19 32 10 00 09 0e 15 0a 19 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e




  Command Message 2a: Set water sensor base value
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ? Smarter Coffee

  Arguments: <BASELHIGHBITS><BASELOWBITS>

  BASE = BASELHIGHBITS * 256 + BASELOWBITS

  Example: 2a 04 03

  This can contain the tail 7e, so check for length here!




  Command Message 2b: Get water sensor base value
  ─────────────────────────────────────────────────────────────────────────
  Response message: [2d,Water sensor base value] [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example: 2b 7e




  Command Message 2c: Calibrate water sensor
  ─────────────────────────────────────────────────────────────────────────
  Response message: [2d,Water sensor base value] [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example: 2c 7e

  Returns also a command success response message after the base repsonse message




  Response Message 2d: Water sensor base value
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [2b,Get water sensor base value] [2c,Calibrate water sensor] 
  Message Size: 4 bytes

  ✓ iKettle 2.0   ? Smarter Coffee

  Response: <BASELHIGHBITS><BASELOWBITS>

  BASE = BASELHIGHBITS * 256 + BASELOWBITS

  This can contain the tail 7e, so check for length here!




  Command Message 2e: Get default user settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [2f,Default user settings] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Also return 00 message in an unconfigured state.

  Example: 2e 7e




  Response Message 2f: Default user settings
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [2e,Get default user settings] 
  Message Size: 9 bytes

  ✓ iKettle 2.0   ✓ Smarter Coffee

  Response: <KEEPWARMTIME><TEMPERATURE><FORMULATEMPERATURE>

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  TEMPERATURE
    00..64  0..100ºC

  FORMULATEMPERATURE
    00..64  0..100ºC




  Command Message 30: Working unknown command
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ? Smarter Coffee

  Arguments: <[UNKNOWN]>{?}

  Example: 30 7e




  Response Message 32: Coffee machine status
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  I do not have a smarter coffee, but I suspect that the WIFISTRENGTH is just
  the WATERSENSORBITSLOW part of the waterlevel sensor.

  Response: <STATUSCOFFEE><WATERLEVEL><WIFISTRENGTH???/WATERSENSORBITSLOW???><STRENGTH><CUPS>

  STATUSKETTLE
    00 Ready
    01 Boiling
    02 Keep Warm
    03 Cycle Finished
    04 Baby Cooling

  WATERSENSOR = WATERSENSORHIGHBITS * 256 + WATERSENSORLOWBITS

  STATUSCOFFEE (unverified)
    04 Filter, ?                      #  00000100
    05 Filter, OK to start            #  00000101
    06 Filter, OK to start            #  00000110
    07 Beans, OK to start             #  00000111
    20 Filter, No carafe              #  00100000
    22 Beans, No carafe               #  00100010
    45 Filter, Done                   #  01000101 <-- from here actions
    47 Beans, Done                    #  01000111
    53 Boiling                        #  01010011
    60 Filter, No carafe, Hotplate On #  01100000
    61 Filter, Hotplate On            #  01100001
    62 Beans, No carafe, Hotplate On  #  01100010
    63 Beans, Hotplate On             #  01100011
    51 Descaling in progress          #  01010001
                                           HB RBC
                                           OO EEA
                                           TI AAR
                                           PL DNA
                                           LI YSF
                                           AN   E
                                           TG
                                           E

  These are guesses I do not own a smarter coffee...
  BIT 0 = UNKNOWN/UNUSED?
  BIT 1 = ACTION???
  BIT 2 = HOTPLATE
  BIT 3 = Boiling & Descaling (USES BIT 6)
  BIT 4 = UNKNOWN/UNUSED?
  BIT 5 = READY/BUSY (OK TO START, FINISHED = 1 else 0)
  BIT 6 = FILTER/BEANS
  BIT 7 = CARAFE OFFBASE/ONBASE

  WATERLEVEL
    00 Not enough water
    01 Low
    02 Half
    12 Half
    13 Full

  STRENGTH
    00 Weak
    01 Medium
    02 Strong

  CUPS
    00..0c




  Command Message 33: Start coffee brewing
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Example: 33 .. .. .. 7e




  Command Message 34: Stop coffee brewing
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

 NEW




  Command Message 35: Set strength of the coffee to brew
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Sets the strength of the coffee to be brewed. Use command 37 to brew
  Argument: <STRENGTH>

  STRENGTH
    00 Weak
    01 Medium
    02 Strong

  Example: 35 01 7e




  Command Message 36: Set number of cups to brew
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Sets the number of cups to be brewed, range between 1 and 12.
  Use command 37 to brew

  Argument: <CUPS>

  CUPS
    00..0c

  Example: 36 03 7e




  Command Message 37: Start coffee brewing using default
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Example: 37 7e




  Command Message 38: Set coffee machine default user settings
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

 NEW




  Command Message 3c: Toggle grinder
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Example: 3c 7e




  Command Message 3e: Turn on hotplate
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Sets on the hotplate, you can specify how many minutes before it switch off.
  Range between 5 and 30, the app sends 5 on default

  Argument: <[KEEPWARMTIME]>

  KEEPWARMTIME
    05..1e 5 .. 20 minutes
    05     5 Minutes (Default)

  Example: 3e 05 7e




  Command Message 40: Working unknown command (schedule?)
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Updating schedules
  No information available on message




  Command Message 41: Working unknown command (schedule?)
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Requesting schedules
  No information available on message




  Command Message 43: Working unknown command (schedule?)
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Schedules
  No information available on message




  Command Message 4a: Turn off hotplate
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Example: 4a 7e




  Command Message 4c: Coffee Carafe Required Status
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

 NEW




  Response Message 4d: Carafe status
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [4c,Coffee Carafe Required Status] 
  Message Size: 3 bytes

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Response: <BOOLEAN>




  Command Message 4f: Coffee Single Mode Status
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ Smarter Coffee

 NEW




  Response Message 50: Single cup mode status
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [4f,Coffee Single Mode Status] 
  Message Size: 3 bytes

  ✕ iKettle 2.0   ✓ Smarter Coffee

  Response: <BOOLEAN>




  Command Message 64: Get device info
  ─────────────────────────────────────────────────────────────────────────
  Response message: [65,Device info] 

  ✓ iKettle 2.0   ✓ Smarter Coffee

  Get the type of the device connected to and it's firmware. It is used for
  auto discovery over UDP broadcast (after device setup is complete?)
  This fails on some routers, which don't propagate UDP broadcasts

  Example: 64 7e




  Response Message 65: Device info
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [64,Get device info] 
  Message Size: 4 bytes

  ✓ iKettle 2.0   ✓ Smarter Coffee

  Response: <TYPE><VERSION>

  TYPE:
    01 iKettle 2.0
    02 Smarter Coffee

  VERSION:
    13 Firmware v19 of iKettle 2.0

  Example: 65 01 13 7e




  Command Message 69: Working unknown command
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Without argumens it returns failed otherwise it returns success.

  Arguments: <UNKNOWN>{?}

  Example: 69 7e




  Command Message 6a: Get wifi firmware info
  ─────────────────────────────────────────────────────────────────────────
  Response message: [6b,Wifi firmware info] 

  ✓ iKettle 2.0   ? Smarter Coffee

  Example: 6a 7e




  Response Message 6b: Wifi firmware info
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [6a,Get wifi firmware info] 

  ✓ iKettle 2.0   ? Smarter Coffee

  The firmware of the wifi module in text with control chars as new line.
  The iKettle 2.0 returns (without control chars):

  Response: <FIRMWARE>{?}

  AT+GMR
  AT version:0.40.0.0(Aug  8 2015 14:45:58)
  SDK version:1.3.0
  compile time:Aug  8 2015 17:19:38
  OK




  Command Message 6d: Device firmware update
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ? Smarter Coffee

  Disables wifi and creates a 'iKettle Update' wireless network and opens port 6000.
  A hard device reset (hold power button for 10 seconds) is sometimes required to fix this state,
  or just unplug the power for a moment.

  Example: 6d 7e



```

### Notes

```



  Smarter iKettle 2.0 & Smarter Coffee Notes
  __________________________________________
    
  WaterSensor Calibration:

    If the kettle is on the base during calibration, the numbers change to be higher,
    but the differences between levels seem the same. This means that the water level
    detection is probably weight based and that calibration is done at the base,
    which then remembers the weight for 'off base'. To detect an empty kettle,
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
     
 
              

```              


## Bugs / Not done
  *    Set Device Time is missing arguments in console
  *    Set default is missing arguments in console
  *    Boil has no arguments 
  *    Brew has no arguments
  *    Auto-reconnect
  *    Missing Coffee Smarter codes
  *    History message is not finished
  *    [will not fix] Should read status message 14 all the time in console mode
  *    [will not implement] Default auto connect first coffee or kettle with no host


## Links

#### Smart Kettles & Coffee Machines
  *    http://smarter.am/

#### Smarthome Controller
  *    https://domoticz.com/  
      
#### References
  *    https://github.com/Jamstah/libsmarteram2/
  *    https://github.com/ian-kent/ikettle2/
  *    https://github.com/athombv/am.smarter/
  *    https://github.com/nanab/smartercoffee/
  *    https://github.com/AdenForshaw/smarter-coffee-api
  *    https://github.com/Half-Shot/Smarter-Coffee-NET
  *    https://domoticz.com/forum/viewtopic.php?f=23&t=12837
  *    https://github.com/jkellerer/fhem-smarter-coffee/
  *    https://www.pentestpartners.com/blog/hacking-a-wi-fi-coffee-machine-part-1/
