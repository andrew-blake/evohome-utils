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



switch_points_hall_landing = [
        { "TimeOfDay": "06:00:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "08:30:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "16:00:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "19:00:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "22:30:00", "TargetTemperature": 16.0, },
    ]

switch_points = [
        { "TimeOfDay": "06:00:00", "TargetTemperature": 20.0, },
        { "TimeOfDay": "08:30:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "16:00:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "19:00:00", "TargetTemperature": 20.0, },
        { "TimeOfDay": "22:30:00", "TargetTemperature": 20.0, },
    ]

switch_points_top_floor = [
        { "TimeOfDay": "06:00:00", "TargetTemperature": 20.0, },
        { "TimeOfDay": "08:30:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "16:00:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "19:00:00", "TargetTemperature": 20.0, },
        { "TimeOfDay": "22:30:00", "TargetTemperature": 20.0, },
    ]

switch_points_edward = [
        { "TimeOfDay": "06:00:00", "TargetTemperature": 20.0, },
        { "TimeOfDay": "08:30:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "16:00:00", "TargetTemperature": 18.0, },
        { "TimeOfDay": "19:00:00", "TargetTemperature": 20.0, },
        { "TimeOfDay": "22:30:00", "TargetTemperature": 20.0, },
    ]

# test
# client_set_zone_schedule(u'123456', get_week_schedule(switch_points_mid_week=switch_points, switch_points_weekend=switch_points))


# {'temp': 44.0, 'thermostat': 'DOMESTIC_HOT_WATER', 'name': '', 'id': u'692332'}

# {'temp': 19.0, 'thermostat': 'EMEA_ZONE', 'name': u'Living room', 'id': u'692330'}
# {'temp': 19.0, 'thermostat': 'EMEA_ZONE', 'name': u'Dining room', 'id': u'692384'}
client_set_zone_schedule(u'692330', get_week_schedule(switch_points_mid_week=switch_points, switch_points_weekend=switch_points))
client_set_zone_schedule(u'692384', get_week_schedule(switch_points_mid_week=switch_points, switch_points_weekend=switch_points))

# {'temp': 18.0, 'thermostat': 'EMEA_ZONE', 'name': u'Kitchen', 'id': u'692367'}
# {'temp': 19.5, 'thermostat': 'EMEA_ZONE', 'name': u'Hall', 'id': u'692440'}
# {'temp': 20.0, 'thermostat': 'EMEA_ZONE', 'name': u'Landing', 'id': u'692442'}
client_set_zone_schedule(u'692367', get_week_schedule(switch_points_mid_week=switch_points_hall_landing, switch_points_weekend=switch_points_hall_landing))
client_set_zone_schedule(u'692440', get_week_schedule(switch_points_mid_week=switch_points_hall_landing, switch_points_weekend=switch_points_hall_landing))
client_set_zone_schedule(u'692442', get_week_schedule(switch_points_mid_week=switch_points_hall_landing, switch_points_weekend=switch_points_hall_landing))

# {'temp': 19.5, 'thermostat': 'EMEA_ZONE', 'name': u'Greg', 'id': u'692388'}
# {'temp': 19.0, 'thermostat': 'EMEA_ZONE', 'name': u'Jen & Andrew', 'id': u'692395'}
client_set_zone_schedule(u'692388', get_week_schedule(switch_points_mid_week=switch_points, switch_points_weekend=switch_points))
client_set_zone_schedule(u'692395', get_week_schedule(switch_points_mid_week=switch_points, switch_points_weekend=switch_points))

# {'temp': 20.5, 'thermostat': 'EMEA_ZONE', 'name': u'Patrick', 'id': u'692439'}
# {'temp': 19.0, 'thermostat': 'EMEA_ZONE', 'name': u'Alistair', 'id': u'692443'}
client_set_zone_schedule(u'692439', get_week_schedule(switch_points_mid_week=switch_points_top_floor, switch_points_weekend=switch_points_top_floor))
client_set_zone_schedule(u'692443', get_week_schedule(switch_points_mid_week=switch_points_top_floor, switch_points_weekend=switch_points_top_floor))

# {'temp': 19.0, 'thermostat': 'EMEA_ZONE', 'name': u'Edward', 'id': u'692389'}
client_set_zone_schedule(u'692389', get_week_schedule(switch_points_mid_week=switch_points_edward, switch_points_weekend=switch_points_edward))

