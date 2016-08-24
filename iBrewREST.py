
# -*- coding: utf8 -*-

import struct
from smarter.SmarterClient import *


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




class iBrewREST:

    """
    from datetime import date
    import tornado.escape
    import tornado.ioloop
    import tornado.web

    client = SmarterClient()
    client.host = '10.0.0.99'
    client.init_default()
    clients = dict()
    clients['10.0.0.99'] = client


    class GenericAPIHandler(BaseHandler):
        def validateAPIKey(self):
                api_key = self.get_argument(u"api_key", default="")
                if api_key == "TRIXWOOD"
                    return True
                else:
                    raise tornado.web.HTTPError(400)
                    return False


    
    class APIHandler(tornado.web.RequestHandler):
        def get(self):
            response = { 'description': 'iBrew Smarter REST API',
                         'version'    : '0.3 rev 6',
                         'copyright'  : '2016 Tristan Crispijn'
                        }
            self.write(response)

    class VersionHandler(tornado.web.RequestHandler):
        def get(self):
            response = { 'description': 'iBrew Smarter REST API',
                         'version'    : '0.3 rev 6',
                         'copyright'  : '2016 Tristan Crispijn'
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
                response[device[0]] = { 'description' : Smarter.device_info(device[1],device[2]),
                                        'id'       : device[1],
                                        'firmware' : device[2]}
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


    class LoginHandler(BaseHandler):
        def get(self):
            if  len(self.get_arguments("next")) != 0:
                next=self.get_argument("next")
            else:
                next=self.webroot + "/"
            
            #if password and user are blank, just skip to the "next"
            if (  self.application.config['security']['password_digest'] == utils.getDigest("")  and
                  self.application.config['security']['username'] == ""
                ):
                self.set_secure_cookie("user", fix_username(self.application.config['security']['username']))
                self.redirect(next)
            else:
                self.render(deviceroot(self)+'login.html', next=next)

        def post(self):
            next = self.get_argument("next")

            if  len(self.get_arguments("password")) != 0:
                    
                #print self.application.password, self.get_argument("password") , next
                if (self.get_argument("password")  ==  'trixwood' and
                    self.set_secure_cookie("user", "trixwood")
                    
            self.redirect(next)

    class AboutPageHandler(BaseHandler):
        #@tornado.web.authenticated
        def get(self):
            self.render("web/about.html", version=self.application.version)

    application = tornado.web.Application([
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/",DeviceHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/calibrate/",CalibrateHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/calibrate/base",CalibrateBaseHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/calibrate/base/([0-9]+)",CalibrateStoreBaseHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/kettle/temperature/",DefaultHandler),
        
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/carafe/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/singlecup/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/hotplate/([0-9]+)/",HotPlateHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/cups/([0-9]+)/",CupsHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/grinder/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/coffee/strength/(weak|normal|strong)/",StrengthHandler),
        
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/",WifiHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/scan/",WifiScanHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/join/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/wifi/leave/",WifiLeaveHandler),
        
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/history/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/start/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/stop/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/reset/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/raw/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/update/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/time/",DefaultHandler),
        
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/default",DefaultHandler),
        (r"/([0-9]+.[0-9]+.[0-9]+.[0-9]+)/settings/([0-9]+)/([0-9]+)/([0-9]+)/([0-9]+)",StoreSettingsHandler),
        
    #    (r"/api",               VersionHandler),
        (r"/version",           VersionHandler),
        (r"/devices",           DevicesHandler),
     #   (r"/.*",                UnknownHandler),
        
      #  (r"/",                  MainHandler),
      #  (r"/(.*)\.html",        GenericPageHandler),
      #  (r"/login",             LoginHandler),

        
    ])
    """
    def __init__(self,port):
        pass
        #self.application.listen(port)
        #tornado.ioloop.IOLoop.instance().start()
