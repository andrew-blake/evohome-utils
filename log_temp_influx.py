#!/usr/bin/env python

from evo import evo_utils
from influx import influx_utils


def log_temperatures():
    zone_details = evo_utils.obtain_zone_details()
    influx_utils.log_to_influx(zone_details=zone_details)

if __name__ == "__main__":
    log_temperatures()
