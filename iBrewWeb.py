# -*- coding: utf-8 -*-

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import socket
import time
import threading
import datetime

import os
from smarter.SmarterInterface import *

from iBrewBonjour import *
from iBrewJokes import *
from iBrewFolders import AppFolders

import traceback

#------------------------------------------------------
# iBrew
#
# Web & JSON REST interface to Smarter Appliances
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2017 Tristan (@monkeycat.nl). All Rights Reserved
#
# The Dream Tea
#------------------------------------------------------


def custom_get_current_user(handler):
    #user = handler.get_secure_cookie("user")
    #if user:
    user = "#NONE#"
    return user


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return custom_get_current_user(self)

    @property
    def webroot(self):
        return self.application.webroot
        
    @property
    def devices(self):
        return self.application.clients



class GenericAPIHandler(BaseHandler):
    SUPPORTED_METHODS = ("GET", "POST", "SUBSCRIBE")
    def setContentType(self):
        self.add_header("Content-type","application/json; charset=UTF-8")

    def validateAPIKey(self):
        api_key = self.get_argument("apikey", default="")
        if api_key == "APIKEY":
            return True
        else:
            raise tornado.web.HTTPError(400)
            return False

#------------------------------------------------------
# WEB GUI PAGES
#------------------------------------------------------


class GenericPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,page):
        if os.path.isfile(os.path.join(os.path.dirname(__file__), self.webroot)+page+".html"):
            self.render(page+".html")
        else:
#            self.render(webroot+"somethingwrong.html")
            self.render("index.html",clients = self.application.clients,joke = iBrewJokes().joke())


class MainPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("index.html",clients = self.application.clients,joke = iBrewJokes().joke())


class ServerPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("statistics.html",clients = self.application.clients)


class InfoPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("info/info.html")


class WirelessPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,ip):
        try:
            c = self.application.clients[ip]
        except:
            c = None
            # FIX!
        self.render("device/wireless.html",client = c)


class APIPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        d = dict()
        for ip in self.application.clients:
            client = self.application.clients[ip]
            d.update({client.host : Smarter.device_to_string(client.deviceId)})
        self.render("info/api.html",devices = d,joke = iBrewJokes().joke())


class ProtocolPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("info/protocol.html")


class MessagesPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("info/messages.html",status = Smarter.StatusToJSON(),commands = Smarter.CommandToJSON(), responses = Smarter.ResponseToJSON())


class LicensePageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("info/license.html")



class ArgumentsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("info/arguments.html",status = Smarter.StatusToJSON(),commands = Smarter.CommandToJSON(), responses = Smarter.ResponseToJSON())


class GroupsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("info/groups.html",status = Smarter.StatusToJSON(),commands = Smarter.CommandToJSON(), responses = Smarter.ResponseToJSON())


class MessagePageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,message):
        try:
            mid = Smarter.code_to_number(message)
        except Exception:
            self.render("info/protocol.html",status = Smarter.StatusToJSON(),commands = Smarter.CommandToJSON(), responses = Smarter.ResponseToJSON())
        self.render("info/message.html", id = mid)


class SettingsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,ip):
        if ip in self.application.clients:
            c = self.application.clients[ip]
            self.render("settings.html",client = c)
        else:
            self.render("somethingwrong.html")


class StatsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,ip):
        if ip in self.application.clients:
            c = self.application.clients[ip]
            self.render("device/statistics.html",client = c)
        else:
            self.render("somethingwrong.html")



#------------------------------------------------------
# REST PAGES
#------------------------------------------------------

#------------------------------------------------------
# Devices Handler
#------------------------------------------------------


def encodeFirmware(device,version):
    return { 'version'   : version, 'certified' : Smarter.firmware_verified(device,version) }


def encodeRelay(enabled,version,host):
    if enabled:
        return { 'version' : version,
                 'host'    : host }
    else:
        return False

