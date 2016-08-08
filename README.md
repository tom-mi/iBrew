# iBrew

#### Introduction

iBrew: iKettle 2.0 and Smarter Coffee Interface
iBrew: Python interface to iKettle 2.0 and Smarter Coffee

This includes a console, monitor, and command line interface.

iKettle 2.0 tested only

Alpha


#### Requirements 

* python 2.7

#### Installation

Download and unpack and run iBrew

#### Console

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

