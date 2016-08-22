
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
