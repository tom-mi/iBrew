# -*- coding: utf8 -*-


from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import socket
import time
import threading

import os
from smarter.SmarterClient import *

from iBrewBonjour import *
from iBrewJokes import *

#import traceback

#------------------------------------------------------
# SMARTER PROTOCOL INTERFACE REST API
#
# REST API interface to iKettle 2.0 & Smarter Coffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Brewing on the 7th day (rev 6)
#------------------------------------------------------


def custom_get_current_user(handler):
    #user = handler.get_secure_cookie("user")
    #if user:
    user = "#NONE#"
    return user


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return custom_get_current_user(self)



class GenericAPIHandler(BaseHandler):
    def setContentType(self):
        self.add_header("Content-type","application/json; charset=UTF-8")

    def validateAPIKey(self):
        api_key = self.get_argument(u"apikey", default="")
        if api_key == "APIKEY":
            return True
        else:
            raise tornado.web.HTTPError(400)
            return False

#------------------------------------------------------
# WEB GUI PAGES
#------------------------------------------------------

webroot = "web/"

class GenericPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,page):
        if os.path.isfile(os.path.join(os.path.dirname(__file__), webroot)+page+".html"):
            self.render(webroot+page+".html")
        else:
            self.render(webroot+"somethingwrong.html")


class MainPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render(webroot+"index.html",clients = self.application.clients,joke = iBrewJokes().joke())


class ServerPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render(webroot+"server.html",clients = self.application.clients)


class InfoPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render(webroot+"info/info.html")


class WifiPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,ip):
        self.render(webroot+"wifi.html",client = self.application.clients[ip])

class ShowTextFilePageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,txt):
        location =  self.application.settings["static_path"] + "/info/" + txt + ".txt"
        print location
        if os.path.isfile(os.path.join(os.path.dirname(__file__), webroot)+ "info/" + txt+".html") and os.path.isfile(location):
            text = ""
            with open(location, 'rb') as fd:
                text = fd.read()
                text = text.replace('\r', '<br>')
                text = text.replace('\n', '<br>')
            self.render(webroot+ "info/" + txt+".html",file = text)
        else:
            self.render(webroot+"somethingwrong.html")



class APIPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        d = dict()
        for ip in self.application.clients:
            client = self.application.clients[ip]
            d.update({client.host : Smarter.device_to_string(client.deviceId)})
        self.render(webroot+"info/rest.html",devices = d,joke = iBrewJokes().joke())


class MessagesPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
              self.render(webroot+"info/messages.html",status = Smarter.StatusToJSON(),commands = Smarter.CommandToJSON(), responses = Smarter.ResponseToJSON())



class ArgumentsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
              self.render(webroot+"info/arguments.html",status = Smarter.StatusToJSON(),commands = Smarter.CommandToJSON(), responses = Smarter.ResponseToJSON())


class MessagePageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,message):
        try:
            mid = Smarter.code_to_number(message)
        except:
            self.render(webroot+"somethingwrong.html")
        self.render(webroot+"info/message.html", id = mid)


class SettingsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,ip):
        if ip in self.application.clients:
            c = self.application.clients[ip]
            self.render(webroot+"settings.html",client = c)
        else:
            self.render(webroot+"somethingwrong.html")


class StatsPageHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self,ip):
        if ip in self.application.clients:
            c = self.application.clients[ip]
            self.render(webroot+"stats.html",client = c)
        else:
            self.render(webroot+"somethingwrong.html")



#------------------------------------------------------
# REST PAGES
#------------------------------------------------------

#------------------------------------------------------
# Devices Handler
#------------------------------------------------------


def encodeFirmware(device,version):
    return { 'version'   : version, 'certified' : Smarter.firmware_verified(device,version) }


def encodeDevice(client):
    return { 'type'        : { 'desciption' : Smarter.device_to_string(client.deviceId),
                               'id'          : client.deviceId
                            },
             'directmode'  : client.isDirect,
             'host'        : client.host,
             'connected'   : client.connected,
             'firmware'    : encodeFirmware(client.deviceId,client.version)
            }

