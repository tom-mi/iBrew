# iBrew Tea Noire Sweet
[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface

## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface and bridge to [Domoticz](http://domoticz.com). You can also use it in your own code. iKettle 2.0 tested only. Please share you Smarter Coffee codes or any other discoveries you made.

#### Please donate you raw codes
Someone please run ```iBrew``` sweep on there coffee machines and post the results in the issues.

#### Versions
 * v0.0 Bean Grinder Pack
 * v0.1 White Tealeaf Edition
 * v0.2 Tea Noir Sweet
 
Upcoming
 
 * v0.3 Kettle Rattle
 
 ToDo:
 - [ ] WiFi Setup!!! <- still can't let it connect to my router... 
 - [ ] Heat/Formula & Brew/Hotplate temperature/time controlled
 - [ ] When heating and fast temperature rise auto-shutdown (iKettle2)
 - [ ] Fix Network code??? (usefull???), it does not read the status messages so it get's backlogged in console...
 - [ ] Figure out the waterlevel (iKettle2)
 - [ ] Server???
 - [ ] History/SetTime missing time
 - [ ] Settings missing parameters
 
#### Donate
Please donate raw codes or donate (for) a (working) Smarter Coffee (interface), can not test without one or without help!

#### Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). Donations & other questions <tristan@monkeycat.nl>

#### iKettle 2.0 & Smarter Protocol
This interface was built using this [protocol](https://github.com/Tristan79/iBrew/blob/master/smarter.txt) description.

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
 
```

Usage: iBrew (dump) [arguments] (host)


       host             host address (format: ip4, ip6, fqdn)
       dump             dump message enabled
       arguments        see console commands
```

### Console
Start the console with the command `iBrew console`. The following commands are available within the console,
you can also use them on the command line as arguments:

```
 
  iKettle 2.0 & Smarter Coffee Commands
    info                   Device info
    history                Action history
    reset                  Reset device to default
    start                  Start the device
    status                 Show status
    stop                   Stop the device
    [data]                 Send raw data to device

  iKettle 2.0 Commands
    base                   Show watersensor base value
    base [base]            Store watersensor base value
    calibrate              Calibrates watersensor
    default                Set default settings
    formula ()()           Heat kettle in formula mode
    heat ()()              Heat kettle
    settings               Show user settings
    settings [] [] [] []   Store user settings

  Smarter Coffee Commands
    brew                   Brew coffee
    cups [number]          Set number of cups [1..12]
    grinder                Toggle grinder
    hotplate off           Turn hotplate off
    hotplate on ()         Turn hotplate on
    strength [strength]    Set strength coffee [weak, medium or strong]

  WiFi Commands
    connect                Connect to wireless network
    clear                  Resets WiFi to default
    firmware               Show firmware WiFi
    name [name]            Set wireless network name to access
    password [password]    Set password of wireless network to access
    scan                   Scan wireless networks

  Help Commands
    examples               Show examples of commands
    messages               Show all known protocol messages
    message [id]           Show protocol message detail of message [id]
    protocol               Show protocol structure information
    smarter                Show whole protocol including messages

  Bridge Commands
    domoticz               Show domoticz bridge help

  Debug Commands
    dump                   Toggle 'dump raw messages'
    console                Start console [Command line only]
    monitor                Monitor incomming traffic
    sweep (id)             Try (all or start with id) unknown command codes

  Console Commands
    joke                   Show joke
    quit                   Quit console [Console only]


```


### Domoticz Bridge
Bridge between iKettle 2.0 and [Domoticz](http://domoticz.com). Its auto-creates 4 devices in domoticz, if not yet created. Monitors the kettle and update the domoticz devices accordingly.
  
  *  Water Temperature in ºC (temperature device)
  *  Water Height (custom device)      
  *  Kettle on base (motion device)      
  *  Kettle status (text device)        


```

  Domoticz Bridge

  *** Currently iKettle 2.0 Only ***

  Usage:

    iBrew domoticz domcon name kettle

  Where:
  
    domocon         Connection string to domoticz, [host:port] or [username:password@host:port]
    name            Name of your kettle. The name may contain spaces
    kettle          Connection string to iKettle 2.0, [host]
    
    host            Format: ip4, ip6, fqdn
    

  Notes:
    It will auto-create the devices in Domoticz
    Tested on Domoticz v3.52
  
  Examples:
  
    iBrew domoticz sofia:$ecrit@localhost:8080 Kettle Kitchen 192.168.4.1
    iBrew domoticz 10.0.0.1:9001 Kettle Office 192.168.10.13
    iBrew dump domoticz 10.0.0.1:9001 Kettle Office 192.168.10.13
    iBrew domoticz localhost:8080 Kettle 
  
```              


## Links

#### Smart Kettles & Coffee Machines
  *    http://smarter.am/
  *    http://www.appkettle.co.uk/
  *    https://www.hackster.io/lahorde/from-a-14-kettle-to-an-ikettle-d2b3f7

#### Smarthome Controller
  *    https://domoticz.com/  
      
#### References
  *    https://github.com/Jamstah/libsmarteram2/
  *    https://github.com/ian-kent/ikettle2/
  *    https://github.com/athombv/am.smarter/
  *    https://github.com/nanab/smartercoffee/
  *    https://github.com/AdenForshaw/smarter-coffee-api
  *    https://domoticz.com/forum/viewtopic.php?f=23&t=12837
  *    https://www.pentestpartners.com/blog/hacking-a-wi-fi-coffee-machine-part-1/
