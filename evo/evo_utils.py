from evohomeclient2 import EvohomeClient

try:
    from config import username, password, filename, dhw_target
except:
    print "Please configure config.py"
    exit(1)


def obtain_zone_details():

    try:
        client = EvohomeClient(username, password, debug=False)
    except ValueError:
        print("\nEvoHome API error - aborting\n")
        exit(1)

    zone_details = []

    for zone in client.temperatures():

        # normalise response for DHW to be consistent with normal zones
        if zone['thermostat'] == 'DOMESTIC_HOT_WATER':
            zone['name'] = '_DHW'
            zone['setpoint'] = dhw_target

        zone_details.append(zone)

    return zone_details
