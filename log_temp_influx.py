#!/usr/bin/env python

from pprint import pprint
import sys

from evohomeclient2 import EvohomeClient

try:
    from config import username, password, filename, dhw_target
except:
    print "Please configure config.py"
    exit(1)

from influx import influx_utils


def obtain_zone_details():

    try:
        client = EvohomeClient(username, password, debug=False)
    except ValueError:
        print("EvoHome server error")
        exit(1)

    zone_details = []

    for zone in client.temperatures():

        # modify response for DHW to be consistent with normal zones
        if zone['thermostat'] == 'DOMESTIC_HOT_WATER':
            zone['name'] = '_DHW'
            zone['setpoint'] = dhw_target

        zone_details.append(zone)

    return zone_details



def log_temperatures():
    zone_details = obtain_zone_details()
    influx_utils.log_to_influx(zone_details=zone_details)

if __name__ == "__main__":
    log_temperatures()
