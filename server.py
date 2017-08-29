import json

import bluetooth
import time
from bt_proximity import BluetoothRSSI
import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 0x1001

server_sock.bind(("", port))
server_sock.listen(1)

while True:
    client_sock, address = server_sock.accept()

    # only accept the peer
    if address[0] != settings.PEER_BT_ADDRESS:
        client_sock.close()

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
        raise KeyboardInterrupt

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
        time.sleep(settings.CHARGING_TIME)
        client_sock.send(json.dumps({'electricity': '10W'}))
        client_sock.close()
    else:
        print('NO electricity wanted')
        client_sock.close()

    client_sock.close()
server_sock.close()

