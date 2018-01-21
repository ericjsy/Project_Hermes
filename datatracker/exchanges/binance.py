import psycopg2


value = {
    "symbol",
    "priceChange",
    "priceChangePercent",
    "prev"

    prevClosePrice
lastPrice
lastQty
bidPrice
askPrice
openPrice
highPrice
lowPrice
Volume
quoteVolume
Basevolume

}

class Binance():
    def __init__(self, response):
        self.response = response


    def connect_to_db(self):
        conn = psycopg2.connect("host=localhost dbname=hermes user=user1 password=admin")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO data.raw (chart_name, currency, rate, last_updated, last_inserted) "
            "VALUES (%s, %s, %s);", (value["symbol"], priceChange, datetime.now(),))

        conn.commit()
        cur.close()
        conn.close()

    def pull_data(self):
        print("Pulling data from API.")
        data = self.response.json()

        value["symbol"] = data["symbol"]
        priceChange = data["priceChange"]