def encodeDevice(client):
    mode = 'normal'
    if client.simulate:
        mode = 'simulation'
    elif client.emulate:
        mode = 'emulation'
    elif client.bridge:
        mode = 'bridge'

    cc = client.connected
    if client.simulate or client.bridge:
        cc = True

    return { 'model'       : Smarter.device_to_string(client.deviceId),
             'mode'        : mode,
             'network'     : { 'connection'  : { 'directmode'  : client.isDirect,
                                                 'host'        : client.host,
                                                 'port'        : client.port,
                                                 'connected'   : cc,
                                                 'relay'       : encodeRelay(client.remoteRelay,client.remoteRelayVersion,client.remoteRelayHost)
                                               },
                               'relay'       : { 'bind'   : client.relayHost,
                                                 'port'   : client.relayPort,
                                                 'active' : client.relay
                                               },
                              },
             'firmware'    : encodeFirmware(client.deviceId,client.version)
            }

class DeviceHandler(GenericAPIHandler):
    
    def get(self, ip):
        response = { 'error': 'no device' }
        if ip in self.application.clients:
            client = self.application.clients[ip]
            
            if client.isKettle:
                response = { 'appliance'   : encodeDevice(client),
                             'sensors'     : { 'waterlevel'  : { 'raw'    : client.waterSensor,
                                                                 'stable' : client.waterSensorStable,
                                                                 'base'   : client.waterSensorBase
                                                               },
                                               'base'        : Smarter.string_base_on_off(client.onBase),
                                               'temperature' : { 'raw'    : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.temperature),
                                                                              'celsius'    : client.temperature
                                                                            },
                                                                 'stable' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.temperatureStable),
                                                                              'celsius'    : client.temperatureStable
                                                                            }
                                                               }
                                                               
                                             },
                             'status'      : Smarter.status_kettle_description(client.kettleStatus),
                             'settings'    : { 'default'     : { 'temperature' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.defaultTemperature),
                                                                                   'celsius'    : client.defaultTemperature,
                                                                                   'prefered'   : Smarter.temperature_metric_to_string()
                                                                                 },
                                                                 'keepwarm'    : client.defaultKeepWarmTime,
                                                                 'formula'     : { 'use'     : client.defaultFormula,
                                                                                   'temperature' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.defaultFormulaTemperature),
                                                                                                     'celsius' : client.defaultFormulaTemperature
                                                                                                   }
                                                                                  }
                                                               }
                                             }
                            }
                            
            elif client.isCoffee:
            
                if client.mode == Smarter.CoffeeCupMode:
                    mode = 'cup'
                else:
                    mode = 'carafe'
                
                if client.carafeRequired:
                    req = "required"
                else:
                    req = "optional"
                response = { 'appliance'   : encodeDevice(client),
                             'sensors'     : { 'hotplate'   : client.hotPlateOn,
                                               'heater'     : client.heaterOn,
                                               'grinder'    : client.grinderOn,
                                               'waterlevel' : client.waterLevel
                                              },
                             'status'      : { 'working'     : client.working,
                                               'ready'       : client.ready,
                                               'cups'        : client.cupsBrew,
                                               'carafe'      : client.carafe,
                                               'enoughwater' : client.waterEnough,
                                               'timerevent'  : client.timerEvent
                                             },
                             'settings'    : { 'default'       : { 'cups'       : client.defaultCups,
                                                                   'strength'   : Smarter.strength_to_string(client.defaultStrength),
                                                                   'source'     : Smarter.grind_to_string(client.defaultGrind),
                                                                   'hotplate'   : client.defaultHotPlate
                                                                 },
                                               'current'       : { 'cups'       : client.cups,
                                                                   'strength'   : Smarter.strength_to_string(client.strength),
                                                                   'source'     : Smarter.grind_to_string(client.grind),
                                                                   'hotplate'   : client.hotPlate
                                                                 },
                                               'carafe'         : req,
                                               'mode'           : mode
                                             },
                            }
        self.setContentType()
        self.write(response)


class DevicesHandler(GenericAPIHandler):
    def get(self):
        devices, relay = Smarter.find_devices(Smarter.Port)
        response = {}
        for device in devices:
            x = -1
            for j in range(0,len(relay)):
                if device[0] == relay[j][0]:
                    x = j
        
            if x != -1:
                r = encodeRelay(True,relay[x][1],relay[x][2])
            else:
                r = encodeRelay(False,0,"")

            response[device[0]] = { 'type'        : { 'description'  : Smarter.device_to_string(device[1]),
                                                      'id'          : device[1]
                                                    },
                                    'relay'       : r,
                                    'firmware'    : encodeFirmware(device[1],device[2])
                                  }
        self.setContentType()
        self.write(response)


