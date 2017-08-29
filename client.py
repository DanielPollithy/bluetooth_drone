
import bluetooth

# bluetooth low energy scan
from bluetooth.ble import DiscoveryService

import time
import json

import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


def send_payload(address):
    payload = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    bt_addr = address
    port = 0x1001

    print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

    sock.connect((bt_addr, port))

    print("connected.  type stuff")

    data = payload
    sock.send(data)
    data = sock.recv(1024)
    print("Data received:", str(data))

    a = input("exit: ")
    sock.close()


if __name__ == '__main__':
    while True:

        service = DiscoveryService()
        devices = service.discover(2)

        for address, name in devices.items():
            print("  %s - %s" % (address, name))
            if address == settings.PEER_BT_ADDRESS:
                print("PEERING PARTNER FOUND")
                send_payload(address)

        time.sleep(settings.BT_SLEEP)