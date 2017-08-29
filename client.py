
import bluetooth

import time
import json

import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


def protocol(address):
    payload = json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    bt_addr = address
    port = 0x1001

    print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

    sock.connect((bt_addr, port))

    print("connected.  type stuff")

    data = 'hello from drone!'
    sock.send(data)

    # THE SERVER WILL ONLY REPLY WHEN THE BLUETOOTH DISTANCE IS CLOSE ENOUGH
    # BUT THE SOCKET STAYS OPEN

    data = sock.recv(1024)
    print("Data received:", str(data))

    print('Sending: "Ok... understood"')
    sock.send('Ok... understood')
    sock.close()


if __name__ == '__main__':
    while True:

        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("found %d devices" % len(nearby_devices))

        for address, name in nearby_devices:
            print("  %s - %s" % (address, name))
            if address == settings.PEER_BT_ADDRESS:
                print("PEERING PARTNER FOUND")
                protocol(address)

        time.sleep(settings.BT_SLEEP)