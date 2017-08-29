import bluetooth

import settings

bt_mac = settings.get_own_bt_address()
print('This devices bluetooth address is: {}'.format(bt_mac))

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 0x1001

server_sock.bind(("", port))
server_sock.listen(1)

client_sock = False

try:
    client_sock, address = server_sock.accept()
    print("Accepted connection from ", address)

    data = client_sock.recv(1024)
    print("Data received: ", str(data))

    while data:
        client_sock.send('Echo => ' + str(data))
        data = client_sock.recv(1024)
        print("Data received:", str(data))
except KeyboardInterrupt:
    print("closing")
finally:
    if client_sock:
        client_sock.close()
    server_sock.close()

