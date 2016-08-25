# -*- coding: utf8 -*-


from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import socket

import os
from smarter.SmarterClient import *

from iBrewBonjour import *
from iBrewJokes import *

#------------------------------------------------------
# SMARTER PROTOCOL INTERFACE REST API
#
# REST API interface to iKettle 2.0 & SmarterCoffee Devices
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Brewing on the 7th day (rev 6)
#------------------------------------------------------


clients = dict()
version = '0.1'


def custom_get_current_user(handler):
    #user = handler.get_secure_cookie("user")
    #if user:
    user = "#NONE#"
    return user


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return custom_get_current_user(self)


class GenericAPIHandler(BaseHandler):
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
        print os.path.join(os.path.dirname(__file__), webroot)+page+".html"
        if os.path.isfile(os.path.join(os.path.dirname(__file__), webroot)+page+".html"):
            self.render(webroot+page+".html")
        else:
            self.render(webroot+"somethingwrong.html")


class MainHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render(webroot+"index.html")



#------------------------------------------------------
# REST PAGES
#------------------------------------------------------


#------------------------------------------------------
# Devices Handler
#------------------------------------------------------


def encodeFirmware(device,version):
    return { 'version'   : version, 'certified' : Smarter.firmware_verified(device,version) }


def encodeDevice(device,version):
    return { 'id'          : device,
             'type'        : Smarter.device_to_string(device),
            }


class DeviceHandler(tornado.web.RequestHandler):
    def get(self, ip):
        if ip in clients:
            x = clients[ip]
            response = { 'device'      : encodeDevice(x.deviceId,x.version),
                         'firmware'    : encodeFirmware(x.deviceId,version),
                         'connected'   : x.connected,
                         'status'      : { 'watersensor' : { 'value'  : x.waterSensor,
                                                             'base'   : x.waterSensorBase
                                                           },
                                           'offbase'     : not x.onBase,

                                           'temperature' : { 'fahrenheid' : Smarter.celcius_to_fahrenheid(x.temperature),
                                                             'celcius   ' : x.temperature
                                                           }
                                         },
                         'default'     : { 'temperature' : { 'fahrenheid' : Smarter.celcius_to_fahrenheid(x.defaultTemperature),
                                                             'celcius   ' : x.defaultTemperature
                                                           },
                                           'keepwarm'    : x.defaultKeepWarmTime,
                                           'formula'     : { 'enabled'     : x.defaultFormula,
                                                             'temperature' : { 'fahrenheid' : Smarter.celcius_to_fahrenheid(x.defaultFormulaTemperature),
                                                                               'celcius   ' : x.defaultFormulaTemperature
                                                                             }

                                                           }
                                         }
                        }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class DevicesHandler(tornado.web.RequestHandler):
    def get(self):
        devices = SmarterClient().find_devices()
        for device in devices:
            response[device[0]] = encodeDevice(device[1],device[2])
        self.write(response)


class UnknownHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'error' : { 'code' : '0', 'message' : 'Request unavailable' }}
        self.write(response)



#------------------------------------------------------
# Kettle calibration
#------------------------------------------------------


class CalibrateHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            x = clients[ip]
            x.calibrate()
            response = { 'base'            : x.waterSensorBase,
                         'command status'  : x.commandStatus }
            self.write(response)
        else:
            response = { 'error': 'no device' }


class CalibrateBaseHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            x = clients[ip]
            x.calibrate_base()
            response = { 'base'            : x.waterSensorBase,
                         'command status'  : x.commandStatus }
            self.write(response)
        else:
            response = { 'error': 'no device' }


class CalibrateStoreBaseHandler(tornado.web.RequestHandler):
    def get(self,ip,base):
        if ip in clients:
            x = clients[ip]
            x.calibrate_store_base(Smarter.string_to_watersensor(base))
            response = { 'base'            : x.waterSensorBase,
                         'command status'  : x.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)



#------------------------------------------------------
# Wifi operation
#------------------------------------------------------


class WifiScanHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.wifi_scan()
            networks = {}
            for i in range(0,len(client.Wifi)):
                networks.update( { client.Wifi[i][0] :
                                            { 'signal'  : str(client.Wifi[i][1]),
                                              'quality' : Smarter.dbm_to_quality(int(client.Wifi[i][1]))
                                            }
                                  } )
            response = { 'networks ': networks }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class WifiJoinHandler(tornado.web.RequestHandler):
    def get(self,ip,name,password):
        if ip in clients:
            clients[ip].wifi_join(name,password)
            response = { 'success': 'joining wireless network' }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class WifiLeaveHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            clients[ip].wifi_leave()
            response = { 'success': 'left wireless network' }
        else:
            response = { 'error': 'no device' }
        self.write(response)



#------------------------------------------------------
# Settings
#------------------------------------------------------


