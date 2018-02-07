#!/usr/bin/python

"""Program execution point.

This program scrapes published information from Cryptocurrency Tickers, and
stores the relevant data into a database for further processing.
"""

from datatracker.thread import Thread

import schedule
import time

__author__ = "Eric Sy"
__version__ = "1.0"
__date__ = "January 27, 2018"


# Resources for Cryptocurrency exchange information.
source = {
    1: {"ID": "BIN", "Name": "Binance", "Interval": 5,
        "API": "https://api.binance.com/api/v1/ticker/24hr?symbol=EOSBTC"}
}


def main():
    """Spawn API request threads.

    A thread is created for each resource provided. Threads are passed the
    appropriate API parameters and run concurrently to allow for frequent,
    and comparable data extractions.
    """

    threads = [Thread(source[i]["Name"], source[i]["ID"], source[i]["API"]) for i in source]

    for j in source:
        schedule.every(source[j]["Interval"]).seconds.do(insert_data, threads[j - 1])

    while 1:
        schedule.run_pending()
        time.sleep(1)


def insert_data(thread):
    thread.run()

if __name__ == "__main__":
    # Execution starting point for when this module is run directly.
    main()
