#!/usr/bin/env python

import sys

from evohomeclient2 import EvohomeClient

try:
    from config import username, password, filename
except:
    print "Please configure config.py"
    sys.exit()

client = EvohomeClient(username, password, debug=True)
filename = './schedule-to-restore.json'

client.zone_schedules_restore(filename)
