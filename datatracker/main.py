#!/usr/bin/python

"""Program execution point.

This program scrapes published information from Cryptocurrency Tickers,
and stores the relevant data into a database for further processing.
"""

from datatracker.exchanges.binance import Binance
from datatracker.exchanges.cryptowatch import Cryptowatch

# Resources for Cryptocurrency exchange information.
sources = {
    1: Binance(),
    2: Cryptowatch()
}


def main():
    """Spawn API request threads.

    A thread is created for each established resource to allow for
    concurrent extractions. Each thread has a defined request interval
    in coordination with the APIs request limit.
    """

    for i in sources:
        sources[i].start()

if __name__ == "__main__":
    # Execution starting point for when this module is run directly.
    main()