class DeviceHandler(GenericAPIHandler):


    def get(self, ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            respons = None
            if client.isKettle:
                response = { 'device'      : encodeDevice(client),
                             'sensors'     : { 'waterlevel'  : { 'raw'    : client.waterSensor,
                                                                 'stable' : client.waterSensorStable,
                                                                 'base'   : client.waterSensorBase
                                                               },
                                               'base'        : Smarter.string_base_on_off(client.onBase),
                                               'status'      : Smarter.status_kettle_description(client.kettleStatus),
                                               'temperature' : { 'raw'    : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.temperature),
                                                                              'celsius'    : client.temperature
                                                                            },
                                                                 'stable' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.temperatureStable),
                                                                              'celsius'    : client.temperatureStable
                                                                            }
                                                               }
                                                               
                                             },
                             
                             'default'     : { 'temperature' : { 'fahrenheid' : Smarter.celsius_to_fahrenheid(client.defaultTemperature),
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
            elif client.isCoffee:
                response = { 'device'      : encodeDevice(client),
                             'sensors'     : { 'hotplate'   : client.hotPlateOn,
                                               'heater'     : client.heaterOn,
                                               'grinder'    : client.grinderOn,
                                               'waterlevel'     : client.waterLevel,
                                               'status'         : { 'working'     : client.working,
                                                                    'ready'       : client.ready,
                                                                    'cups'        : clinet.cupsBrew,
                                                                    'carafe'      : client.carafe,
                                                                    'enoughwater' : client.waterEnough,
                                                                    'timerevent'  : client.timerEvent
                                                                  },
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
                                               'caraferequired' : client.carafeMode,
                                               'singlecup'      : client.singlecup
                                             },
                            }


        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class DevicesHandler(GenericAPIHandler):
    def get(self):
        devices = SmarterClient().find_devices()
        response = {}
        for device in devices:
            response[device[0]] = { 'type'        : { 'desciption'  : Smarter.device_to_string(device[1]),
                                                      'id'          : device[1]
                                                    },
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
# Kettle calibration
#------------------------------------------------------


class CalibrateHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isKettle:
                client.kettle_calibrate()
                response = { 'base'            : client.waterSensorBase,
                             'command status'  : client.commandStatus }
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
                             'command status'  : client.commandStatus }
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
                client.calibrate_store_base(Smarter.string_to_watersensor(base))
                response = { 'base'            : client.waterSensorBase,
                             'command status'  : client.commandStatus }
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
            except:
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


class WifiLeaveHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            self.application.clients[ip].wifi_leave()
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
            response = { 'command status'  : client.commandStatus }
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
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


#------------------------------------------------------
# Coffee settings
#------------------------------------------------------

class StrengthHandler(GenericAPIHandler):
    def get(self,ip,strength):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_strength(strength)
                response = { 'command status'  : client.commandStatus }
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
                client.coffee_strength(strength)
                response = { 'command status'  : client.commandStatus }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class GrinderHandler(GenericAPIHandler):
    def get(self,ip,bool):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_grinder(bool)
                response = { 'command status'  : client.commandStatus }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class HotPlateHandler(GenericAPIHandler):
    def get(self,ip,timer):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_cups(timer)
                response = { 'command status'  : client.commandStatus }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class CarafeHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_carafe()
                response = { 'carafe'         : client.carafe,
                             'command status' : client.commandStatus }
            else:
                response = { 'error': 'need coffee machine' }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class SingleCupHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            if client.isCoffee:
                client.coffee_singlecup()
                response = { 'singlecup'      : client.singlecup,
                             'command status' : client.commandStatus }
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
                response = { 'error'      : 'none' },
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
                response = { 'error'      : 'none' },
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
            response = { 'command status' : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.setContentType()
        self.write(response)


class StartHandler(GenericAPIHandler):
    def get(self,ip):
        if ip in self.application.clients:
            client = self.application.clients[ip]
            client.device_start()
            response = { 'command status' : client.commandStatus }
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
            
            response = { 'messages'         : { 'send'      : client.sendCount,
                                                'read'      : client.readCount,
                                                'client'    : client.commandCount,
                                                'server'    : client.responseCount
                                            },
                         'bytes'            : { 'send'      : client.sendBytesCount,
                                                'read'      : client.readBytesCount
                                            },
                         'reconnect'        : client.connectCount - 1,
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
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : self.application.version,
                     'copyright'  : { 'year'   : '2016',
                                      'holder' : 'Tristan Crispijn'
                                    }
                    }
        self.setContentType()
        self.write(response)



#------------------------------------------------------
# REST INTERFACE
#------------------------------------------------------


class iBrewWeb(tornado.web.Application):

    version = '0.71'
    
    def start(self):
        tornado.ioloop.IOLoop.instance().start()
    
    
    def autoconnect(self):

        #if not self.isRunning:
        #    return
        devices = SmarterClient().find_devices()
        SmarterClient().print_devices_found(devices)
        
        
        reconnect = 7
        
        for ip in self.clients.keys():
            client = self.clients[ip]
            #print "Checking " + ip
            if not client.connected:
                if self.reconnect_count[ip] < 7:
                    #print "Trying " + ip
                    self.reconnect_count[ip] += 1
                    try:
                        if self.dump:
                            if self.reconnect_count[ip] == 1:
                                print "[" + ip + "] Auto-connect attempt " + str(self.reconnect_count[ip])
                            else:
                                print "[" + ip + "] Auto-connect attempt " + str(self.reconnect_count[ip])
                        client.connect()
                        try:
                            threading.Thread(target=client.init_default)
                        except:
                            pass
                    except:
                        client.disconnect()
                else:
                    client.disconnect()
                    if self.dump:
                        print "[" + ip + "] Auto-connect tried " + str(reconnect) + " attempts, removing"
                    del self.clients[ip]
                    del self.reconnect_count[ip]
            else:
                self.reconnect_count[ip] = 0


        for device in devices:
            if device[0] not in self.clients:
                try:
                    if self.dump:
                        print "[" + device[0] + "] Adding Web Device"
                    client = SmarterClient()
                    client.dump = self.dump
                    client.dump_status = self.dump
                    client.host = device[0]
                    client.connect()
                    self.clients[device[0]] = client
                    threading.Thread(target=client.init_default)
                    self.reconnect_count[device[0]] = 0
                    print "iBrew Web Server: " + client.string_connect_status()
                except:
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
                        print "[" + ip + "] Adding Web Device"
                    client = SmarterClient()
                    client.host = self.host
                    client.dump = self.dump
                    client.dump_status = self.dump
                    client.connect()
                    self.clients[ip] = client
                    client.init_default()
                    self.reconnect_count[ip] = 0
                    print "iBrew Web Server: " + client.string_connect_status()
                except:
                    client.disconnect()
                    pass # raise SmarterError(WebServerListen,"Web Server: Couldn't open socket on port" + str(self.port))


        self.threadAutoConnect = threading.Timer(15, self.autoconnect)
        self.threadAutoConnect.start()


    def __init__(self):
        self.isRunning = False


    def __del__(self):
        self.kill()
    
    
    def kill(self):
        self.isRunning = False
        deadline = time.time() + 3

        self.threadAutoConnect.cancel()
        try:
            for ip in self.clients:
                self.clients[ip].disconnect()
        except:
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

        except:
            raise SmarterError(WebServerStopMonitorWeb,"Web Server: Could not stop webserver monitor")

        try:
            if self.thread.isAlive():
                self.thread.join()
        except:
            raise SmarterError(WebServerStopWeb,"Web Server: Could not stop webserver")


    def run(self,port,dump=False,host=""):
        self.port = port
        self.isRunning = False
        self.dump = dump
        self.host = host
        
        try:
            self.listen(self.port, no_keep_alive = True)
        except:
            raise SmarterError(WebServerListen,"Web Server: Couldn't open socket on port " + str(self.port))
            return
    
        self.clients = dict()
        self.reconnect_count = dict()
        
        self.autoconnect()
        

        try:
            settings = {
                "debug": True,
                "static_path": os.path.join(os.path.dirname(__file__), "web/static")
            }

            handlers = [
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/status/?",DeviceHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/?",CalibrateHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/base/?",CalibrateBaseHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/base/([0-9]+)/?",CalibrateStoreBaseHandler),

                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/beans/?",BeansHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/filter/?",FilterHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/carafe/?",CarafeHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/singlecup/?",SingleCupHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/hotplate/([0-9]+)/?",HotPlateHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/cups/([0-9]+)/?",CupsHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/grinder/?",GrinderHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/(weak|normal|strong)/?",StrengthHandler),
                
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/scan/?",WifiScanHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/join/(.+)/(.*)/?",WifiJoinHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/leave/?",WifiLeaveHandler),
                
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/start/?",StartHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stop/?",StopHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/joke/?",JokeHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stats/?",StatsHandler),
                
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/?",SettingsHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/default/?",SettingsDefaultHandler),
                (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/?",StoreSettingsHandler),
                
                (r"/api/version/?",VersionHandler),
                (r"/api/devices/?",DevicesHandler),
                (r"/api/joke/?",JokeHandler),
                (r"/api/messages/?",MessagesHandler),
                (r"/api/?.*",UnknownHandler),
                
                # WEB PAGES
                (r"/",MainPageHandler),
                (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/?", WifiPageHandler),
                (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stats/?", StatsPageHandler),
                (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/?", SettingsPageHandler),
                (r"/server/?",ServerPageHandler),
                (r"/info/rest/?",APIPageHandler),
                (r"/info/messages/?",MessagesPageHandler),
                (r"/info/arguments/?",ArgumentsPageHandler),
                (r"/info/message/([0-9,A-F,a-f][0-9,A-F,a-f])/?",MessagePageHandler),
                (r"/",MainPageHandler),
                (r"/info/?",InfoPageHandler),
                (r"/info/(.*)",ShowTextFilePageHandler),
                (r"/(.*)",GenericPageHandler),

                
            ]
            tornado.web.Application.__init__(self, handlers, **settings)
        except:
            print(traceback.format_exc())
            self.kill()
            raise SmarterError(WebServerStartFailed,"Web Server: Couldn't start on port " + str(self.port))

        bonjour = iBrewBonjourThread(self.port)
        bonjour.start()

        try:
            self.thread = threading.Thread(target=self.start)
            self.thread.start()
        except:
            self.kill()
            raise SmarterError(WebServerStartFailed,"Web Server: Couldn't start on port " + str(self.port))


        self.isRunning = True
