import urllib
import json
import time

import settings

url = 'http://google.de'


def run():
    while True:
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        print(data)
        time.sleep(settings.WEBSITE_POLLING_SLEEP)


if __name__ == '__main__':
    run()