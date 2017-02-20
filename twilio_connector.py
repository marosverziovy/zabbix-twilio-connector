#!env/bin/python

from twilio.rest import Client
from config import Config as c
import argparse
import datetime
import sys

class Zabbix_connector:

    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("to", nargs='?', action='store', help="Number in international format to call", default=c.config['default_number_to'])
    parser.add_argument("eventid", nargs='?', action='store', help="Event ID to store in log")
    args = parser.parse_args()

    def connectToApi(self):
        return Client(c.config['account_sid'], c.config['auth_token'])

    def numberFrom(self):
        return c.config['number_from']

    def makeCall(self):
        call = self.connectToApi().calls.create(
            to=args.to,
            from_   =self.numberFrom(),
            url=c.config['twiml_file_url'])
        return(call)

    def logCall(self, call):
        log = {'from': call.from_,
               'to': call.to,
               'sid': call.sid,
               'timestamp': datetime.date.today().strftime("%x %X"),
               'status': call.status,
               'eventid': args.eventid
               }

        f = open(c.config['log_file'], 'aw')
        f.write(str(log) + "\n")
        f.close()

if __name__ == "__main__":
    z = Zabbix_connector()

    # make actual call
    call = z.makeCall()

    # if logging is on, write to log
    if c.config['logging_enabled'] == True:
        z.logCall(call)

    sys.exit(0)