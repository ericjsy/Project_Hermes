#!/usr/bin/python

import threading
import requests
import time
from datetime import datetime
from datatracker.exchanges.binance import Binance
from datatracker.exchanges.cryptowatch import Cryptowatch
from datatracker.log import Log


class Exchange(threading.Thread):
    def __init__(self, name, ID, API, interval):
        threading.Thread.__init__(self)
        self.name = name
        self.ID = ID
        self.API = API
        self.interval = interval

    def connect_to_api(self, response):
        try:
            response.raise_for_status()
        except Exception as e:
            log = Log(self.name, e, response.headers)
            log.add_entry()
            response.close()
            return 0

        return 1

    def run(self):
        while 1:
            timestamp = datetime.now().replace(microsecond=0)
            response = requests.get(self.API)
            source = None

            print("{0} - Starting thread for {1}".format(timestamp, self.name))

            if self.connect_to_api(response) == 1:
                print("{0} - Connection to API {1} established.".format(timestamp, self.API))

                if self.ID == "BIN":
                    source = Binance(response)
                elif self.ID == "CYP":
                    source = Cryptowatch(response)
                else:
                    print("Invalid source ID provided.")

                if source is not None:
                    source.extract_data()
            else:
                print("{0} - Connection to API {1} failed. "
                      "Refer to the error logs for details.".format(timestamp, self.API))

            response.close()

            print("{0} - Exiting thread for {1}".format(timestamp, self.name))

            time.sleep(self.interval)
