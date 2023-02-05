# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import soupsieve
import pandas as pd


def tickers_of_the_day(string_value):
    response = requests.get("https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/")

    soup = BeautifulSoup(response.text, 'html.parser')
    # find all buys,sells
    string_value_tags = soup.find_all(string=string_value)
    # find all tickers in selected filter
    tickers = []
    for tag in string_value_tags:
        ticker = tag.parent.parent.parent['data-rowkey']
        if ticker.__contains__("NYSE") or ticker.__contains__("NASDAQ"):
            ticker = ticker.split(":", 1)[1]
            tickers.append(ticker)
            print(ticker)
    return tickers