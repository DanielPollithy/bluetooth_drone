import json

import bluetooth
import time

import sys
from bt_rssi2 import BluetoothRSSI
from subprocess import Popen, PIPE

import settings
import relais


settings.activate_bluetooth_discovery('hci1')
#bt_mac = settings.get_own_bt_address()
# hack
bt_mac = settings.HIKEY_BT_ADDRESS
print('This devices bluetooth address is: {}'.format(bt_mac))


def run(server_sock):
    client_sock, address = server_sock.accept()

    # only accept the peer
    if address[0].lower() != settings.DRONE_BT_ADDRESS:
        print('Not awaited: {} (awaited)'.format(address[0].lower(), settings.DRONE_BT_ADDRESS))
        client_sock.close()
        raise StandardError

    print("Accepted connection from ", address)

    data = client_sock.recv(1024)
    print("Data received: ", str(data))
    try:
        data = json.loads(data)
        assert 'addr' in data
        client_ethereum_address = data['addr'].lower()
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
    btrssi = BluetoothRSSI(addr=address[0], dev_id=1)
    while distance < settings.RSSI_DISTANCE and try_counter < settings.MAX_RSSI_TRY_COUNT:
        try_counter += 1
        distance = btrssi.get_rssi()
        if try_counter % 10 == 0:
            print('Distance to {} at try #{}\trssi={}'.format(address, try_counter, distance))
        time.sleep(settings.DISTANCE_SLEEP)

    if distance < settings.RSSI_DISTANCE:
        print('The distance was too big to connect')
        client_sock.send(json.dumps({'accepted': False}))
        client_sock.close()
        raise StandardError

    print('Distance OK')

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


def bluetooth_routine():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 0x1001
    server_sock.bind(("", port))
    server_sock.listen(1)
    print('Bluetooth server listening')
    run(server_sock)
    server_sock.close()
    time.sleep(1)


def run_server():
    try:
        while True:
            bluetooth_routine()
    except KeyboardInterrupt:
        print('keyboard interrupt')


if __name__ == '__main__':
    relais.switch_off()
    run_server()






