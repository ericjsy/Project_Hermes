#!/usr/bin/python

import threading
import requests
import os
import errno
from datetime import datetime
from datatracker.exchanges.binance import Binance
from datatracker.exchanges.bithumb import Bithumb


class Thread(threading.Thread):
    def __init__(self, source, ID, API):
        threading.Thread.__init__(self)
        self.source = source
        self.ID = ID
        self.API = API

    def run(self):
        timestamp = datetime.now().replace(microsecond=0)
        response = requests.get(self.API)
        source = None

        print("{0} - Starting thread for {1}".format(timestamp, self.source))

        if connect_to_api(response) == 1:
            print("{0} - Connection to API {1} established.".format(timestamp, self.API))

            if self.ID == "BIN":
                source = Binance(response)
            elif self.ID == "BHB":
                source = Bithumb(response)
            else:
                print("Invalid source ID provided.")

            if source is not None:
                source.extract_data()
        else:
            print("{0} - Connection to API {1} failed. "
                  "Refer to the error logs for details.".format(timestamp, self.API))

        response.close()

        print("{0} - Exiting thread for {1}".format(timestamp, self.source))


def connect_to_api(response):
    try:
        response.raise_for_status()
    except Exception as e:
        log_status_code(e, response.headers)
        response.close()
        return 0

    return 1


def log_status_code(status_code, headers):
    timestamp = datetime.now().replace(microsecond=0)

    try:
        os.makedirs("logs")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f = open("logs\errors.txt", "a+")
    f.write("[{0}] - {1} {2}\n".format(timestamp, status_code, headers))
    f.close()
