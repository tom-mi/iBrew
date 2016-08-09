# iBrew White Tealeaf Edition
[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface

## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, and command line interface. You can also use it in your own code. iKettle 2.0 tested only.  Please share you Smarter Coffee codes or any other discoveries you made.

#### Please donate you raw codes
Someone please run ```iBrew``` sweep on there coffee machines and post the results in the issues.

#### Versions
 * v0.0 Bean Grinder Pack
 * v0.1 White Tealeaf Edition
 
Upcoming
 
 * v0.2 Tea Noir Suite
 - [x] simplify and better renaming console
 - [x] command scanfunction (sweep)
 - [x] search & add new reply messages (as possible)
 - [x] search & add new command messages (as possible)
 - [ ] Show message parameters
 - [x] WiFi Commands
 - [ ] WiFi Setup
 - [ ] Heat/Formula & Brew temperature/time controlled
 - [ ] When heating and fast temperature rise auto-shutdown (iKettle2)
 - [ ] Clean up code (better interface protocol...)
 - [ ] Clean up message descriptions
 - [ ] Fix Network code, it does not read the status messages so it get's backlogged...
 - [ ] Figure out the waterlevel (iKettle2)
 - [ ] Smarter codes
 
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

#### Setup
The file iBrewSettings.py contains the default settings. You can edit it with your favorite editor

## Usage

### Command Line Options
 The following commands are available at the command line:
 
```
Usage:
  iBrew [console command] (host)

  (host) ip4 format, ip6 format or host name
```

### Console
Start the console with the command `iBrew console`. The following commands are available within the console:

```

  iKettle 2.0 & Smarter Coffee Commands
  info                   Device info
  start                  Start the device
  status                 Show status
  stop                   Stop the device
  [data]                 Send raw data to device

  iKettle 2.0 Commands
  base                   Show watersensor base value
  calibrate              Calibrates watersensor
  default                Set default settings
  formula ()()           Heat kettle in formula mode
  heat ()()              Heat kettle
  settings               Set user settings
  store base [base]      Store watersensor base value

  Smarter Coffee Commands
  brew                   Brew coffee
  cups [number]          Set number of cups [1..12]
  grinder                Toggle grinder
  hotplate off           Turn hotplate off
  hotplate on            Turn hotplate on
  strength [strength]    Set strength coffee [weak, medium or strong]

  WiFi Commands
  connect                Connect to wireless network
  firmware               Show firmware WiFi
  name [name]            Set wireless network name to access
  password [password]    Set password of wireless network to access
  reset                  Reset WiFi
  scan                   Scan wireless networks

  Help Commands
  examples               Show examples of commands
  messages               Show all known protocol messages
  message [id]           Show protocol message detail
  protocol               Show protocol structure
  smarter                Show protocol

  Debug Commands
  dump                   Toggle 'dump raw messages'
  monitor                Monitor incomming traffic
  sweep [startcommand]   Try (all) unknown command codes

  Console Commands
  joke                   Show joke
  quit                   Quit console

```

## Links

#### Smart Kettles & Coffee Machines
  *    http://smarter.am/
  *    http://www.appkettle.co.uk
  *    https://www.hackster.io/lahorde/from-a-14-kettle-to-an-ikettle-d2b3f7
      
#### References
  *    https://github.com/Jamstah/libsmarteram2/
  *    https://github.com/ian-kent/ikettle2/
  *    https://github.com/athombv/am.smarter/
  *    https://github.com/nanab/smartercoffee/
  *    https://github.com/AdenForshaw/smarter-coffee-api
  *    https://domoticz.com/forum/viewtopic.php?f=23&t=12837
  *    https://www.pentestpartners.com/blog/hacking-a-wi-fi-coffee-machine-part-1/
