#!/usr/bin/env python

from datetime import datetime
from pprint import pprint
import csv
import os

from evo import evo_utils


def log_to_csv(zone_details):

    exists = os.path.isfile(evo_utils.filename)

    inc_header = not exists

    fp = open(evo_utils.filename, 'a')
    writer = csv.writer(fp)

    ts = datetime.utcnow()
    ts = ts.replace(second=0, microsecond=0)

    result = {}

    for zone in zone_details:
        result["%s-%s" % (zone['id'], zone['name'])] = [zone['temp'], zone['setpoint']]

    header = ['ts']
    for k in sorted(result.keys()):
        header.append("%s-temp" % k)
        header.append("%s-target" % k)

    if inc_header:
        writer.writerow(header)

    row = [ts]

    for k in sorted(result.keys()):
        row.extend(result[k])

    writer.writerow(row)

    fp.close()

    print ts
    pprint(result)


def log_temperatures():
    zone_details = evo_utils.obtain_zone_details()
    log_to_csv(zone_details=zone_details)

if __name__ == "__main__":
    log_temperatures()
