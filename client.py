
import bluetooth

import time
import json

from subprocess import Popen, PIPE

import settings
from drone_poller import notify_website

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

    with open('connection_state.txt', 'w') as inp:
        inp.write(json.dumps({
            'state': 'landing approach',
            'station': ''
        }))
    notify_website()

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
            server_ethereum_address = data['addr'].lower()
            with open('connection_state.txt', 'w') as inp:
                inp.write(json.dumps({
                    'status': 'landing accepted',
                    'station': server_ethereum_address
                }))
            notify_website()
        else:
            server_ethereum_address = False
            with open('connection_state.txt', 'w') as inp:
                inp.write(json.dumps({
                    'status': 'landing denied',
                    'station': ''
                }))
            notify_website()
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

    print('Connection accepted')
    print('calling ethereum network')

    # ETHEREUM
    # now start the transaction
    if not settings.DEMO:
        print('node start_charging.js {} {}'.format(settings.CLIENT_ETHEREUM_ADDRESS, server_ethereum_address))
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
    else:
        returncode = 0

    if returncode != 0:
        sock.send(json.dumps({'start_charging': False}))
        print('Not starting charging logic (no reservation or blockchain problem)')
        print('Closing connection.')
        with open('connection_state.txt', 'w') as inp:
            inp.write(json.dumps({
                'status': 'charging denied',
                'station': server_ethereum_address
            }))
        notify_website()
        # wait for remote closing
        data = sock.recv(1024)
        # sock.close()

    with open('connection_state.txt', 'w') as inp:
        inp.write(json.dumps({
            'status': 'start charging',
            'station': server_ethereum_address
        }))
    notify_website()
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

    with open('connection_state.txt', 'w') as inp:
        inp.write(json.dumps({
            'status': 'charging ended',
            'station': server_ethereum_address
        }))
    notify_website()

    sock.close()

def run():
    connecting = True
    while connecting:
        nearby_devices = bluetooth.discover_devices(duration=settings.BT_DISCOVERY_DURATION, flush_cache=False)
        print("found %d devices" % len(nearby_devices))

        for address in nearby_devices:
            print("  %s " % (address))
            if address.lower() == settings.PEER_BT_ADDRESS:
                print("PEERING PARTNER FOUND")
                try:
                    protocol(address.lower())
                except bluetooth.BluetoothError as e:
                    print('e')
                    print(e)
                    print('errno')
                    print(e.errno)
                    print('args')
                    print(e.args)
                    print('msg')
                    print(e.message)
                    print('__repr__()')
                    print(e.__repr__())
                    if e.__repr__() == "(104, 'Connection reset by peer')":
                        print('Connection reset by peer')
                        print('That is o.k. I make a break and then we keep on')
                        time.sleep(settings.DRONE_REJECTED_RESTART_TIME)
                    elif e.message == "(112, 'Host is down')":
                        print('The host is down. :(')
                        print('Try to reconnect')
                    elif e.message == "(9, 'Bad file descriptor')":
                        print('Closing connection because booking is unconfirmed')
                        print('No booking in blockchain')
                    elif e.message == "(104, 'Connection reset by peer')":
                        print('Peer closed connection')
                        print('No booking in blockchain')
                    else:
                        print('This error is not known. I stop connecting')
                        print(e)
                        # connecting = False

        time.sleep(settings.BT_SLEEP)


if __name__ == '__main__':
    run()