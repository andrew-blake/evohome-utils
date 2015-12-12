#!/usr/bin/env python

from datetime import datetime
from pprint import pprint
import csv
import os
import sys

from evohomeclient2 import EvohomeClient

try:
    from config import username, password, filename
except:
    print "Please configure config.py"
    sys.exit()


client = EvohomeClient(username, password, debug=True)

def temperatures(client, location=None):
        status = client.status(location)

        if 'dhw' in status['gateways'][0]['temperatureControlSystems'][0]:
            dhw = status['gateways'][0]['temperatureControlSystems'][0]['dhw']
            yield {'thermostat': 'DOMESTIC_HOT_WATER',
                    'id': dhw['dhwId'],
                    'name': '_DHW',
                    'temp': dhw['temperatureStatus']['temperature'],
                    'target': -1
                  }

        for zone in status['gateways'][0]['temperatureControlSystems'][0]['zones']:
            yield {'thermostat': 'EMEA_ZONE',
                    'id': zone['zoneId'],
                    'name': zone['name'],
                    'temp': zone['temperatureStatus']['temperature'],
                    'target': zone['heatSetpointStatus']['targetTemperature']
                  }

exists = os.path.isfile(filename)

inc_header = not exists

fp = open(filename, 'a')
writer = csv.writer(fp)

ts = datetime.utcnow()
ts = ts.replace(second=0, microsecond=0)

result = {}

for t in client.temperatures():
    result["%s-%s" % (t['id'], t['name'])] = [t['temp'], t['setpoint']]

header = []
header.append('ts')
for k in sorted(result.keys()):
    header.append("%s-temp" % k)
    header.append("%s-target" % k)

if inc_header:
    writer.writerow(header)

row = []
row.append(ts)

for k in sorted(result.keys()):
    row.extend(result[k])

writer.writerow(row)

fp.close()

print ts
pprint(result)

