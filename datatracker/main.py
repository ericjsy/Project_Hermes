#!/usr/bin/python

"""Program execution point.

This program scrapes published information from Cryptocurrency Tickers, and
stores the relevant data into a database for further processing.
"""

from datatracker.exchanges.exchange import Exchange

# Resources for Cryptocurrency exchange information.
source = {
    1: {"ID": "BIN", "Name": "Binance", "Interval": 5,
        "API": "https://api.binance.com/api/v1/ticker/24hr?symbol=EOSBTC"},
    2: {"ID": "CYP", "Name": "Cryptowatch", "Interval": 86400,
        "API": "https://api.cryptowat.ch/markets/summaries"}
}


def main():
    """Spawn API request threads.

    A thread is created for each resource provided. Threads are passed the
    appropriate API parameters and run concurrently to allow for frequent,
    and time-sensitive data extractions.
    """

    threads = [Exchange(source[i]["Name"], source[i]["ID"],
                        source[i]["API"], source[i]["Interval"]) for i in source]

    for i in source:
        threads[i - 1].start()


if __name__ == "__main__":
    # Execution starting point for when this module is run directly.
    main()
