#!/usr/bin/python

from twilio.rest import Client
import conf
import argparse
import datetime
import sys

c = conf.Conf
parser = argparse.ArgumentParser()
parser.add_argument("to", action='store', help="Number in international format to call")
args = parser.parse_args()

class Zabbix_connector:
  global args

  def connectToApi(self):
      return Client(c.config['account_sid'], c.config['auth_token'])

  def numberTo(self):
    return args.to if args.to else c.config['default_number_to']

  def numberFrom(self):
    return c.config['number_from']

  def makeCall(self):
    call = self.connectToApi().calls.create(
      to=self.numberTo(),
      from_=c.config['number_from'],
      url=c.config['twiml_file_url'])
    return(call)

  def logCall(self, call):
    log = {'from': call.from_,
           'to': call.to,
           'sid': call.sid,
           'timestamp': datetime.date.today().strftime("%x %X"),
           'status': call.status,
           }

    f = open(c.config['log_file'], 'aw')
    f.write(str(log) + "\n")
    f.close()

z = Zabbix_connector()

# make actual call
call = z.makeCall()

# if logging is on, write to log
if c.config['logging_enabled'] == True:
  z.logCall(call)

sys.exit(0)