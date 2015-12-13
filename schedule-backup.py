#!/usr/bin/env python

import sys
from datetime import datetime

from evohomeclient2 import EvohomeClient

try:
    from config import username, password, filename
except:
    print "Please configure config.py"
    sys.exit()

client = EvohomeClient(username, password, debug=True)

today = datetime.today().date()
filename = './backup-%s-%s-%s-b.json' % (today.year, today.month, today.day)

client.zone_schedules_backup(filename)
