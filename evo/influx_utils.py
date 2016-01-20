from datetime import datetime

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

try:
    from influx_config import db_name, influx_host, influx_port, influx_user, influx_password, write_to_influx
except:
    print "Please configure influx_config.py"
    exit(1)


def log_to_influx(zone_details):

    influx_client = InfluxDBClient(influx_host, influx_port, influx_user, influx_password, db_name)

    data = []
    ts = datetime.utcnow()
    ts = ts.replace(second=0, microsecond=0)

    for zone in zone_details:

        temp_actual = zone['temp']
        temp_target = zone['setpoint']
        zone_name = zone['name']

        record_actual, record_target, record_delta = prep_record(ts, zone_name, temp_actual, temp_target)

        if record_actual:
            data.append(record_actual)
        if record_target:
            data.append(record_target)
        if record_delta:
            data.append(record_delta)

        print "%s : %s (%s, %s)" % (ts, zone_name, temp_actual, temp_target)

    try:
        if write_to_influx:
            influx_client.write_points(data)
    except InfluxDBClientError as e:
        print e


def prep_record(time, zone, actual, target):
    record_actual = None
    record_target = None
    record_delta = None

    if actual is not None and actual != '':
        try:
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
        except Exception as e:
            print e

    if target is not None and target != '':
        try:
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
        except Exception as e:
            print e

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

    return record_actual, record_target, record_delta

