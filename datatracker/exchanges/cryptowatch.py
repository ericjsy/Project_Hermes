#!/usr/bin/python

import psycopg2
from datetime import datetime
from datatracker.config import config
from datatracker.log import Log


class Cryptowatch():
    def __init__(self, response):
        self.response = response

    def extract_data(self):
        data = self.response.json()
        timestamp = datetime.now().replace(microsecond=0)

        conn = None

        try:
            params = config()

            print("{0} - Connecting to database...".format(timestamp))
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            print("{0} - Extracting data...".format(timestamp))
            cur.execute(
                "INSERT INTO cryptowatch.raw_data (symbol, price_change, price_change_percent, last_price, "
                "high_price, low_price, volume, quote_volume, last_updated) "
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
            log = Log("cryptowatch", e, None)
            log.add_entry()
        finally:
            if conn is not None:
                conn.close()
