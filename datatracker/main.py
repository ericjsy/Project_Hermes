#!/usr/bin/python

"""Program execution point.

This program scrapes published information from Cryptocurrency Tickers, and
stores the relevant data into a database for further processing.
"""

from datatracker.thread import Thread

__author__ = "Eric Sy"
__version__ = "1.0"
__date__ = "January 27, 2018"


# Resources for Cryptocurrency exchange information.
source = {
    1: {"ID": "BIN", "Name": "Binance",
        "API": "https://api.binance.com/api/v1/ticker/24hr?symbol=EOSBTC"},
    2: {"ID": "BHB", "Name": "Bithumb",
        "API": "https://api.bithumb.com/public/ticker/EOS"}
}


def main():
    """Spawn API request threads.

    A thread is created for each resource provided. Threads are passed the
    appropriate API parameters and run concurrently to allow for frequent,
    and comparable data extractions.
    """

    threads = [Thread(source[i]["Name"], source[i]["ID"], source[i]["API"])
               for i in source]

    threads[0].run()
    #threads[1].run()


if __name__ == "__main__":
    # Execution starting point for when this module is run directly.
    main()
