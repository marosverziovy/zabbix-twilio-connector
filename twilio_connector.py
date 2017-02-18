#!/usr/bin/python

from twilio.rest import Client
import conf
import argparse
import sys

c = conf.Conf
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--to", action='store', help="Number in international format to call")
parser.add_argument("-c", "--configlist", action="store_true", help="List configuration vars")
parser.add_argument("-d", "--debug", action="store_true", help="Print configuration vars before placing call")
args = parser.parse_args()

class Zabbix_connector:
  def connectToApi(self):
      return Client(c.config['account_sid'], c.config['auth_token'])

  def makeCall(self):
    call = self.connectToApi().calls.create(to=c.config['number_from'],
                               from_= args.to if args.to else c.config['number_from'],
                               url=c.config['twiml_file_url'])
    print(call.sid)

  def getConfig(self):
    for key, value in c.config.iteritems():
      if not value:
        value = "_EMPTY_"
      print("{}:\t{}".format(key, value))

z = Zabbix_connector()
if args.configlist:
  z.getConfig()
  sys.exit(0)

z.makeCall()