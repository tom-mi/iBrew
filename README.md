# iBrew Kettle Rattle

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface, web interface, rest api and bridge to [Domoticz](http://domoticz.com). You can also use it in your own code. iKettle 2.0 v19 tested only at the moment. Please share any other discoveries you made!

This means your machine is free! You can connect it yourself and do whatever you want with it. You are in full control! You can also interface it with your favorite smarthome controller. A working bridge to domoticz is already included (which you can bridge with homekit or other fun stuff)!

   Signed TRiXWooD

#### Versions
 * v0.0 Bean Grinder Pack
 * v0.1 White Tealeaf Edition
 * v0.2 Tea Noire Sweet
 * v0.3 Kettle Rattle 
 * v0.4 Brewing on the 7th day (web interface)
 
#### Upcoming   
 * Better error handling (sometimes it does not quit :-)
 * it also hangs if you scan wifi too much (luckily it reconnects)
 * Connecting in console mode... fails sometimes, and after reconnect is had strange data... stupid threads... missing...
 * Brew, heat, formula arguments (I have to figure out what is what, one cup at a time... 
 * Time arguments (have not figured that out)
 * Web interface & rest api (rest almost finished, web interface still have to create some pages) and introduce webroot & api key...
 * History message is not finished
 * web does not reconnect added devices (if scanning for kettle & cofee machine does not work)
 * Fahrenheid not finished, please to not use.
 * can't start the web interface twice in console (i probably did not clean up)
 * if you send a message with an if of a response as command it displays the response infoiting to send...
 * v0.5 Missing Coffee Smarter codes (!)
 * I broke domoticz :-)
 
 
 iBrew v0.5: Dumb Dump Limited Collector Edition
 (numbered, signed by author)
 
#### Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). Donations & other questions <tristan@monkeycat.nl>


## Installation

#### Software Requirements 
* python 2.7
* python (optional) package: tornado 
* python (optional) package: pybonjour)
* pandoc (optional, development only)

