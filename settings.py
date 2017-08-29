# this is the address of the hikey
# PEER_BT_ADDRESS = '98:7B:F3:19:FE:57'
PEER_BT_ADDRESS = '7C:E9:D3:DD:66:23'
BT_SLEEP = 2  # seconds

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

