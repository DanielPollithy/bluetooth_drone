import json

import bluetooth
import time

import sys
from bt_proximity import BluetoothRSSI
from subprocess import Popen, PIPE

import settings
import relais


settings.activate_bluetooth_discovery()
bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))


def run(server_sock):
    client_sock, address = server_sock.accept()

    # only accept the peer
    if address[0] != settings.DRONE_BT_ADDRESS:
        print('Not awaited: {} (awaited)'.format(address[0], settings.DRONE_BT_ADDRESS))
        client_sock.close()
        raise StandardError

    print("Accepted connection from ", address)

    data = client_sock.recv(1024)
    print("Data received: ", str(data))
    try:
        data = json.loads(data)
        assert 'addr' in data
        client_ethereum_address = data['addr']
    except AssertionError:
        print('Json is missing data')
        client_sock.close()
        raise StandardError
    except:
        print('Error reading json from the data')
        client_sock.close()
        raise StandardError

    distance = 0
    try_counter = 0
    print('Setting up BluetoothRSSI')
    btrssi = BluetoothRSSI(addr=address[0])
    while distance < settings.RSSI_DISTANCE and try_counter < settings.MAX_RSSI_TRY_COUNT:
        try_counter += 1
        distance = btrssi.get_rssi()
        print('Distance to {} at try #{}\trssi={}'.format(address, try_counter, distance))
        time.sleep(settings.DISTANCE_SLEEP)

    if distance < settings.RSSI_DISTANCE:
        print('The distance was too big to connect')
        client_sock.send(json.dumps({'accepted': False}))
        client_sock.close()
        raise StandardError

    # everything is o.k. The drone is close enough, so now we return the proceedings
    payload = json.dumps({'accepted': True, 'addr': settings.SERVER_ETHEREUM_ADDRESS})
    assert len(payload) < 1024
    client_sock.send(payload)

    # receive the last interaction
    data = client_sock.recv(1024)
    print("Data received:", str(data))
    try:
        data = json.loads(data)
        assert 'start_charging' in data
        start_charging = data['start_charging']
    except AssertionError:
        print('Json is missing data')
        client_sock.close()
        raise StandardError
    except:
        print('Error reading json from the data')
        client_sock.close()
        raise StandardError

    if start_charging:
        print('START THE CHARGING NOW')
        # wait the charging time
        print('opening the relais')
        relais.switch_on()
        for i in range(10):
            print('.')
            time.sleep(settings.CHARGING_TIME/10.0)
        print('closing the relais')
        relais.switch_off()

        # ETHEREUM
        # now end the charging
        if not settings.DEMO:
            p = Popen(
                [
                    'node',
                    'end_charging.js',
                    client_ethereum_address,
                    settings.SERVER_ETHEREUM_ADDRESS,
                    settings.STATION_OWNER_ETH_ADDRESS
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
            print('FATAL ERROR: Could not release the booking from contract.')
            print('Suicide.')
            client_sock.close()
        else:
            print('Booking ended and station can accept new one.')

        print('FINISHED charging')
        client_sock.send(json.dumps({'electricity': '10W'}))
    else:
        print('NO electricity wanted or blockchain problem')

    print('END: regularly closing the connection')
    client_sock.close()

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 0x1001
server_sock.bind(("", port))
server_sock.listen(1)

running = True

while running:
    try:
        run(server_sock)
    except KeyboardInterrupt:
        print('keyboard interrupt')
        running = False
    # except StandardError:
    #     print('Received a protocol error')
    #     print("Unexpected error:", sys.exc_info()[0])
    #     print('... Continue the loop')
    # except:
    #     running = False

server_sock.close()
