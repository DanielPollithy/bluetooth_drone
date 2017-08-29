import bluetooth
import time

import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


while True:
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
        if addr == settings.PEER_BT_ADDRESS:
            print("PEERING PARTNER FOUND")

    time.sleep(settings.BT_SLEEP)