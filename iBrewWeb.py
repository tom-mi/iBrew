# -*- coding: utf8 -*-


from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web

import os
from smarter.SmarterClient import *

from iBrewBonjour import *

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
# Version Handler
#------------------------------------------------------


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : version,
                     'copyright'  : { 'year'   : '2016',
                                      'holder' : 'Tristan Crispijn'
                                    }
                    }
        self.write(response)


class DeviceHandler(tornado.web.RequestHandler):
    def get(self, ip):
        if ip in clients:
            x = clients[ip]
            response = { 'device'      : { 'id'          : x.deviceId,
                                           'description' : Smarter.device_info(x.deviceId,x.version),
                                           'firmware'    : x.version
                                         },
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
        response = { 'devices' : len(devices) }
        for device in devices:
            response[device[0]] = { 'type'        : Smarter.device_to_string(device[1]),
                                    'firmware'    : { 'version'   : device[2],
                                                      'certified' : Smarter.firmware_verified(device[1],device[2])
                                                    }
                                  }
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
            self.write(response)
        else:
            response = { 'error': 'no device' }


#------------------------------------------------------
# Wifi
#------------------------------------------------------

class WifiHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            response = { 'firmware   ': client.WifiFirmware}
            self.write(response)
        else:
            response = { 'error': 'no device' }


class WifiScanHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            client.wifi_scan()
        
            response = { 'firmware   ': client.WifiFirmware
                        }
            self.write(response)
        else:
            response = { 'error': 'no device' }


class WifiLeaveHandler(tornado.web.RequestHandler):
    def get(self,ip):
        if ip in clients:
            client = clients[ip]
            response = { 'firmware   ': client.WifiFirmware
                   }
            self.write(response)
        else:
            response = { 'error': 'no device' }


#------------------------------------------------------
# Settings
#------------------------------------------------------

class StoreSettingsHandler(tornado.web.RequestHandler):
    def get(self,ip,x1,x2,x3,x4):
        if ip in clients:
            client = clients[ip]
            response = { 'base'            : x1,
                         'command status'  : client.commandStatus }
            self.write(response)
        else:
            response = { 'error': 'no device' }


class DefaultHandler(tornado.web.RequestHandler):
    def get(self,ip):
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : SmarterRESTAPIVersion,
                     'copyright'  : '2016 Tristan Crispijn'
                    }
        self.write(response)


#------------------------------------------------------
# Coffee
#------------------------------------------------------

class StrengthHandler(tornado.web.RequestHandler):
    def get(self,ip,strength):
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : SmarterRESTAPIVersion,
                     'copyright'  : '2016 Tristan Crispijn'
                    }
        self.write(response)

class CupsHandler(tornado.web.RequestHandler):
    def get(self,ip,cups):
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : SmarterRESTAPIVersion,
                     'copyright'  : '2016 Tristan Crispijn'
                    }
        self.write(response)


class HotPlateHandler(tornado.web.RequestHandler):
    def get(self,ip,cups):
        response = { 'description': 'iBrew Smarter REST API',
                     'version'    : SmarterRESTAPIVersion,
                     'copyright'  : '2016 Tristan Crispijn'
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
 
 
    def __init__(self,port):
        self.port = port
        
        client = SmarterClient()
        client.host = '10.0.0.99'
        client.init_default()

        clients['10.0.0.99'] = client
        version = "s"

        '''
        settings = dict(
            template_path=os.path.join(AppFolders.appBase(), "web"),
            static_path=os.path.join(AppFolders.appBase(), "static"),
            static_url_prefix=self.webroot + "/static/",
            debug=True,
            #autoreload=False,
            login_url=self.webroot + "/login",
            cookie_secret=self.config['security']['cookie_secret'],
            xsrf_cookies=True,
        )
        '''

        settings = {
                "debug": True,
                "static_path": os.path.join(os.path.dirname(__file__), "web/static")
            }

        handlers = [
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/",DeviceHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/calibrate/",CalibrateHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/calibrate/base",CalibrateBaseHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/calibrate/base/([0-9]+)",CalibrateStoreBaseHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/temperature/",DefaultHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/carafe/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/singlecup/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/hotplate/([0-9]+)/",HotPlateHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/cups/([0-9]+)/",CupsHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/grinder/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/strength/(weak|normal|strong)/",StrengthHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/",WifiHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/scan/",WifiScanHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/join/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/leave/",WifiLeaveHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/history/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/start/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stop/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/reset/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/raw/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/update/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/time/",DefaultHandler),
            
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/default",DefaultHandler),
            (r"/api/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)",StoreSettingsHandler),
            
            (r"/api/version",           VersionHandler),
            (r"/api/devices",           DevicesHandler),
            
            (r"/",                  MainHandler),
                 #(r"/login",             LoginHandler),
            (r"/(.*)",                GenericPageHandler),

            
        ]

        self.application = tornado.web.Application(handlers, **settings)
        self.application.listen(self.port)
        
        bonjour = iBrewBonjourThread(self.port)
        bonjour.start()
        tornado.ioloop.IOLoop.instance().start()

