#!/usr/bin/env python

import sys
import json
from pprint import pprint

from evohomeclient2 import EvohomeClient

try:
    from config import username, password, filename
except:
    print "Please configure config.py"
    sys.exit()

client = EvohomeClient(username, password, debug=False)


def get_week_schedule(switch_points_mid_week, switch_points_weekend):
    return {
        "DailySchedules": [
            {
                "DayOfWeek": 0,
                "Switchpoints": switch_points_mid_week
            },
            {
                "DayOfWeek": 1,
                "Switchpoints": switch_points_mid_week
            },
            {
                "DayOfWeek": 2,
                "Switchpoints": switch_points_mid_week
            },
            {
                "DayOfWeek": 3,
                "Switchpoints": switch_points_mid_week
            },
            {
                "DayOfWeek": 4,
                "Switchpoints": switch_points_mid_week
            },
            {
                "DayOfWeek": 5,
                "Switchpoints": switch_points_weekend
            },
            {
                "DayOfWeek": 6,
                "Switchpoints": switch_points_weekend
            },
        ]
    }


def client_set_zone_schedule(zone_id, zone_info):
    control = client._get_single_heating_system()

    schedule = json.dumps(zone_info)

    # set schedule
    control.zones_by_id[zone_id].set_schedule(schedule)

    # retrieve schedule
    print "Schedule: %s" % control.zones_by_id[zone_id].name
    pprint(control.zones_by_id[zone_id].schedule())



switch_points = [
        { "TimeOfDay": "06:01:00", "TargetTemperature": 21.0, },
        { "TimeOfDay": "08:30:00", "TargetTemperature": 21.0, },
        { "TimeOfDay": "16:00:00", "TargetTemperature": 21.0, },
        { "TimeOfDay": "19:00:00", "TargetTemperature": 21.0, },
        { "TimeOfDay": "22:30:00", "TargetTemperature": 17.0, },
    ]


# test
client_set_zone_schedule(u'123456', get_week_schedule(switch_points_mid_week=switch_points, switch_points_weekend=switch_points))
