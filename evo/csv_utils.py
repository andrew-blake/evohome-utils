from datetime import datetime
from pprint import pprint
import csv
import os


def log_to_csv(zone_details, filename):

    exists = os.path.isfile(filename)

    inc_header = not exists

    fp = open(filename, 'a')
    writer = csv.writer(fp)

    ts = datetime.utcnow()
    ts = ts.replace(microsecond=0)

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
