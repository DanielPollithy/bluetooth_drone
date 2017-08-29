# this is the address of the hikey
HIKEY_BT_ADDRESS = '98:7B:F3:19:FE:57'
# raspy
RASPY_BT_ADDRESS = 'B8:27:EB:76:09:0B'
PEER_BT_ADDRESS = HIKEY_BT_ADDRESS
BT_SLEEP = 0.01  # seconds
DISTANCE_SLEEP = 0.1

CHARGING_TIME = 10

# eth
CLIENT_ETHEREUM_ADDRESS = '0xde0b2sdsdsddddddddddddddddddddddddddddde'
SERVER_ETHEREUM_ADDRESS = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'

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
