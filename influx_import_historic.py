#!/usr/bin/env python
import csv
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

from influx_config import *

def prep_record(time, zone, actual, target):
    record_actual = None
    record_target = None
    record_delta = None

    try:
      record_actual = {
        "measurement": "zone_temp.actual",
        "tags": {
            "zone": zone,
        },
        "time": time,
        "fields": {
            "value": float(actual) if actual is not None or actual != '' else None
        }
    } if actual is not None else None
    except:
      pass

    try:
      if target == '' or target == -1:
        print "setting target to: -1 for %s" % zone
        target = -1.0

      record_target = {
        "measurement": "zone_temp.target",
        "tags": {
            "zone": zone,
        },
        "time": time,
        "fields": {
            "value": float(target) if target is not None or target != '' else None
        }
    } if target is not None else None
    except:
      pass

    try:
      if record_actual is not None and record_target is not None:

        record_delta = {
            "measurement": "zone_temp.delta",
            "tags": {
                "zone": zone,
            },
            "time": time,
            "fields": {
                "value": float(actual) - float(target)
            }
        }
    except:
      pass

    return record_actual, record_target, record_delta


client = InfluxDBClient(influx_host, influx_port, influx_user, influx_password, db_name)

print("Create database: " + db_name)
try:
    client.create_database(db_name)
except InfluxDBClientError:
    # Drop and create
    # client.drop_database(DBNAME)
    # client.create_database(DBNAME)
    pass

row_num = 0

with open(hist_filename, 'rb') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:

        if row_num == 0:
            row_num += 1
            continue

        data = []
        time = row[0]
        
        for zone_num in range(0,11):

            temp_actual = row[zone_num*2 + 1]
            temp_target = row[zone_num*2 + 2]
            zone_name = zones[zone_num]

            record_actual, record_target, record_delta = prep_record(time, zone_name, temp_actual, temp_target)

            if record_actual:
                data.append(record_actual)
            if record_target:
                data.append(record_target)
            if record_delta:
                data.append(record_delta)

            print "%s : %s (%s, %s)" % (time, zone_name, temp_actual, temp_target)

        try:
            client.write_points(data)
        except InfluxDBClientError as e:
            print e
            import ipdb; ipdb.set_trace()

        row_num += 1
