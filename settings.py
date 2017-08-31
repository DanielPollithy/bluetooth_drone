# this is the address of the hikey
HIKEY_BT_ADDRESS = '98:7B:F3:19:FE:57'.lower()
HIKEY_IP_ADDRESS = '192.168.1.139'.lower()
# raspy
RASPY_BT_ADDRESS = 'B8:27:EB:1F:94:78'.lower()
RASPY_IP_ADDRESS = '192.168.1.106'.lower()


# for demo purpose
DEMO = True


BT_SLEEP = 0.01  # seconds
DISTANCE_SLEEP = 0.1

# used addresses
DRONE_BT_ADDRESS = RASPY_BT_ADDRESS
PEER_BT_ADDRESS = HIKEY_BT_ADDRESS

CHARGING_TIME = 10
DRONE_REJECTED_RESTART_TIME = 10

# eth
# this is the drone
CLIENT_ETHEREUM_ADDRESS = '0x00928C4Ce6be59B078350a548E739D5086FEf872'

# this is the station contract
SERVER_ETHEREUM_ADDRESS = '0x5d7CF9F787E89C73Bcb15393520bFe6aF4098bB8'
STATION_OWNER_ETH_ADDRESS = '0x00DEa97B0E2a09b932b67079c184c2284d0880c0'

WEBSITE_POLLING_SLEEP = 10  # seconds
WEBSITE_POLLING_URL = 'http://iotwist.com:8200/api/drone/bookings/{}'.format(CLIENT_ETHEREUM_ADDRESS)
WEBSITE_STATUS_URL =  'http://iotwist.com:8200/api/drone/status/{}'.format(CLIENT_ETHEREUM_ADDRESS)

RSSI_DISTANCE = 10
MAX_RSSI_TRY_COUNT = 10000

from subprocess import Popen, PIPE
import re


def get_own_bt_address():
    p = Popen(['hcitool', 'dev'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    returncode = p.returncode
    regex = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    test_str = output
    matches = re.finditer(regex, test_str)

    numMatches = 0
    bt_addresses = []

    for match in matches:
        numMatches+=1
        bt_addr = '{match}'.format(match=match.group())
        bt_addresses.append(bt_addr)

    return bt_addresses[0]


def activate_bluetooth_discovery():
    p = Popen(['sudo', 'hciconfig', 'hci0', 'piscan'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.wait()
