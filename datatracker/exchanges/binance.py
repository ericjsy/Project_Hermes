import psycopg2
import os
import errno
from datetime import datetime
from datatracker.config import config


class Binance():
    def __init__(self, response):
        self.response = response

    def extract_data(self):
        data = self.response.json()
        timestamp = datetime.now().replace(microsecond=0)

        conn = None
        cur = None

        try:
            params = config()

            print("{} - Connecting to database...".format(timestamp))
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO data.raw (symbol, price_change, price_change_percent, prev_close_price, "
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
            print("{} - Failed to populate database with data. "
                  "Refer to the error logs for details.".format(timestamp))
            log_db_code(e)
        finally:
            if conn is not None:
                conn.close()

            if cur is not None:
                cur.close()


def log_db_code(error):
    timestamp = datetime.now().replace(microsecond=0)

    try:
        os.makedirs("logs")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f = open("logs\errors.txt", "a+")
    f.write("[{}] - {}\n".format(timestamp, error))
    f.close()