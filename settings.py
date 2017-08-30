# this is the address of the hikey
HIKEY_BT_ADDRESS = '98:7B:F3:19:FE:57'
# raspy
RASPY_BT_ADDRESS = 'B8:27:EB:76:09:0B'


# for demo purpose
DEMO = False


WEBSITE_POLLING_SLEEP = 1  # seconds

BT_SLEEP = 0.01  # seconds
DISTANCE_SLEEP = 0.1

# used addresses
DRONE_BT_ADDRESS = RASPY_BT_ADDRESS
PEER_BT_ADDRESS = HIKEY_BT_ADDRESS

CHARGING_TIME = 10
DRONE_REJECTED_RESTART_TIME = 10

# eth
# this is the drone
CLIENT_ETHEREUM_ADDRESS = '0x772dcb53b59fc61410aa0514bebce8a9bb1e8ed6'

# this is the station contract
SERVER_ETHEREUM_ADDRESS = '0xc35719829b3a08211f181e22a3d93d79f4fa3ab9'
STATION_OWNER_ETH_ADDRESS = '0x0d84fe7f2011ea5253867cba1d32225b671af145'

RSSI_DISTANCE = 20
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
