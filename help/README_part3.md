
```


### Web Interface

This is a build in progress, please contribute!


### REST API

Start the web interface.


```http://ip:port/api```

The following links are available

```
/api/version
/api/devices
```

Which contains the ip which you can use to monitor or control individual devices.

```http://ip:port/api/ip```

The following links are available

```
/start
/stop
/join/name/(password)
/leave
/scan
/default
/settings/(v1/v2/v3/v4/)
/calibrate
/calibrate/base/(value)
/carafe
/singlecup
/hotplate/value
/grinder/bool
/cups/value
/strength/value
```

### Domoticz Bridge

Bridge to [Domoticz](http://domoticz.com). You are in full control!


iKettle Devices in Domoticz
![alt tag](https://raw.githubusercontent.com/Tristan79/iBrew/master/help/Domoticz.png)
   
```
