# iBrew Kettle Rattle

[iKettle 2.0](http://smarter.am/ikettle) and [Smarter Coffee](http://smarter.am/coffee) Interface


## Introduction
iBrew is a (python) interface to iKettle 2.0 and Smarter Coffee devices. It includes a console, monitor, command line interface, web interface and rest api. You can also use it in your own code. iKettle 2.0 v19 and SmarterCoffee v20 tested at the moment. Please share any other discoveries you made!

This means your machine is free! You can connect it yourself and do whatever you want with it. Like interface it with your favorite smarthome controller!

   Signed TRiXWooD

#### Versions
 * v0.0 Bean Grinder Pack
 * v0.1 White Tealeaf Edition
 * v0.2 Tea Noire Sweet
 * v0.3 Kettle Rattle <-- CURRENT VERSION
 * v0.4 Brewing on the 7th day (web interface) 
 * v0.5 Dumb Dump Limited Collector Edition (numbered, signed by author)
 * v1.0 Out of order! (the final cut!)
 
#### Upcoming for the last 3 versions  
 * Better error handling (sometimes it does not quit :-)
 * it also hangs if you scan wifi too much (luckily it reconnects)
 * Connecting in console mode... fails sometimes, and after reconnect is had strange data... stupid threads... missing...
 * Brew, heat, formula arguments (I have to figure out what is what, one cup at a time... 
 * Time arguments (have not figured that out)
 * Web interface & rest api (rest almost finished, web interface still have to create some pages) and introduce webroot & api key,...,...
 * History message is not finished
 * Fahrenheid not finished, please to not use.
 * can't start the web interface twice in console (i probably did not clean up)
 * if you send a message with an ..something was here...
 * v0.5 Missing Coffee Smarter codes (!)
 * messages everywhere from the monitor...
 * I broke domoticz, i decided I do not needed it anymore :-)
 * fix wireless with the same name
 
 
 
#### Contact
[Bugs or issues](https://github.com/Tristan79/iBrew/issues). Donations & other questions <tristan@monkeycat.nl>
If you have jokes on coffee, tea, hot chocolade, coffee machines or kettles, please post in the issues.

Still no coffee machine (so no web for that)! I could like to thank Ju4ia for letting me access his coffee machine remotely, so I could test the client code.


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
    carafe [state]         set carafe is required [on or off]
    cups [number]          set number of cups [1..12]
    grinder                use grinder
    filter                 use filter
    hotplate off           turn hotplate off
    hotplate on (minutes)  turn hotplate on (time in minutes)
    singlecup              return single coffee cup mode
    singlecup [state]      set single coffee cup mode [on or off]
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
    sweep (id)             [developer only] try (all or start with id) unknown command codes

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
   
### LICENSE

Copyright (c) 2016, Tristan Crispijn
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. You may not use source, binary forms or derivative work, with or without modification, for commercial purposes. 


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. SMARTER EMPLOYEES OR SMARTER AFFILIATED PEOPLE ARE NOT ALLOWED TO USE THIS SOFTWARE OR DERIVATIVE WORK. YOU AGREE THAT THE SOFTWARE CAN MONITOR THE USAGE OF THE SOFTWARE ITSELF AND OR THE DEVICES ATTACHED TO THE SOFTWARE, AND SEND IT BACK TO A MONITOR SERVER FOR BETTER SUPPORT. 

