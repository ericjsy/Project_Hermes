#!/usr/bin/python

"""Program execution point.

This program scrapes published information from Cryptocurrency Tickers, and
stores the relevant data into a database for further processing.
"""

import time
from datatracker.exchanges.exchange import Exchange

# Resources for Cryptocurrency exchange information.
source = {
    1: {"ID": "BIN", "Name": "Binance", "Interval": 5,
        "API": "https://api.binance.com/api/v1/ticker/24hr?symbol=EOSBTC"}
}


def main():
    """Spawn API request threads.

    A thread is created for each resource provided. Threads are passed the
    appropriate API parameters and run concurrently to allow for frequent,
    and time-sensitive data extractions.
    """

    threads = [Exchange(source[i]["Name"], source[i]["ID"], source[i]["API"]) for i in source]

    while 1:
        threads[0].run()
        time.sleep(source[1]["Interval"])


if __name__ == "__main__":
    # Execution starting point for when this module is run directly.
    main()
