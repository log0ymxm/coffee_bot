import time
import os
from datetime import datetime

import redis

from smartplug import SmartPlug

REDIS_URL = os.environ.get('REDIS_URL', 'localhost')
PLUG_IP = os.environ.get('PLUG_IP', '172.16.100.75')
PLUG_USER = os.environ.get('PLUG_USER', 'admin')
PLUG_PW = os.environ.get('PLUG_PW', '1234')

# Regularly log current & power draw so we can estimate
# a heuristic rule for when the coffee is finished after
# we've seen it run
def main():
    print('Starting Coffee Bot')

    r = redis.StrictRedis(host=REDIS_URL)
    plug = SmartPlug(PLUG_IP, (PLUG_USER, PLUG_PW))

    while True:
        now = datetime.now().timestamp()
        try:
            power = plug.power
            current = plug.current
            print('Plug', now, plug.state, power, current)
            r.zadd('coffee_bot_stats', now, json.dumps({'power': power, 'current': current}))
        except Exception as e:
            print('Error', now, str(e))
        print('Sleeping')
        time.sleep(1)

if __name__ == "__main__":
    main()
