# this file checks in a given interval a http endpoint for booking the drone should make

import urllib
import json
import settings

while True:
    url = 'http://localhost:8080/drone/{}/bookings'.format(settings.CLIENT_ETHEREUM_ADDRESS)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    print data