class StoreSettingsHandler(tornado.web.RequestHandler):
    def get(self,ip,x1,x2,x3,x4):
        if ip in clients:
            client = clients[ip]
            client.device_store_settings(x1,x2,x3,x4)
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class SettingsHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.device_settings()
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class SettingsDefaultHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.device_defaults()
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


#------------------------------------------------------
# Coffee settings
#------------------------------------------------------

class StrengthHandler(tornado.web.RequestHandler):
    def get(self,ip,strength):
        if ip in clients:
            client = clients[ip]
            client.coffee_strength(strength)
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class CupsHandler(tornado.web.RequestHandler):
    def get(self,ip,cups):
        if ip in clients:
            client = clients[ip]
            client.coffee_strength(strength)
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class GrinderHandler(tornado.web.RequestHandler):
    def get(self,ip,bool):
        if ip in clients:
            client = clients[ip]
            client.coffee_grinder(bool)
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class HotPlateHandler(tornado.web.RequestHandler):
    def get(self,ip,timer):
        if ip in clients:
            client = clients[ip]
            client.coffee_cups(timer)
            response = { 'command status'  : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class CarafeHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.coffee_carafe()
            response = { 'carafe'         : client.carafe,
                         'command status' : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class SingleCupHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.coffee_singlecup()
            response = { 'singlecup'      : client.singlecup,
                         'command status' : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)



#------------------------------------------------------
# STOP START COMMANDS
#------------------------------------------------------


class StopHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.device_stop()
            response = { 'command status' : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


class StartHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.device_start()
            response = { 'command status' : client.commandStatus }
        else:
            response = { 'error': 'no device' }
        self.write(response)


#------------------------------------------------------
# Misc
#------------------------------------------------------


class JokeHandler(tornado.web.RequestHandler):
    def get(self,ip=""):
        if ip in clients:
            client = clients[ip]
            joke = iBrewJokes().joke()
            response = { 'joke' :  { 'question' : joke[0] , 'answer' : joke[1] }}
        elif ip == "":
            joke = iBrewJokes().joke()
            response = { 'joke' :  { 'question' : joke[0] , 'answer' : joke[1] }}
        else:
            response = { 'error': 'no device' }
        self.write(response)



class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : version,
                     'copyright'  : { 'year'   : '2016',
                                      'holder' : 'Tristan Crispijn'
                                    }
                    }
        self.write(response)



#------------------------------------------------------
# REST INTERFACE
#------------------------------------------------------


class iBrewWeb:


    def run(self):
        tornado.ioloop.IOLoop.instance().start()


    def runInThread(self):
        import threading
        t = threading.Thread(target=self.run)
        t.start()


    def shutdown(self):
        deadline = time.time() + 3
        io_loop = tornado.ioloop.IOLoop.instance()
     
        def stop_loop():
            now = time.time()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()
    
        stop_loop()
 
 
    def __init__(self,port,host=""):
        self.port = port
        
        devices = SmarterClient().find_devices()
        
        for device in devices:
            client = SmarterClient()
            client.host = device[0]
            client.init_default()
            clients[device[0]] = client
            client.print_connect_status()

        if host != "":
            ip = socket.gethostbyname(host)
            print host
            print ip
            print clients
            if not ip in clients:
                client = SmarterClient()
                client.host = host
                client.init_default()
                clients[ip] = client
                client.print_connect_status()

        settings = {
                "debug": True,
                "static_path": os.path.join(os.path.dirname(__file__), "web/static")
            }

        handlers = [
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/?",DeviceHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/?",CalibrateHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/base/?",CalibrateBaseHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/calibrate/base/([0-9]+)/?",CalibrateStoreBaseHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/carafe/?",CarafeHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/singlecup/?",SingleCupHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/hotplate/([0-9]+)/?",HotPlateHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/cups/([0-9]+)/?",CupsHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/grinder/?",GrinderHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/strength/(weak|normal|strong)/?",StrengthHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/scan/?",WifiScanHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/join/(.+)/(.*)/?",WifiJoinHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/leave/?",WifiLeaveHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/start/?",StartHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stop/?",StopHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/joke/?",JokeHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/?",SettingsHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/default/?",SettingsDefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)/?",StoreSettingsHandler),
            
            (r"/api/version/?",           VersionHandler),
            (r"/api/devices/?",           DevicesHandler),
            (r"/api/joke/?",              JokeHandler),
            (r"/api/?.*",                 UnknownHandler),
            
            (r"/",                        MainHandler),
                 #(r"/login",             LoginHandler),
            (r"/(.*)",                    GenericPageHandler),

            
        ]

        self.application = tornado.web.Application(handlers, **settings)
        self.application.listen(self.port)
        
        bonjour = iBrewBonjourThread(self.port)
        bonjour.start()
        tornado.ioloop.IOLoop.instance().start()

