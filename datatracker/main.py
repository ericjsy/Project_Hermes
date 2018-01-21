from datatracker.thread import Thread

source = {
    1: {"ID": "BIN", "Name": "Binance", "API": "https://api.binance.com/api/v1/ticker/24hr?symbol=EOSBTC"},
    2: {"ID": "BHB", "Name": "Bithumb", "API": "https://api.bithumb.com/public/ticker/EOS"}
}


def main():
    threads = [Thread(source[i]["Name"], source[i]["ID"], source[i]["API"]) for i in source]

    threads[0].run()
    #threads[1].run()

if __name__ == "__main__":
    main()
