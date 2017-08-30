
import bluetooth

import time
import json

from subprocess import Popen, PIPE

import settings

settings.activate_bluetooth_discovery()
bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


def protocol(address):
    payload = json.dumps({'addr': settings.CLIENT_ETHEREUM_ADDRESS})
    assert len(payload) < 1024
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    bt_addr = address
    port = 0x1001

    print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

    sock.connect((bt_addr, port))

    print("connected.  Sending: ", payload)
    sock.send(payload)

    # THE SERVER WILL ONLY REPLY WHEN THE BLUETOOTH DISTANCE IS CLOSE ENOUGH
    # BUT THE SOCKET STAYS OPEN

    data = sock.recv(1024)
    print("Data received:", str(data))
    try:
        data = json.loads(data)
        assert 'accepted' in data
        connection_accepted = data['accepted']
        if connection_accepted:
            assert 'addr' in data
            server_ethereum_address = data['addr']
        else:
            server_ethereum_address = False
    except AssertionError:
        print('Json is missing data')
        sock.close()
        raise StandardError
    except:
        print('Error reading json from the data')
        sock.close()
        raise StandardError

    if not connection_accepted:
        print('The server has not accepted the drone')
        print('Closing connection.')
        sock.close()

    # ETHEREUM
    # now start the transaction
    p = Popen(
        [
            'node',
            'start_charging.js',
            settings.CLIENT_ETHEREUM_ADDRESS,
            server_ethereum_address
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    )
    output, err = p.communicate()
    returncode = p.returncode

    if returncode != 0:
        sock.send(json.dumps({'start_charging': False}))
        print('Not starting charging logic (no reservation or blockchain problem)')
        print('Closing connection.')
        sock.close()

    sock.send(json.dumps({'start_charging': True}))

    # the server will activate the relais now
    # the loading will take time and there could be some information exchanged here in the future
    data = sock.recv(1024)
    print("Data received:", str(data))
    try:
        data = json.loads(data)
        assert 'electricity' in data
        electricity = data['electricity']
    except AssertionError:
        print('Json is missing data')
        sock.close()
        raise StandardError
    except:
        print('Error reading json from the data')
        sock.close()
        raise StandardError

    print('Energy consumption as hangar says: {}'.format(electricity))
    print('Transaction done.')

    sock.close()

def run():
    connecting = True
    while connecting:
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        print("found %d devices" % len(nearby_devices))

        for address, name in nearby_devices:
            print("  %s - %s" % (address, name))
            if address == settings.PEER_BT_ADDRESS:
                print("PEERING PARTNER FOUND")
                try:
                    protocol(address)
                except bluetooth.btcommon.BluetoothError as e:
                    if e.errno == 104:
                        print('Connection reset by peer')
                        print('That is o.k. I make a break and then we keep on')
                        time.sleep(settings.DRONE_REJECTED_RESTART_TIME)
                    else:
                        print('This error is not known. I stop connecting')
                        print(e)
                        connecting = False

        time.sleep(settings.BT_SLEEP)


if __name__ == '__main__':
    run()