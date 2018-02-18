#!/usr/bin/python

import psycopg2
from datetime import datetime
from datatracker.config import config
from datatracker.log import Log


class Binance():
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
                "INSERT INTO binance.raw_data (symbol, price_change, price_change_percent, prev_close_price, "
                "last_price, last_qty, bid_price, ask_price, open_price, high_price, low_price, volume, "
                "quote_volume, last_updated) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (
                    data["symbol"],
                    data["priceChange"],
                    data["priceChangePercent"],
                    data["prevClosePrice"],
                    data["lastPrice"],
                    data["lastQty"],
                    data["bidPrice"],
                    data["askPrice"],
                    data["openPrice"],
                    data["highPrice"],
                    data["lowPrice"],
                    data["volume"],
                    data["quoteVolume"],
                    datetime.now().replace(microsecond=0),))

            conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print("{0} - Failed to populate database with data. "
                  "Refer to the error logs for details.".format(timestamp))
            log = Log("binance", e, None)
            log.add_entry()
        finally:
            if conn is not None:
                conn.close()
