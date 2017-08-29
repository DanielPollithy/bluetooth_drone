# this is the address of the hikey
HIKEY_BT_ADDRESS = '98:7B:F3:19:FE:57'
# raspy
RASPY_BT_ADDRESS = 'B8:27:EB:76:09:0B'
PEER_BT_ADDRESS = HIKEY_BT_ADDRESS
BT_SLEEP = 0.01  # seconds
DISTANCE_SLEEP = 0.1

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
