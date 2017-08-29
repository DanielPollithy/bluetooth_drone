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

client_sock, address = server_sock.accept()
print("Accepted connection from ", address)

data = client_sock.recv(1024)
print("Data received: ", str(data))

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
    client_sock.send('Bad distance')
    client_sock.close()
    raise KeyboardInterrupt

# everything is o.k. The drone is close enough, so now we return the proceedings
client_sock.send('You are here my friend')

# receive the last interaction
data = client_sock.recv(1024)
print("Data received:", str(data))

client_sock.close()
server_sock.close()