class UnknownHandler(GenericAPIHandler):
    def get(self):
        response = { 'error' : { 'code' : '0', 'message' : 'Request unavailable' }}
        self.setContentType()
        self.write(response)



#------------------------------------------------------
# Kettle heat
#------------------------------------------------------


class BeverageHandler(GenericAPIHandler):
    def get(self,ip,beverage):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            
            if client.isKettle:
                if beverage == "coffee":
                    client.kettle_heat_coffee()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif beverage == "white":
                    client.kettle_heat_white_tea()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif beverage == "milk":
                    client.kettle_heat_milk()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif beverage == "black":
                    client.kettle_heat_black_tea()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif beverage == "green":
                    client.kettle_heat_green_tea()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif beverage == "oelong":
                    client.kettle_heat_oelong_tea()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif beverage == "boil":
                    client.kettle_boil()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                else:
                    response = { 'error': 'wrong beverage use coffee, white, black, green, oelong, boil' }
                
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class HeatHandler(GenericAPIHandler):
    def get(self,ip,temperature,keepwarm):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                client.kettle_heat(int(temperature),int(keepwarm))
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class FormulaHandler(GenericAPIHandler):
    def get(self,ip,temperature,keepwarm):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                client.kettle_formula_heat(int(temperature),int(keepwarm))
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)

#------------------------------------------------------
# Kettle calibration
#------------------------------------------------------


class CalibrateHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                client.kettle_calibrate()
                # fix kettle_calibrate_offbase
                response = { 'base'            : client.waterSensorBase,
                             'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CalibrateBaseHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                client.kettle_calibrate_base()
                response = { 'base'            : client.waterSensorBase,
                             'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CalibrateStoreBaseHandler(GenericAPIHandler):
    def get(self,ip,base):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                client.kettle_calibrate_store_base(Smarter.string_to_watersensor(base))
                response = { 'base'            : client.waterSensorBase,
                             'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)



#------------------------------------------------------
# Wifi operation
#------------------------------------------------------


class WifiScanHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            #if client.connected:
            try:
                client.wifi_scan()
        
                networks = {}
                for i in range(0,len(client.Wifi)):
                    networks.update( { client.Wifi[i][0] : { 'signal'  : str(client.Wifi[i][1]),
                                                             'quality' : Smarter.dbm_to_quality(int(client.Wifi[i][1]))
                                                           }
                                     })
                response = { 'networks'   : networks,
                             'directmode' : client.isDirect
                           }
            except Exception:
                response = { 'error': 'no communication' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class WifiJoinHandler(GenericAPIHandler):
    def get(self,ip,name,password):
        if ip in self.application.clients:
            self.application.clients[ip].wifi_join(name,password)
            response = { 'success': 'joining wireless network' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class WifiDirectHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            self.application.clients[ip].wifi_direct()
            response = { 'success': 'left wireless network' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)



#------------------------------------------------------
# Settings
#------------------------------------------------------


class StoreSettingsHandler(GenericAPIHandler):
    def get(self,ip,x1,x2,x3,x4):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            client.device_store_settings(x1,x2,x3,x4)
            response = { 'command'  : Smarter.status_command(client.commandStatus) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class SettingsHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            client.device_settings()
            response = { 'temperature' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.defaultTemperature),
                                           'celsius'    : client.defaultTemperature,
                                           'prefered'   : Smarter.temperature_metric_to_string()
                                         },
                         'keepwarm'    : client.defaultKeepWarmTime,
                         'formula'     : { 'use'         : client.defaultFormula,
                                           'temperature' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.defaultFormulaTemperature),
                                                             'celsius'    : client.defaultFormulaTemperature
                                                           }
                                         }
                        }

        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class SettingsDefaultHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            client.device_default()
            response = { 'command'  : Smarter.status_command(client.commandStatus) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


#------------------------------------------------------
# Coffee settings
#------------------------------------------------------


class BrewHandler(GenericAPIHandler):
    def get(self,ip,cups,hotplate,grind,strength):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_brew(Smarter.string_to_cups(cups),Smarter.string_to_hotplate(hotplate),Smarter.string_to_bool(grind),Smarter.string_to_strength(strength))
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class BrewDefaultHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_brew_default()
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class DescaleHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
            
                client.coffee_descale()
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class StrengthHandler(GenericAPIHandler):
    def get(self,ip,strength):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            
            if client.isCoffee:
                if strength == Smarter.CoffeeStringWeak:
                    client.coffee_weak()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif strength == Smarter.CoffeeStringMedium:
                    client.coffee_medium()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                elif strength == Smarter.CoffeeStringStrong:
                    client.coffee_strong()
                    response = { 'command'  : Smarter.status_command(client.commandStatus) }
                else:
                    response = { 'error': 'wrong strength use weak, medium or strong' }   
                
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CupsHandler(GenericAPIHandler):
    def get(self,ip,cups):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_cups(Smarter.string_to_cups(cups))
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class HotPlateOnHandler(GenericAPIHandler):
    def get(self,ip,timer):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_hotplate_on(timer)
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class HotPlateOffHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_hotplate_off()
                response = { 'command'  : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CarafeOnHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_carafe_required_on()
                response = { 'carafe' : 'required',
                             'command' : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CarafeOffHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_carafe_required_off()
                response = { 'carafe' : 'optional',
                             'command' : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CarafeModeHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_carafe_mode()
                response = { 'mode'           : 'carafe',
                             'command' : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CupModeHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_cup_mode()
                response = { 'mode'      : 'cup',
                             'command'   : Smarter.status_command(client.commandStatus) }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class BeansHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_beans()
                response = { 'error'      : 'none' }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class FilterHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_filter()
                response = { 'command'      : 'success' }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


#------------------------------------------------------
# STOP START COMMANDS
#------------------------------------------------------


class StopHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            client.device_stop()
            response = { 'command' : Smarter.status_command(client.commandStatus) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class StartHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            client.device_start()
            response = { 'command' : Smarter.status_command(client.commandStatus) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


#------------------------------------------------------
# REMOTE BLOCKS
#------------------------------------------------------


def encodeRules(rulesIn,rulesOut):

    groupsIn,  idsIn  = Smarter.idsListEncode(rulesIn)
    groupsOut, idsOut = Smarter.idsListEncode(rulesOut)
    return { 'in' :  { 'groups' : list(groupsIn),
                       'ids'    : list(idsIn)
                     },
             'out' : { 'groups' : list(groupsOut),
                       'ids'    : list(idsOut)
                     }
            }


def encodeRules():
    #FIX
    return { 'patch' :  'not implemented yet' }


class BlockHandler(GenericAPIHandler):
    def get(self,ip,block):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if block[-1] == '/':
                block = block[0:-1]
            print(block)
            client.block(block)
            response = encodeRules(client.rulesIn,client.rulesOut)
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class UnblockHandler(GenericAPIHandler):
    def get(self,ip,unblock):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if unblock[-1] == '/':
                unblock = unblock[0:-1]
            print(unblock)
            client.unblock(unblock)
            response = encodeRules(client.rulesIn,client.rulesOut)
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class PatchHandler(GenericAPIHandler):
    def get(self,ip,patch):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if patch[-1] == '/':
                patch = patch[0:-1]
            client.patch(patch)
            response = encodePatch()
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class PatchesHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            response = encodePatch(client.rulesIn,client.rulesOut)
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)

class RulesHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            response = encodeRules(client.rulesIn,client.rulesOut)
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)

#------------------------------------------------------
# Misc
#------------------------------------------------------


class JokeHandler(GenericAPIHandler):
    def get(self,ip=""):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if   client.isCoffee: joke = iBrewJokes().coffee()
            elif client.isKettle: joke = iBrewJokes().tea()
            response = { 'question' : joke[0] , 'answer' : joke[1] }
        elif ip == "":
            joke = iBrewJokes().joke()
            response = { 'question' : joke[0] , 'answer' : joke[1] }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class StatsHandler(GenericAPIHandler):
    def get(self,ip=""):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            
            if client.isKettle:
                device = { 'heater'     : client.countHeater,
                           'keepwarm'   : client.countKeepWarm,
                           'removed'    : client.countKettleRemoved
                        }
            elif client.isCoffee:
                device = { 'heater'     : client.countHeater,
                           'grinder'    : client.countGrinderOn,
                           'hotplate'   : client.countHotPlateOn,
                           'removed'    : client.countCarafeRemoved
                         }
            else:
                device = {}
            
            response = { 'messages'         : { 'session' : { 'send'      : { 'count' : client.sendCount,
                                                                          'bytes' : client.sendBytesCount},
                                                          'read'      : { 'count' : client.readCount,
                                                                          'bytes' : client.readBytesCount},
                                                          'command'   : client.commandCount,
                                                          'response'  : client.responseCount
                                                         },
                                             'total'    : { 'send'      : { 'count' : client.totalSendCount,
                                                                          'bytes' : client.totalSendBytesCount},
                                                          'read'      : { 'count' : client.totalReadCount,
                                                                          'bytes' : client.totalReadBytesCount}
                                                         # 'command'   : client.commandCount,
                                                         # 'response'  : client.responseCount
                                                         }
                                                },

                         'sessions'      : client.sessionCount,
                         client.deviceId    : device
                        }
        
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)



class MessagesHandler(GenericAPIHandler):
    def get(self):
       
        response = { 'status'  : Smarter.StatusToJSON(),
                     'commands'  : Smarter.CommandToJSON(),
                     'responses' : Smarter.ResponseToJSON()
                    }

        self.setContentType()
        self.write(response)



class VersionHandler(GenericAPIHandler):
    def get(self):
        response = { 'description': 'iBrew REST API',
                     'version'    : self.application.version,
                     'copyright'  : { 'year'   : '2017',
                                      'holder' : 'Tristan Crispijn'
                                    }
                    }
        self.setContentType()
        self.write(response)

#------------------------------------------------------
# Triggers
#------------------------------------------------------


class TriggerHandler(GenericAPIHandler):

    def get(self, ip, group, trigger, http, url):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            try:
                print("$$$$$$$")
                print("$$$$$$$")
                print(http+url)
                print("$$$$$$$")
                print("$$$$$$$")
                client.triggerAdd(group,trigger,http+url)
                response = { 'command' : 'success' }
            except Exception as e:
                response = { 'error' : str(e) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)



class UnTriggerHandler(GenericAPIHandler):

    def get(self, ip, group, trigger):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            try:
                client.triggerDelete(group,trigger)
                response = { 'command' : 'success' }
            except Exception as e:
                response = { 'error' : str(e) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class GroupUnTriggerHandler(GenericAPIHandler):

    def get(self, ip, group):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            try:
                client.triggerGroupDelete(group)
                response = { 'command' : 'success' }
            except Exception as e:
                response = { 'error' : str(e) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)



class TriggersHandler(GenericAPIHandler):

    def get(self, ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            response = {}
            for j in client.triggersGroups:
                tk = {}
                one = False
                two = False
                for i in Smarter.triggersKettle:
                    action = client.triggerGet(j[0],Smarter.triggersKettle[i][0].upper())
                    if action != "":
                        tk[Smarter.triggersKettle[i][0].upper()] = action
                        one = True
                tc = {}
                for i in Smarter.triggersCoffee:
                    action = client.triggerGet(j[0],Smarter.triggersCoffee[i][0].upper())
                    if action != "":
                        two = True
                        tc[Smarter.triggersCoffee[i][0].upper()] = action
                if one and two:
                    response[j[0]] = { 'iKettle2.0' : tk, 'SmarterCoffee' : tc }
                elif one:
                    response[j[0]] = { 'iKettle2.0' : tk }
                elif two:
                    response[j[0]] = { 'SmarterCoffee' : tc }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class TriggersGroupHandler(GenericAPIHandler):

    def get(self, ip, group):
        if ip in self.application.clients:
            if group[-1] == '/':
                group = group[:-1]

            client = self.application.clients[ip]
            if client.isTriggersGroup(group):
                response = {}
                j = client.getGroup(group)
                tk = {}
                one = False
                two = False
                for i in Smarter.triggersKettle:
                    action = client.triggerGet(j[0],Smarter.triggersKettle[i][0].upper())
                    if action != "":
                        tk[Smarter.triggersKettle[i][0].upper()] = action
                        one = True
                tc = {}
                for i in Smarter.triggersCoffee:
                    action = client.triggerGet(j[0],Smarter.triggersCoffee[i][0].upper())
                    if action != "":
                        two = True
                        tc[Smarter.triggersCoffee[i][0].upper()] = action
                if one and two:
                    response = { 'iKettle2.0' : tk, 'SmarterCoffee' : tc }
                elif one:
                    response = { 'iKettle2.0' : tk }
                elif two:
                    response = { 'SmarterCoffee' : tc }
            else:
                response = { 'error': 'trigger group not found' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)

#-----------------------------------------------------
#SmartThings
#----------------------------------------------------
class SmartThingsHandler(GenericAPIHandler):

    def subscribe(self, ip):
        cb_url = self.request.headers.get("Callback")[1:-1]
        print(cb_url)
        if ip in self.application.clients:
            client = self.application.clients[ip]
            try:
                print("$$$$$$$")
                print("$$$$$$$")
                print(cb_url)
                print("$$$$$$$")
                print("$$$$$$$")
                client.triggerAdd("SmartThings","TEMPERATURE", cb_url )
                client.triggerAdd("SmartThings","KETTLEBUSY", cb_url )
                client.triggerAdd("SmartThings","KETTLEHEATER", cb_url )
                client.triggerAdd("SmartThings","ONBASE", cb_url )
                response = { 'command' : 'success' }
            except Exception as e:
                response = { 'error' : str(e) }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)



#------------------------------------------------------
# Legacy
#------------------------------------------------------

def encodeLegacy(client):
    cc = client.connected
    if client.simulation or client.bridge:
        cc = True
    
    t = "Off"
    if client.temperatureSelect:
        t = SmarterLegacy.string_response(client.temperature)
    w = "Off"
    if client.keepwarmSelect:
        t = SmarterLegacy.string_response(client.keepwarm)

    mode = 'normal'
    if client.simulation:
        mode = 'simulation'
    elif client.emulation:
        mode = 'emulation'
    elif client.bridge:
        mode = 'bridge'
    return { 'appliance' : { 'model'       : 'iKettle',
                             'mode'        : mode,
                             'firmware'    : { 'version'   : 1,
                                               'certified' : 'iBrew certified firmware'
                                             },
                             'network'     : { 'connection'  : { 'host'        : client.host,
                                                                 'port'        : client.port,
                                                                 'active'      : cc
                                                               },
                                               'relay'       : { 'bind'   : client.relayHost,
                                                                 'port'   : client.relayPort,
                                                                 'active' : client.relay
                                             },
                                                #  'relay'       : encodeRelay(client.remoteRelay,client.remoteRelayVersion,client.remoteRelayHost),
                                             }
  
                           },
             'sensors'   : { 'heater'  : client.heaterOn,
                             'warming' : client.keepwarmOn,
                             'onbase'  : client.onBase
                           },
             'status'    : { 'overheated'       : client.overheated,
                             'keepwarmfinished' : client.keepwarmFinished,
                             'heatingfinished'  : client.heatingFinished
                           },
             'settings'  : { 'temperature' : t,
                             'keepwarm'    : w
                           },

           }


class LegacyHandler(GenericAPIHandler):

    def get(self, ip, command):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                try:
                    print(command)
                    if command != "":
                        client.iKettle.send(command)
                    response = encodeLegacy(client.iKettle)
                # FIX for right exception
                except Exception as e:
                    print(str(e))
                    response = { 'error' : 'failed to send command' }
            else:
                response = { 'error': 'need kettle' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


#------------------------------------------------------
# REST INTERFACE
#------------------------------------------------------


class iBrewWeb(tornado.web.Application):

    version = '0.90a'
    
    def start(self):
        tornado.ioloop.IOLoop.instance().start()
    
    
    def autoconnect(self):
        
        #if not self.isRunning:
        #    return
        devices, relay = Smarter.find_devices(Smarter.Port)
        Smarter.print_devices_found(devices,relay)
        
        reconnect = 7
        
        for ip in list(self.clients.keys()):
            client = self.clients[ip]
            #print "Checking " + ip
            if not client.connected:
                if self.reconnect_count[ip] < 7:
                    #print "Trying " + ip
                    self.reconnect_count[ip] += 1
                    try:
                        if self.dump:
                            logging.info("[" + ip + "] Auto-connect attempt " + str(self.reconnect_count[ip]))
                        client.connect()
                        try:
                            threading.Thread(target=client.device_all_settings)
                        except Exception as e:
                            logging.info(e)
                    except Exception:
                        client.disconnect()
                else:
                    client.disconnect()
                    if self.dump:
                        logging.warning("[" + ip + "] Auto-connect tried " + str(reconnect) + " attempts, removing")
                    del self.clients[ip]
                    del self.reconnect_count[ip]
            else:
                self.reconnect_count[ip] = 0


        for device in devices:
            if device[0] not in self.clients:
                try:
                    if self.dump:
                        logging.info("[" + device[0] + "] Adding Web Device")
                    client = SmarterInterface(AppFolders.settings() + "/")
                    client.events = self.events
                    client.deviceId = device[1]
                    client.device = Smarter.device_to_string(device[1])
                    client.version = device[2]
                    client.dump = self.dump
                    client.dump_status = self.dump
                    client.setHost(device[0])
                    client.connect()
                    self.clients[device[0]] = client
                    #client.device_all_settings()
                    threading.Thread(client.device_all_settings())
                    self.reconnect_count[device[0]] = 0
                    logging.info("iBrew Web Server: " + client.string_connect_status())
                except Exception:
                    client.disconnect()
                    pass #raise SmarterError(WebServerListen,"Web Server: Couldn't open socket on port" + str(self.port))
            else:
                client = self.clients[device[0]]
                if not client.connected:
                    self.reconnect_count[device[0]] += 1
                    client.connect()


        
        if self.host != "":
            ip = socket.gethostbyname(self.host)
            if ip not in self.clients:
                try:
                    if self.dump:
                        logging.info("[" + ip + "] Adding Web Device")
                    client = SmarterInterface(AppFolders.settings() + "/")
                    client.events = self.events
                    client.setHost(self.host)
                    client.port = self.sport
                    client.dump = self.dump
                    client.dump_status = self.dump
                    client.connect()
                    self.clients[ip] = client
                    #client.device_all_settings()
                    threading.Thread(client.device_all_settings())
                    self.reconnect_count[ip] = 0
                    logging.info("iBrew Web Server: " + client.string_connect_status())
                except Exception:
                    client.disconnect()
                    pass # raise SmarterError(WebServerListen,"Web Server: Couldn't open socket on port" + str(self.port))

        if self.isRunning:
            self.threadAutoConnect = threading.Timer(15, self.autoconnect)
            self.threadAutoConnect.start()


    def __init__(self,webroot=""):
        self.isRunning = False
        self.webroot = webroot
        self.clients = dict()
        self.thread = None
        self.reconnect_count = dict()
        self.events = False

    def __del__(self):
        self.kill()
    
    
    def kill(self):
        self.isRunning = False
        deadline = time.time() + 3

        try:
            self.threadAutoConnect.cancel()
        except Exception:
            pass
        try:
            for ip in self.clients:
                self.clients[ip].trash()
        except Exception:
            raise SmarterError(WebServerStopMonitor,"Web Server: Could not stop monitors")
            
        try:
            io_loop = tornado.ioloop.IOLoop.instance()
     
            def stop_loop():
                now = time.time()
                if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                    io_loop.add_timeout(now + 1, stop_loop)
                else:
                    io_loop.stop()
        
            stop_loop()

        except Exception:
            raise SmarterError(WebServerStopMonitorWeb,"Web Server: Could not stop webserver monitor")

        try:
            if self.thread:
                if self.thread.isAlive():
                    self.thread.join()
        except Exception:
            raise SmarterError(WebServerStopWeb,"Web Server: Could not stop webserver")


    def run(self,bind="",port=Smarter.Port-1,dump=False,host="",sport=Smarter.Port):
        self.port = port
        self.isRunning = False
        self.dump = dump
        self.host = host
        self.sport = port
        self.bind = bind
        
        try:
        
            self.listen(self.port, no_keep_alive = True, address=self.bind)
        except Exception:
            logging.error("Web Server: Couldn't open socket on port " + self.bind + ":" +str(self.port))
            raise SmarterError(WebServerListen,"Web Server: Couldn't open socket on port " + self.bind + ":" + str(self.port))

        try:
            self.autoconnect()
        except KeyboardInterrupt:
            self.kill()
            raise SmarterError(WebServerStartFailed,"Web Server: Couldn't start on port "+ self.bind + ":" + str(self.port))
            
        try:
            settings = {
                "debug"         : self.dump,
                "template_path" : os.path.join(AppFolders.appBase(), 'web'),
                "static_path"   : os.path.join(AppFolders.appBase(), 'resources'),
                "static_url_prefix" : self.webroot + "/resources/", }

            handlers = [
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/status/?",DeviceHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/?",CalibrateHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/legacy/(|status|5|10|20|warm|65|80|95|100|heat|stop)/?",LegacyHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/base/?",CalibrateBaseHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/base/([0-9]+)/?",CalibrateStoreBaseHandler),

                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/heat/([0-9]+)/([0-9]+)/?",HeatHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/brew/([0-9]+)/([0-9]+)/(false|true|on|off|beans|filter)/(weak|medium|strong)/?",BrewHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/formula/([0-9]+)/([0-9]+)/?",FormulaHandler),

                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/beans/?",BeansHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/filter/?",FilterHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/descale/?",DescaleHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/brew/default/?",BrewDefaultHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/filter/?",FilterHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/carafe/off?",CarafeOffHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/mode/cup/?",CupModeHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/mode/carafe/?",CarafeModeHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/hotplate/on/([0-9]+)/?",HotPlateOnHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/hotplate/off/?",HotPlateOffHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/cups/([0-9]+)/?",CupsHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/(weak|normal|strong)/?",StrengthHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/(boil|coffee|white|green|black|oelong|milk)/?",BeverageHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/scan/?",WifiScanHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/join/(.+)/(.*)/?",WifiJoinHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/direct/?",WifiDirectHandler),
                
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/start/?",StartHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stop/?",StopHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/joke/?",JokeHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/statistics/?",StatsHandler),

                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/rules/?",RulesHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/rules/block/(.+)/?",BlockHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/rules/unblock/(.+)/?",UnblockHandler),
#                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/rules/patches/?",PatchesHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/rules/patch/(.+)/?",PatchHandler),
                
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/triggers/(.+)/add/(.+)/(http://|https://)(.*)",TriggerHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/triggers/(.+)/delete/?",GroupUnTriggerHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/triggers/(.+)/delete/(.+)/?",UnTriggerHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/triggers/(.+)/?",TriggersGroupHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/triggers/?",TriggersHandler),
                
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/smartthings/?",SmartThingsHandler),
                
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/?",SettingsHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/default/?",SettingsDefaultHandler),
                
                # test these two...
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/([0-9]+)/([0-9]+)/(false|true|on|off|beans|filter)/(weak|medium|strong)/?",StoreSettingsHandler),
                (self.webroot + r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/([0-9]+)/([0-9]+)/(false|true|on|off|normal|formula)/([0-9]+)/?",StoreSettingsHandler),
                (self.webroot + r"/api/version/?",VersionHandler),
                (self.webroot + r"/api/appliances/?",DevicesHandler),
                (self.webroot + r"/api/joke/?",JokeHandler),
                (self.webroot + r"/api/messages/?",MessagesHandler),
                (self.webroot + r"/api/?.*",UnknownHandler),
                
                # WEB PAGES
                (r"/",MainPageHandler),
                (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wireless/?", WirelessPageHandler),
                (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/statistics/?", StatsPageHandler),
                (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/?", SettingsPageHandler),
                (r"/statistics/?",ServerPageHandler),
                (r"/info/api/?",APIPageHandler),
                (r"/info/license/?",LicensePageHandler),
                (r"/info/protocol/?",ProtocolPageHandler),
                (r"/info/messages/?",MessagesPageHandler),
                (r"/info/arguments/?",ArgumentsPageHandler),
                (r"/info/groups/?",GroupsPageHandler),
                (r"/info/message/([0-9,A-F,a-f][0-9,A-F,a-f])/?",MessagePageHandler),
                (r"/",MainPageHandler),
                (r"/info/?",InfoPageHandler),
                (r"/(.*)",GenericPageHandler),

                
            ]
            tornado.web.Application.__init__(self, handlers, **settings)
        except Exception:
            print((traceback.format_exc()))
            self.kill()
            raise SmarterError(WebServerStartFailed,"Web Server: Couldn't start on port " + self.bind + ":" + str(self.port))

        bonjour = iBrewBonjourThread(self.port)
        bonjour.start()

        try:
            self.thread = threading.Thread(target=self.start)
            self.thread.start()
        except Exception:
            self.kill()
            raise SmarterError(WebServerStartFailed,"Web Server: Couldn't start on port " + self.bind + ":" + str(self.port))


        self.isRunning = True
        self.autoconnect()
