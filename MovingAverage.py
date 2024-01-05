import collections
import sqlite3

import requests
import bs4
import urllib.request, json
import os
import pandas as pd
import datetime as dt
import csv
from collections import deque

import DataScraper

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

# formula for exponential moving average
def exponentialMA(ema_queue, price, previous_ema):
    elements = len(ema_queue)
    multiplier = 2 / (elements + 1)
    EMA = (price * multiplier) + (previous_ema * (1 - multiplier))
    return EMA


def excel_report(ticker_analyzed, url_string):
    file_name = 'stock_market_data-%s.csv' % ticker_analyzed
    if not os.path.exists(file_name):
        with urllib.request.urlopen(url_string) as url:
            data = json.loads(url.read().decode())
            # pull stock market data
            try:
                data = data['Time Series (Daily)']
            except:
                print("Rate limit hit")

            # Create a queue
            five_day_queue = deque(maxlen=5)

            # Create a pandas data table
            df = pd.DataFrame(columns=['Date', 'Low', 'High', 'Close', 'Open', "EMA"])
            EMA_for_the_day = 0
            for key, val in data.items():
                date = dt.datetime.strptime(key, '%Y-%m-%d')

                # iterate values for queue
                closing_price = float(val['4. close'])
                five_day_queue.append(closing_price)
                EMA_for_the_day = exponentialMA(five_day_queue, closing_price, EMA_for_the_day)

                # populate table
                data_row = [date.date(), float(val['3. low']), float(val['2. high']),
                            closing_price, float(val['1. open']), EMA_for_the_day]
                df.loc[-1, :] = data_row
                df.index = df.index + 1

        # Convert to Excel
        df.to_csv(file_name)
        print("Generated " + file_name)

    else:
        print('Loading data from local')
        df = pd.read_csv(file_name)


# if __name__ == '__main__':
#   for ticker in DataScraper.tickers_of_the_day("Strong Buy"):
#      url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full' \
#           '&apikey=%s' % (ticker, polygon_api_key)
#    excel_report(ticker, url)
if __name__ == '__main__':
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full' \
          '&apikey=%s' % ("SNAP", alphavantage_api_key)
    excel_report("SNAP", url)
