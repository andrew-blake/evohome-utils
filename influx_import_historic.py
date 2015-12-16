#!/usr/bin/env python
import csv
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

from influx_config import *

def prep_record(time, zone, actual, target):
    record_actual = {
        "measurement": "zone_temp.actual",
        "tags": {
            "zone": zone,
        },
        "time": time,
        "fields": {
            "value": float(actual)
        }
    }

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
            "value": float(target)
        }
    }

    return record_actual, record_target


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

with open(filename, 'rb') as csv_file:
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

            record_actual, record_target = prep_record(time, zone_name, temp_actual, temp_target)
            data.append(record_actual)
            data.append(record_target)

            print "%s : %s (%s, %s)" % (time, zone_name, temp_actual, temp_target)

        try:
            client.write_points(data)
        except InfluxDBClientError as e:
            print e
            import ipdb; ipdb.set_trace()

        row_num += 1
