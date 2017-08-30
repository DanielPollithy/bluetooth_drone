import urllib
import json
import time

import settings

url = 'http://google.de'


def run():
    while True:
        try:
            response = urllib.urlopen(url)
            print(response.read())
            data = json.loads(response.read())
            print(data)
        except:
            print('No valid connection to the website')
            pass
        time.sleep(settings.WEBSITE_POLLING_SLEEP)


if __name__ == '__main__':
    run()
