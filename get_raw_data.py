import requests
import sqlite3
import os

conn = None
db_name = "db.sqlite3"

def request_api(symbol):

    conn = None
    try:
        
        api_key = os.environ.get('API_KEY')

        if not api_key:
            print("API Key not found")
            return

        endpoint = "https://www.alphavantage.co/query"

        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": api_key
        }

        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        response = requests.get(endpoint, params=params) 

        if response.status_code == 200:
            data = response.json()
            # print(data)
            series = data["Time Series (Daily)"]

            print("Symbol:", symbol)

            # Connect to the db
            conn = sqlite3.connect(db_name)

            # Cursor object
            cursor = conn.cursor()

            # key is date 
            for date in series.keys():

                date_data = series[date]
                open_price = date_data['1. open']
                close_price = date_data['5. adjusted close']
                volume = date_data['6. volume']

                print(f'symbol: {symbol}')
                print(f'date: {date}')
                print(f'open_price: {open_price}')
                print(f'close_price: {close_price}')
                print(f'volume: {volume}')

                # Insert query
                data = (symbol, date, open_price, close_price, volume)
                cursor.execute("INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES (?, ?, ?, ?, ?)" , data)

                # Commit changes
                conn.commit()
            
            # Close connection
            conn.close()
            conn = None
        else:
            print("Request failed with status code:", response.status_code)

    except BaseException as ex:
        print(f'Exception was thrown: {ex}')
    finally:
        if conn is not None:
            conn.close()
            conn = None

def insert_data():
    # IBM
    request_api("IBM")
    # Apple
    request_api("AAPL")

def main():
    insert_data()

if __name__ == '__main__':
    main()