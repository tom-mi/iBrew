# iBrew

## Introduction

iBrew: iKettle 2.0 and Smarter Coffee Interface
iBrew: Python interface to iKettle 2.0 and Smarter Coffee

This includes a console, monitor, and command line interface.

iKettle 2.0 tested only

Alpha


### Requirements 

* python 2.7

### Installation

`git clone https://github.com/Tristan79/iBrew.git`

Download[source](https://github.com/Tristan79/iBrew/archive/master.zip) unpack and run iBrew


## iKettle 2.0 & Smarter Protocol

This interface was built using [Protocol](https://github.com/Tristan79/iBrew/blob/master/protocol.txt)

### References
*    https://github.com/Jamstah/libsmarteram2/
*    https://github.com/ian-kent/ikettle2/
*    https://github.com/athombv/am.smarter/
*    https://github.com/nanab/smartercoffee/
*    https://github.com/AdenForshaw/smarter-coffee-api

*    https://www.pentestpartners.com/blog/hacking-a-wi-fi-coffee-machine-part-1/
*    https://www.hackster.io/lahorde/from-a-14-kettle-to-an-ikettle-d2b3f7


## Console

```
Console options v0.1

  iKettle 2.0 & Smarter Coffee Commands
  info                   Device info
  status                 Show status
  [data]                 Send raw data to device

  iKettle 2.0 Commands
  off                    Turn off
  on                     Turn on
  base                   Show watersensor base value
  calibrate              Calibrates watersensor

  Smarter Coffee Commands
  cups [nr]              Set number of cups [1..12]
  grinder                Toggle grinder
  hotplate off           Turn hotplate off
  hotplate on            Turn hotplate on
  strength [s]           Set strength coffee [weak, medium or strong]

  WiFi Commands
  connect                Connect to wireless network
  firmware               Show firmware WiFi
  name [name]            Set wireless network [name] to access
  password [pw]          Set [password] of wireless network to access
  reset                  Reset WiFi
  scan                   Scan wireless networks
  setup                  Select and connect wireless network

  Help Commands
  examples               Show examples of commands
  messages               Show all known protocol messages
  message [id]           Show protocol message detail
  protocol               Show protocol structure

  Console Commands
  dump                   Toggle 'dump raw messages'
  joke                   Show joke
  quit                   Quit console
```
