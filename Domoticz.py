# -*- coding: utf8 -*-

import json
import urllib

#------------------------------------------------------
# DOMOTICZ INTERFACE
#
# Python interface to domoticz
#
# https://github.com/Tristan79/???
#
# 2016 Copyright © 2016 Tristan (@monkeycat.nl)
#
# CRAP WRAP v0.01
#------------------------------------------------------



#------------------------------------------------------
# DOMOTICZ INTERFACE CLASS
#------------------------------------------------------


class Domoticz:

    def __init__(self,server,secure = False):
        self.server = server
        self.secure = secure

    def base(self):
        s = ""
        if self.secure:
            s = "s"
        return "http" + s + "://" + self.server + "/json.htm?"

    def exists_hardware(self,name):
        url = self.base() + "type=hardware"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if "result" in data:
            for i in range(0,len(data["result"])):
                if name == data["result"][i]["Name"]:
                    return data["result"][i]["idx"]
        return "None"

    def use_virtual_hardware(self,name):
        self.hardware_idx = self.exists_hardware(name)
        if "None" == self.hardware_idx:
            nameurl = name.replace(" ", "%20")
            url = self.base() + "type=command&param=addhardware&htype=15&port=1&name=" + nameurl + "&enabled=true"
            response = urllib.urlopen(url)
            self.hardware_idx = self.exists_hardware(name)
            if "None" == self.hardware_idx:
                return False
        return True
    

    def exists_sensor(self,name):
        url = self.base() + "type=devices&filter=all&used=true&order=Name"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if "result" in data:
            for i in range(0,len(data["result"])):
                if name == data["result"][i]["Name"] and int(self.hardware_idx) == data["result"][i]["HardwareID"]:
                    return data["result"][i]["idx"]
        
        return "None"


    def use_virtual_sensor(self,name,type,options=""):
        nameurl = name.replace(" ", "%20")
        idx = self.exists_sensor(name)
        if "None" != idx:
            return idx
        if "None" == idx:
            url = self.base() + "type=createvirtualsensor&idx="+ self.hardware_idx + "&sensorname=" + nameurl +  "&sensortype=" + str(type)
            if options != "":
                url = url + "&sensoroptions=" + options
            response = urllib.urlopen(url)
            return self.exists_sensor(name)
        else:
            return "None"


    SensorTemperature = 80
    SensorHumidity    = 81
    SensorCustom      = 1004

    def print_type(self,type):
        if type == self.SensorTemperature:  return "Temperature"
        elif type == self.SensorHumidity:   return "Humidity"
        elif type == self.SensorCustom:     return "Custom"
        else:                               return "Unknown"


    # no check if right sensor....

    def get_custom(self,idx):
        url = self.base() + "type=devices&rid=" + idx
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data["result"][0]["Data"]


    def set_custom(self,idx,custom):
        if float(self.get_custom(idx)) != float(custom):
            url = self.base() + "type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue="+str(custom)
            response = urllib.urlopen(url)
            return True
        return False


    def get_temperature(self,idx):
        url = self.base() + "type=devices&rid=" + idx
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data["result"][0]["Temp"]

    def set_temperature(self,idx,temperature):
        if float(self.get_temperature(idx)) != float(temperature):
            url = self.base() + "type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue="+str(temperature)
            response = urllib.urlopen(url)
            return True
        return False

