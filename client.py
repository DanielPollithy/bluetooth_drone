
import bluetooth

import time
import json

import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


def protocol(address):
    payload = json.dumps({'addr': '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'})
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

    # do some ethereum logic here with
    # server_ethereum_address
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

if __name__ == '__main__':
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
                    code = e.code
                    if code == 104:
                        print('Peer reset the connection')
                        print('That is o.k. I make a break and then we keep on')
                        time.sleep(settings.DRONE_REJECTED_RESTART_TIME)
                    else:
                        print('This error is not known. I stop connecting')
                        connecting = False

        time.sleep(settings.BT_SLEEP)
