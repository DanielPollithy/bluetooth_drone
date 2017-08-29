import bluetooth
import time
import json

import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


def send_payload(address):
    payload = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)

    bt_addr = address
    port = 0x1001

    print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

    sock.connect((bt_addr, port))

    print("connected.  type stuff")

    data = payload
    sock.send(data)
    data = sock.recv(1024)
    print("Data received:", str(data))

    sock.close()


while True:
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))
        if addr == settings.PEER_BT_ADDRESS:
            print("PEERING PARTNER FOUND")
            send_payload(addr)

    time.sleep(settings.BT_SLEEP)