#### Download
You can download and unpack the [source](https://github.com/Tristan79/iBrew/archive/master.zip) or download it from github using

```
git clone https://github.com/Tristan79/iBrew.git
```


## Contributing

Use the fork button in the upper right corner of [iBrew](https://github.com/Tristan79/iBrew/) and [Github Desktop](https://desktop.github.com) 
or fork it manually. Run the following commands in the root if the iBrew folder to do so.

Create your feature branch 

```git checkout -b my-new-feature-or-fix```

Commit your changes 

```git commit -am 'Add some feature-or-fix```

Push to the branch 

```git push origin my-new-feature-or-fix```

Create new Pull Request


## Usage

### Command Line

See the console section for the commands
 
```

  Usage: iBrew (dump) (shout|coffee|kettle) (fahrenheid) [command] (host)

    fahrenheid             use fahrenheid
    dump                   dump message enabled
    host                   host address (format: ip4, ip6, fqdn)
    shout                  sends commands and quits not waiting for a reply
    command                action to take!

  If you do not supply a host, it will try to connect to the first detected device
  Thus if you have more then one device supply a host (if its not in direct mode)

```

### Console
Start the console with the command `iBrew console`. The following commands are available within the console,
you can also use them on the command line as arguments:

```

  iKettle 2.0 & SmarterCoffee  Commands
    default                set default settings
    info                   device info
    history                action history
    list                   list detected devices
    reset                  reset device to default
    start                  start the device
    status                 show status
    settings               show user settings
    stop                   stop the appliance
    time [time]            set the device time

  iKettle 2.0 Commands
    base                   show watersensor base value
    base [base]            store watersensor base value
    calibrate              calibrates watersensor
    celsius                use celsius ºC [console only]
    fahrenheid             use fahrenheid ºF [console only]
    formula ()()           heat kettle in formula mode
    heat ()()              heat kettle
    stop kettle            stops heating
    settings [keepwarm] [temperature] [formula] [formulatemperature] store kettle user settings

  SmarterCoffee  Commands
    brew ()                brew coffee
    carafe                 returns if carafe is required
    cups [number]          set number of cups [1..12]
    grinder                use grinder
    filter                 use filter
    hotplate off           turn hotplate off
    hotplate on (minutes)  turn hotplate on (time in minutes)
    singlecup              return if singlecup mode is on
    (strength) [strength]  set strength coffee [weak, medium or strong]
    stop coffee            stops brewing
    settings [cups] [strength] [grinder] [hotplate]   store user settings

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
    web (port)             start web interface & rest api on port [default 2082]

  Debug Commands
    [hexdata]              send raw data to device (e.g. '64 7e')
    dump                   toggle 'dump raw messages'
    console                start console [command line only]
    connect [host]         connect to device [console only]
    firmware               show firmware Wifi
    monitor                monitor incomming traffic
    protocol               show all protocol information available
    stats                  show traffic statistics
    sweep (id)             try (all or start with id) unknown command codes

  Console Commands
    joke                   show joke
    quit                   quit console [console only]


```

#### Examples

```

  Example:
    off            Stop heating/brewing
    messages       Show all protocol messages
    message 3e     Show protocol message 3a, turn hotplate on
    167E           Send kettle raw stop
    21 30 05 7e    Send kettle raw heat
    strength weak  Set coffee strength to weak
    cups 3         Set number of cups to brew


```


### Web Interface

This is a build in progress, please contribute!

```
http://ip:port/
```

![devices](https://raw.githubusercontent.com/Tristan79/iBrew/master/help/devices.png)

![api](https://raw.githubusercontent.com/Tristan79/iBrew/master/help/api.png)

![info](https://raw.githubusercontent.com/Tristan79/iBrew/master/help/info.png)



### REST API

Start the web interface.


```
http://ip:port/api
```

The following links are available

```
/version
/devices
/joke
```

Which contains the ip which you can use to monitor or control individual devices.

```
http://ip:port/api/ip
```

The following links are available

```
/start
/stop
/join/name/(password)
/leave
/scan
/joke
/default
/settings/(v1/v2/v3/v4/)
/status
```

Kettle
```
/calibrate
/calibrate/base/(value)
```

Coffee Machine
```
/carafe
/singlecup
/hotplate/value
/grinder/bool
/cups/value
/strength/value
```

Look up the the possible arguments in the console commands.


### Domoticz Bridge

Bridge to [Domoticz](http://domoticz.com)!

iKettle Devices in Domoticz
![domoticz v3.52](https://raw.githubusercontent.com/Tristan79/iBrew/master/help/domoticz.png)
   
   
```

```

Example keepalive LaunchAgent for macOS/OSX, i soft linked /usr/local/bin/ibrew to iBrew.
But you can change it to your normal copy, also change the working directory,domoticz ip and kettle ip.

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
    
              

```

### Messages Index

```


  Smarter iKettle 2.0 & SmarterCoffee  Messages
  _____________________________________________


    k c ID Command Message
    ___________________________________________
    ✓ ✓ 02 Set device time
    ✓ ✓ 05 Set wireless network name
    ✓ ✓ 07 Set wireless network password
    ✓ ✓ 0c Join wireless network
    ✓ ✓ 0d Scan for wireless networks
    ✓ ✓ 0f Leave wireless network
    ✓ ✓ 10 Reset default user settings
    ✓ ✕ 15 Heat kettle
    ✓ ✕ 16 Stop heating kettle
    ✓ ✕ 19 Heat kettle using formula mode
    ✓ ✕ 1f Set kettle default user settings
    ✓ ✕ 20 Working unknown command (turn on?)
    ✓ ✕ 21 Working unknown command (turn on?)
    ✓ ✕ 22 Working unknown command (turn on?)
    ✓ ✕ 23 Working unknown command (turn on?)
    ✓ ✕ 28 Get kettle history
    ✓ ✕ 2a Set water sensor base value
    ✓ ✕ 2b Get water sensor base value
    ✓ ✕ 2c Calibrate water sensor
    ✓ ✕ 2e Get default kettle user settings
    ✓ ✕ 30 Working unknown command
    ✕ ✓ 33 Start coffee brewing
    ✕ ✓ 34 Stop coffee brewing
    ✕ ✓ 35 Set strength of the coffee to brew
    ✕ ✓ 36 Set number of cups to brew
    ✕ ✓ 37 Start coffee brewing using machine settings
    ✕ ✓ 38 Set coffee machine default user settings
    ✕ ✓ 3c Toggle grinder
    ✕ ✓ 3e Turn on hotplate
    ✕ ✓ 40 Working unknown command (schedule?)
    ✕ ✓ 41 Working unknown command (schedule?)
    ✕ ✓ 43 Working unknown command (schedule?)
    ✕ ✓ 46 Get coffee machine history
    ✕ ✓ 48 Get default coffee machine user settings
    ✕ ✓ 4a Turn off hotplate
    ✕ ✓ 4b Working unknown command
    ✕ ✓ 4c Get coffee carafe required
    ✕ ✓ 4e Working unknown command
    ✕ ✓ 4f Get single coffee cup mode
    ✓ ✓ 64 Get device info
    ✓ ✓ 69 Working unknown command
    ✓ ✓ 6a Get wifi firmware info
    ✓ ✓ 6d Device firmware update

    k c ID Response Message
    _______________________________
    ✓ ✓ 03 Command status
    ✓ ✓ 0e Wireless networks list
    ✓ ✓ 14 Kettle status
    ✓ ✕ 29 Kettle history
    ✓ ✕ 2d Water sensor base value
    ✓ ✓ 2f Default kettle user settings
    ✕ ✓ 32 Coffee machine status
    ✕ ✓ 47 Coffee machine history
    ✕ ✓ 49 Get default coffee machine user settings
    ✕ ✓ 4d Carafe required
    ✕ ✓ 50 Single coffee cup mode
    ✓ ✓ 65 Device info
    ✓ ✓ 6b Wifi firmware info

    Legend:
      k iKettle 2
      c SmarterCoffee 



```

### Message Information

```


  Command Message 02: Set device time
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

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

  Example: 02 12 13 03 01 05 02 14 10 ???




  Response Message 03: Command status
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [02,Set device time] [05,Set wireless network name] [07,Set wireless network password] [10,Reset default user settings] [15,Heat kettle] [16,Stop heating kettle] [19,Heat kettle using formula mode] [1f,Set kettle default user settings] [20,Working unknown command (turn on?)] [21,Working unknown command (turn on?)] [22,Working unknown command (turn on?)] [23,Working unknown command (turn on?)] [2b,Get water sensor base value] [2c,Calibrate water sensor] [69,Working unknown command] [40,Working unknown command (schedule?)] [41,Working unknown command (schedule?)] [43,Working unknown command (schedule?)] [4b,Working unknown command] [4e,Working unknown command] 
  Message Size: 3 bytes

  ✓ iKettle 2.0   ✓ SmarterCoffee 

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

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Argument: <SSID>{0,32}
  Just normal ascii




  Command Message 07: Set wireless network password
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Argument: <PASSWORD>{0,32}
  Just normal ascii




  Command Message 0c: Join wireless network
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ✓ SmarterCoffee 

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

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Example raw code: 0d 7e




  Response Message 0e: Wireless networks list
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [0d,Scan for wireless networks] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  DB is the signal strength in dBm format.

  Response: <SSID>{0,32}<",-"><DB>{2}<"}">

  Examples: MyWifi,-56}
            MyWifi,-56}OtherWifi,-82}




  Command Message 0f: Leave wireless network
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Leaves wireless network and reset wifi to default

  Example raw code: 0f 7e
  It actually sends: 0f 7e 6d 7e




  Command Message 10: Reset default user settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  For the kettle these are the default user settings:
  keepwarm 0 minutes (0x00), temperature 100ºC (0x64)
  formula mode off (0x00) and formula temperature 75ºC (0x4b)

  The SmarterCoffee  it will probably reset the number of cups and strength

  Example raw code: 10 7e




  Response Message 14: Kettle status
  ─────────────────────────────────────────────────────────────────────────
  Message Size: 7 bytes

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  There is correlation between the temperature the watersensor and the base. How higher
  the temperature how higher the watersensor with the same volume of water.

  Response iKettle: <STATUSKETTLE><TEMPERATURE><WATERSENSORBITSHIGH><WATERSENSORBITSLOW><??>

  STATUSKETTLE
    00 Ready
    01 Heating water
    02 Keep warm
    03 Cycle finished
    04 Baby cooling

  TEMPERATURE
    00..64  0..100ºC
    7f      Kettle Off Base

  WATERSENSOR = WATERSENSORHIGHBITS * 256 + WATERSENSORLOWBITS  [0..4095]




  Command Message 15: Heat kettle
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  if it's warming you have to send an off command to heat again
  if it's not on temp it heats first before warming...

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

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Example: 16 7e




  Command Message 19: Heat kettle using formula mode
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Heats water to (default user temperature)
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

  ✓ iKettle 2.0   ✕ SmarterCoffee 

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

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  This setting ignores the user setting and heats untill the tempeature is 100ºC

  Example raw code: 20 7e




  Command Message 21: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  No information available on message: 21




  Command Message 22: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Example: 22 7e




  Command Message 23: Working unknown command (turn on?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Example: 23 7e




  Command Message 28: Get kettle history
  ─────────────────────────────────────────────────────────────────────────
  Response message: [29,Kettle history] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  When called will erase this history.

  Example: 28 7e




  Response Message 29: Kettle history
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [28,Get kettle history] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  The payload is generated everytime the kettle stops heating. The actioncounter increases with every heating?
  Formula temperature is above 0 then it was heated with formula temperature enabled. There seems to be some
  packed time available.

  Payload maximum is 8. So if 8 check again, if there is more history
  month checked only accepts value from 1..0c

  Response: <COUNTER> [<PAYLOAD>{COUNTER}]

  PAYLOAD
    <??><TEMPERATURE><KEEPWARMTIME><FORMULATEMPERATURE><ACTIONCOUNTER>
    <SECONDS??><HOURS?><MINUTES?><DAY?><MONTH><YEAR80?><STATE><??>{19}

  COUNTER
    00..08

  TEMPERATURE
    00..64  0..100ºC

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  FORMULATEMPERATURE
    00..64  0..100ºC

  ACTIONCOUNTER
    00..ff  Amount of heatings before off base

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

  YEAR80
    00..FF  YEAR = YEAR80 + 1980

  STATE
    00 Stopped
    01 Success

  Example: 29 02 01 5f 00 00 0f 00 09 03 15 0a 19 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d
                 01 64 19 32 10 00 09 0e 15 0a 19 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e




  Command Message 2a: Set water sensor base value
  ─────────────────────────────────────────────────────────────────────────

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Arguments: <BASELHIGHBITS><BASELOWBITS>

  BASE = BASELHIGHBITS * 256 + BASELOWBITS [0..4095]
  Example: 2a 04 03

  This can contain the tail 7e, so check for length here!




  Command Message 2b: Get water sensor base value
  ─────────────────────────────────────────────────────────────────────────
  Response message: [2d,Water sensor base value] [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Example: 2b 7e




  Command Message 2c: Calibrate water sensor
  ─────────────────────────────────────────────────────────────────────────
  Response message: [2d,Water sensor base value] [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Example: 2c 7e

  Returns also a command success response message after the base repsonse message




  Response Message 2d: Water sensor base value
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [2b,Get water sensor base value] [2c,Calibrate water sensor] 
  Message Size: 4 bytes

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Response: <BASELHIGHBITS><BASELOWBITS>

  BASE = BASELHIGHBITS * 256 + BASELOWBITS [0..4095]

  This can contain the tail 7e, so check for length here!




  Command Message 2e: Get default kettle user settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [2f,Default kettle user settings] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Also return 00 message in an unconfigured state.??? CHECK

  Example: 2e 7e




  Response Message 2f: Default kettle user settings
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [2e,Get default kettle user settings] 
  Message Size: 9 bytes

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Response: <TEMPERATURE><KEEPWARMTIME><FORMULATEMPERATURE>

  KEEPWARMTIME
    00      Default off
    05..1e  Keep Warm in Minutes

  TEMPERATURE
    00..64  0..100ºC

  FORMULATEMPERATURE
    00..64  0..100ºC




  Command Message 30: Working unknown command
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✕ SmarterCoffee 

  Arguments: <[UNKNOWN]>{?}

  Example: 30 7e




  Response Message 32: Coffee machine status
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  I do not have a smarter coffee, but I suspect that the WIFISTRENGTH is just
  the WATERSENSORBITSLOW part of the waterlevel sensor.

  Response: <STATUSCOFFEE><WATERLEVEL><WIFISTRENGTH???/WATERSENSORBITSLOW???><STRENGTH><UNKNOWNANDCUPS>

  STATUSKETTLE
    00 Ready
    01 Heating water
    02 Keep warm
    03 Cycle finished
    04 Baby cooling

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
    53 Heating water                  #  01010011
    60 Filter, No carafe, Hotplate On #  01100000
    61 Filter, Hotplate On            #  01100001
    62 Beans, No carafe, Hotplate On  #  01100010
    63 Beans, Hotplate On             #  01100011
    51 Descaling in progress          #  01010001
                                          WHHGRBC
                                          OOEREEA
                                          RTAIAAR
                                          KPTNDNA
                                          ILIDYSF
                                          NANI  E
                                          GTGN
                                           E G

  These are guesses I do not own a smarter coffee...
  BIT 7 = UNKNOWN/UNUSED?
  BIT 6 = IDLE/WORKING
  BIT 5 = Hot plate On/Off
  BIT 4 = Heating On/Off
  BIT 3 = Grinding
  BIT 2 = READY/BUSY (OK TO START)
  BIT 1 = FILTER/BEANS
  BIT 0 = CARAFE OFFBASE/ONBASE

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

  UNKNOWNANDCUPS
    CUPS    4 lower bits
    UNKNOWN 4 higher bits

  CUPS
    00..0c




  Command Message 33: Start coffee brewing
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Arguments: <CUPS><STRENGTH><HOTPLATE><GRINDER>

  CUPS
    00..0c

  STRENGTH
    00 Weak
    01 Medium
    02 Strong

  HOTPLATE TIMER
    05..28 5 .. 40 minutes
    05     5 Minutes (Default)

  GRINDER <BOOLEAN>

  Example: 33 04 02 00 7e




  Command Message 34: Stop coffee brewing
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Example 33 7e 




  Command Message 35: Set strength of the coffee to brew
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Sets the strength of the coffee to be brewed. Use command 37 to brew
  Argument: <STRENGTH>

  STRENGTH
    00 Weak
    01 Medium
    02 Strong

  Example: 35 01 7e




  Command Message 36: Set number of cups to brew
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Sets the number of cups to be brewed, range between 1 and 12.
  Use command 37 to brew

  Argument: <CUPS>

  CUPS
    00..0c

  Example: 36 03 7e




  Command Message 37: Start coffee brewing using machine settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Uses the settings not the default user settings
  Example: 37 7e




  Command Message 38: Set coffee machine default user settings
  ─────────────────────────────────────────────────────────────────────────

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Arguments: <STRENGTH><CUPS><GRINDER><HOTPLATE>

  STRENGTH
    00 Weak
    01 Medium
    02 Strong

  CUPS
    00..0c

  GRINDER <BOOLEAN>

  HOTPLATE
    05..28 5 .. 40 minutes
    05     5 Minutes (Default)





  Command Message 3c: Toggle grinder
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Example: 3c 7e




  Command Message 3e: Turn on hotplate
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Sets on the hotplate, you can specify how many minutes before it switch off.
  Range between 5 and 40, the app sends 5 on default

  Argument: <[KEEPWARMTIME]>

  KEEPWARMTIME
    05..28 5 .. 40 minutes
    05     5 Minutes (Default)

  Example: 3e 05 7e




  Command Message 40: Working unknown command (schedule?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Updating schedules
  No information available on message




  Command Message 41: Working unknown command (schedule?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Requesting schedules
  No information available on message




  Command Message 43: Working unknown command (schedule?)
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Schedules
  No information available on message




  Command Message 46: Get coffee machine history
  ─────────────────────────────────────────────────────────────────────────
  Response message: [47,Coffee machine history] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  When called will erase this history.

  Example: 46 7e




  Response Message 47: Coffee machine history
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [46,Get coffee machine history] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  The payload is generated everytime the coffee machine brews. The actioncounter increases with every brewing?

  Payload maximum is 8. So if 8 check again, if there is more history
  month checked only accepts value from 1..0c

  Response: <COUNTER> [<PAYLOAD>{COUNTER}]

  COUNTER
    00..08

  PAYLOAD
    <??><??><??><DEFAULT/CUPS?><DEFAULT/CUPS?><SECONDS??>
    <HOURS???><MINUTES???><DAY??><MONTH><YEAR80???><STATE><??>{19}

  CUPS
    00..0c

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

  YEAR80
    00..FF  YEAR = YEAR80 + 1980

  STATE
    00 Stopped
    01 Success

  Example: 47 02 01 00 00 02 02 00 19 00 01 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d
                 01 00 00 0c 0c 00 19 00 01 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7d 7e




  Command Message 48: Get default coffee machine user settings
  ─────────────────────────────────────────────────────────────────────────
  Response message: [49,Get default coffee machine user settings] [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Also return 00 message in an unconfigured state.???? CHECK

  Example: 48 7e




  Response Message 49: Get default coffee machine user settings
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [48,Get default coffee machine user settings] 
  Message Size: 6 bytes

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Response: <STRENGTH><CUPS><GRINDER><HOTPLATE>

  CUPS
    00..0c

  STRENGTH
    00 Weak
    01 Medium
    02 Strong

  GRINDER <BOOLEAN>

  HOTPLATE
    05..28 5 .. 40 minutes
    05     5 Minutes (Default)





  Command Message 4a: Turn off hotplate
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Example: 4a 7e




  Command Message 4b: Working unknown command
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Arguments: <[UNKNOWN]>{?}

  Example: 4b ?? 7e




  Command Message 4c: Get coffee carafe required
  ─────────────────────────────────────────────────────────────────────────
  Response message: [32,Coffee machine status] [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

 NEW




  Response Message 4d: Carafe required
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [4c,Get coffee carafe required] 
  Message Size: 3 bytes

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Response: <BOOLEAN>




  Command Message 4e: Working unknown command
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Arguments: <[UNKNOWN]>{?}

  Example: 4e ?? 7e




  Command Message 4f: Get single coffee cup mode
  ─────────────────────────────────────────────────────────────────────────
  Response message: [50,Single coffee cup mode] [03,Command status] 

  ✕ iKettle 2.0   ✓ SmarterCoffee 

 NEW




  Response Message 50: Single coffee cup mode
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [4f,Get single coffee cup mode] 
  Message Size: 3 bytes

  ✕ iKettle 2.0   ✓ SmarterCoffee 

  Response: <BOOLEAN>




  Command Message 64: Get device info
  ─────────────────────────────────────────────────────────────────────────
  Response message: [65,Device info] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Get the type of the device connected to and it's firmware. It is used for
  auto discovery over UDP broadcast (after device setup is complete?)
  This fails on some routers, which don't propagate UDP broadcasts

  Example: 64 7e




  Response Message 65: Device info
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [64,Get device info] 
  Message Size: 4 bytes

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Response: <TYPE><VERSION>

  TYPE:
    01 iKettle 2.0
    02 SmarterCoffee 

  VERSION:
    13 Firmware v19 of iKettle 2.0

  Example: 65 01 13 7e




  Command Message 69: Working unknown command
  ─────────────────────────────────────────────────────────────────────────
  Response message: [03,Command status] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Without argumens it returns failed otherwise it returns success.

  Arguments: <UNKNOWN>{?}

  Example: 69 7e




  Command Message 6a: Get wifi firmware info
  ─────────────────────────────────────────────────────────────────────────
  Response message: [6b,Wifi firmware info] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Example: 6a 7e




  Response Message 6b: Wifi firmware info
  ─────────────────────────────────────────────────────────────────────────
  In response to command message: [6a,Get wifi firmware info] 

  ✓ iKettle 2.0   ✓ SmarterCoffee 

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

  ✓ iKettle 2.0   ✓ SmarterCoffee 

  Disables wifi and creates a 'iKettle Update' wireless network and opens port 6000.
  A hard device reset (hold power button for 10 seconds) is sometimes required to fix this state,
  or just unplug the power for a moment.

  Example: 6d 7e



```

### Notes

```



  Smarter iKettle 2.0 & SmarterCoffee  Notes
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
         *  It will heat up empty, making the lights bulbs to flikker.
         *  You can easily knock out it's connection to the wireless network,
            if it fails to connect it creates an default open unencrypted wifi access point 
            (check!, could be that wifi was not connecting, then this is rubbish ;-).

            Attack Vectors
            1. Repeat sending heat to 100ºC temperature commands, if we're lucky
               there is no water and it will heat up empty, if not it will take a while.
               plus the kettle will get warmer and warmer. If you do not expect that when touching.
            2. Alternating heat and stop commands.
            3. (Check) Wait until the owner of the kettle log in on the kettle, since its an
               open access point and the password are send in the open you can read it.


  Coffee Brewing:

    Between setting the number of cups, the strength of the coffee and start of brewing
    atleast 500ms is recommended.
    

  Water Heating:
  
    From smarter website the temperature that can be set is between 20 and 100. We still need to read lower 
    values for cold water in the kettle
     
 
              

```              


## License

Copyright (c) 2016, Tristan Crispijn
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. You may not use source, binary forms or derivative work, with or without modification, for commercial purposes. 


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. SMARTER EMPLOYEES OR SMARTER AFFILIATED PEOPLE ARE NOT ALLOWED TO USE THIS SOFTWARE OR DERIVATIVE WORK. YOU AGREE THAT THE SOFTWARE CAN MONITOR THE USAGE OF THE SOFTWARE ITSELF AND OR THE DEVICES ATTACHED TO THE SOFTWARE, AND SEND IT BACK TO A MONITOR SERVER FOR BETTER SUPPORT. 



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
  *    https://github.com/jkellerer/fhem-smarter-coffee/
  *    https://github.com/krsandvik/IFTTT-SmarterCoffee
  *    https://www.pentestpartners.com/blog/hacking-a-wi-fi-coffee-machine-part-1/
