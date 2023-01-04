

import os
from binance.client import Client
import datetime, time
import pandas as pd
import talib as ta
import robin_stocks.robinhood as rs
from csv import writer


class trading_bot():
    def __init__(self):
        self.symbol = "SHIB"
        self.value = float(1)
        self.array = [[]]
        self.col_names = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        self.stamps = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        self.quantity_purchased = []
        self.purchase_prices = []
        self.trade_type = []
        self.profit = []
        self.historical_mfi = []
        self.api_key = os.getenv("api_key")
        self.api_secret = os.getenv("secret_key")
        self.client = Client(self.api_key, self.api_secret)



    def login(self):
        r_user = os.getenv("robinhood_username")
        r_pass = os.getenv("robinhood_password")

        try:
            rs.login(r_user, r_pass, expiresIn=800000)
        except Exception as e:
            print("Pickle error, manually log in with two factor auth.")




    def logout(self):
        rs.logout()




    def price(self):
        dct = rs.get_crypto_quote('ETH', info=None)
        val = dct['mark_price']
        print(val)




    def hist_data(self):
        raw_data = self.client.get_historical_klines(self.symbol + 'USDT', Client.KLINE_INTERVAL_5MINUTE, "60 minutes ago UTC")
        print("pulled historical data")
        for i in raw_data:
            self.array.append(i[0:6])
        database = pd.DataFrame(data=self.array, columns = self.col_names)
        database.to_csv(self.symbol + '_data.csv', index = False)




    def curr_data(self):
        recent_data = self.client.get_historical_klines(self.symbol + 'USDT', Client.KLINE_INTERVAL_5MINUTE, "10 minutes ago UTC")
        with open(self.symbol + '_data.csv', 'a', newline='') as thing:
            writer_object = writer(thing)
            writer_object.writerow(recent_data[0][0:6])
            thing.close()




    def mfi(self):
        df = pd.read_csv(self.symbol + '_data.csv')
        high = df['High']
        low = df['Low']
        close = df['Close']
        volume = df['Volume']

        mfi_values = ta.MFI(high, low, close, volume)
        relevant_mfi = mfi_values.iloc[-1]
        self.historical_mfi.insert(0, relevant_mfi)
        print(relevant_mfi)
        df['MFI'] = mfi_values
        df.to_csv(self.symbol + '_data.csv', index = False)




    def record(self):
        trade = [self.symbol, self.trade_type, self.purchase_prices[-1], self.quantity_purchased[-1]]
        with open ('traderecords.csv', 'a', newline='') as thing:
            write = writer(thing)
            write.writerow(trade)
            thing.close()




    def buy(self):
        buy_order = rs.orders.order_buy_crypto_by_price(self.symbol, self.value, jsonify=True)
        buy_price = float(rs.orders.get_all_crypto_orders(info=None)[0]['price'])
        buy_quantity = rs.orders.get_all_crypto_orders(info=None)[0]['quantity']

        self.purchase_prices.append(buy_price)
        self.quantity_purchased.append(buy_quantity)
        self.trade_type.append("Buy")
        print("Bought some ", self.symbol)




    def sell(self):
        rs.orders.order_sell_crypto_by_quantity(self.symbol, self.quantity_purchased[-1], jsonify=True)
        price_sold = rs.orders.get_all_crypto_orders(info=None)[0]['price']
        amt_sold = rs.orders.get_all_crypto_orders(info=None)[0]['quantity']
        profit = (float(amt_sold)*(float(price_sold))) - (float(self.purchase_prices[-1])*(float(self.quantity_purchased[-1])))

        self.profit.append(profit)
        self.purchase_prices.append(price_sold)
        self.quantity_purchased.append(amt_sold)
        self.trade_type.append("Sold")
        print("Sold some ", self.symbol)
