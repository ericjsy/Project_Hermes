#!/usr/bin/python

"""Cryptowatch cryptocurrency exchange.

Gathers market summaries from Cryptowatch and stores the raw information
into the datahub. The rate limit is set to 8 seconds of CPU time per hour
as per the cryptowatch documentation: https://cryptowat.ch/docs/api.
"""

import psycopg2
import threading
import requests
import time

from datetime import datetime
from datatracker.utility.config import config
from datatracker.utility.log import Log
from datatracker.utility.connect import connect_to_api


class Cryptowatch(threading.Thread):
    def __init__(self):
        """Thread parameters.

        Sets up API endpoint and request interval in seconds.
        """

        threading.Thread.__init__(self)
        self.api = "https://api.cryptowat.ch/markets/summaries"
        self.interval = 10
        self.active = True

    def extract_data(self, response):
        """Database insertion method.

        Pulls json data from Cryptowatch and inserts the data into the
        database.

        :param response: the API response
        """

        data = response.json()
        timestamp = datetime.now().replace(microsecond=0)

        conn = None

        try:
            params = config()

            print("{0} - Connecting to database...".format(timestamp))
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            print("{0} - Extracting data...".format(timestamp))
            cur.execute(
                "INSERT INTO cryptowatch.raw_data (symbol, price_change, "
                "price_change_percent, last_price, high_price, low_price, "
                "volume, quote_volume, last_updated) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (
                    "EOSBTC",
                    data["result"]["bitfinex:eoseth"]["price"]["change"]["absolute"],
                    data["result"]["bitfinex:eoseth"]["price"]["change"]["percentage"],
                    data["result"]["bitfinex:eoseth"]["price"]["last"],
                    data["result"]["bitfinex:eoseth"]["price"]["high"],
                    data["result"]["bitfinex:eoseth"]["price"]["low"],
                    data["result"]["bitfinex:eoseth"]["volume"],
                    data["result"]["bitfinex:eoseth"]["volumeQuote"],
                    datetime.now().replace(microsecond=0),))

            conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print("{0} - Failed to populate database with data. "
                  "Refer to the error logs for details.".format(timestamp))
            log = Log(self.getName(), e, None)
            log.add_entry()
        finally:
            if conn is not None:
                conn.close()

    def run(self):
        """Initiates thread actions.

        Pings the API and handles the response.
        """

        while self.active:
            timestamp = datetime.now().replace(microsecond=0)
            response = requests.get(self.api)

            print("{0} - Starting thread for {1}".format(timestamp, self.getName()))

            if connect_to_api(self, response) == 1:
                print("{0} - Connection to API {1} established.".format(timestamp, self.api))
                self.extract_data(response)
            else:
                print("{0} - Connection to API {1} failed. "
                      "Refer to the error logs for details.".format(timestamp, self.api))

            response.close()

            print("{0} - Exiting thread for {1}".format(timestamp, self.getName()))

            time.sleep(self.interval)

    def getName(self):
        """Name retrieval helper function.

        Retrieves the name of the cryptocurrency exchange.

        :return: the class name
        """

        return self.__class__.__name__
