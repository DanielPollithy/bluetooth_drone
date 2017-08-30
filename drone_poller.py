import urllib
import json
import time
import urllib2

from subprocess import Popen, PIPE

import sys

import settings

# array of booking numbers
booking_history = []


def notify_website():
    with open('connection_state.txt', 'r') as inp:
        data = json.loads(inp.read())

    req = urllib2.Request(settings.WEBSITE_STATUS_URL)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))


def poll_website():
    response = urllib.urlopen(settings.WEBSITE_POLLING_URL)
    data = json.loads(response.read())
    print(data)
    for booked_station in data:
        if booked_station['id'] and booked_station['id'] not in booking_history and \
                booked_station['station']:
            print('received a new booking')
            # ETHEREUM
            # now end the charging
            if not settings.DEMO:
                p = Popen(
                    [
                        'node',
                        'make_booking.js',
                        settings.CLIENT_ETHEREUM_ADDRESS,
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

            if returncode == 0:
                print('Booking was done successfully!')
            else:
                print('ERROR! There was a problem with the booking or with the blockchain contract')


def run():
    while True:
        try:
            # send my own data
            notify_website()
        except:
            print('[x] Could not notify the website')
            print("Unexpected error:", sys.exc_info()[0])

        try:
            # receive new bookings
            poll_website()
        except :
            print('[x] Could not fetch bookings from the website')
            print("Unexpected error:", sys.exc_info()[0])

        time.sleep(settings.WEBSITE_POLLING_SLEEP)


if __name__ == '__main__':
    run()
