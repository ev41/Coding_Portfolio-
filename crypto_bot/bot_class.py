"""
The code below is for a trading bot in the cryptocurrency market. The bot is designed to trade a specific digital asset called "SHIB" 
and has the ability to buy and sell it based on certain conditions.
In the beginning, the code imports several libraries that are necessary for the bot to work, including libraries for accessing trading 
data and executing trades, as well as libraries for data analysis and storage. The libraries used in this code are:

os: This library provides a way of using operating system dependent functionality such as reading or writing to environment variables, which are used 
to securely store sensitive information such as API keys.

binance.client: This library is a client for the Binance API and allows the bot to access trading data and execute trades on the Binance platform.
datetime and time: These libraries provide functions for working with dates and times, which are used to retrieve historical and real-time data 
from the market.

pandas: This library provides data structures for efficiently storing and manipulating large amounts of data, which are used to store and analyze 
the historical and real-time market data.

talib: This library provides technical analysis functions, which are used to analyze market data and make trading decisions.

robin_stocks.robinhood: This library is a client for the Robinhood API and allows the bot to execute trades on the Robinhood platform.

csv: This library provides functions for reading and writing data to and from CSV files, which are used to store data about completed trades for 
future reference.
"""

import os
from binance.client import Client
import datetime, time
import pandas as pd
import talib as ta
import robin_stocks.robinhood as rs
from csv import writer


"""
The code then defines a class called trading_bot that contains the logic for the bot. The class has several functions:

__init__: This is a special function that is called when an object of the class is created. It initializes the necessary variables and 
sets up the client objects for accessing the Binance and Robinhood APIs.
"""

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

        
        

        
"""
login: This function logs into the Robinhood API using the provided username and password, which are stored as environment variables.
"""

    def login(self):
        r_user = os.getenv("robinhood_username")
        r_pass = os.getenv("robinhood_password")

        try:
            rs.login(r_user, r_pass, expiresIn=800000)
        except Exception as e:
            print("Pickle error, manually log in with two factor auth.")


            
            
            
"""
logout: This function logs out of the Robinhood API.
"""

    def logout(self):
        rs.logout()

  




"""
price: This function retrieves the current market price of whichever digital asset is defined in the __init__ method.
"""

    def price(self):
        dct = rs.get_crypto_quote(self.symbol, info=None)
        val = dct['mark_price']
        print(val)

        
        
        
        
        

"""
hist_data: This function retrieves and stores historical market data for the specified symbol.
"""

    def hist_data(self):
        raw_data = self.client.get_historical_klines(self.symbol + 'USDT', Client.KLINE_INTERVAL_5MINUTE, "60 minutes ago UTC")
        print("pulled historical data")
        for i in raw_data:
            self.array.append(i[0:6])
        database = pd.DataFrame(data=self.array, columns = self.col_names)
        database.to_csv(self.symbol + '_data.csv', index = False)

    
    
    
    
        

"""
curr_data: This function retrieves and stores the most recent market data for the specified symbol.
"""

    def curr_data(self):
        recent_data = self.client.get_historical_klines(self.symbol + 'USDT', Client.KLINE_INTERVAL_5MINUTE, "10 minutes ago UTC")
        with open(self.symbol + '_data.csv', 'a', newline='') as thing:
            writer_object = writer(thing)
            writer_object.writerow(recent_data[0][0:6])
            thing.close()


            
            
            
"""
mfi: This function calculates the money flow index (MFI) for the stored market data, which is a technical indicator used for measuring 
buying and selling pressure. The calculated MFI is then added to the stored data.
"""


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


   

        
"""
record: This function stores information about completed trades in a CSV file for future reference.
"""


    def record(self):
        trade = [self.symbol, self.trade_type, self.purchase_prices[-1], self.quantity_purchased[-1]]
        with open ('traderecords.csv', 'a', newline='') as thing:
            write = writer(thing)
            write.writerow(trade)
            thing.close()

     
    
    
            
 """
 buy: This function executes a buy order for the specified symbol and value on the Robinhood platform.
 """

    def buy(self):
        buy_order = rs.orders.order_buy_crypto_by_price(self.symbol, self.value, jsonify=True)
        buy_price = float(rs.orders.get_all_crypto_orders(info=None)[0]['price'])
        buy_quantity = rs.orders.get_all_crypto_orders(info=None)[0]['quantity']

        self.purchase_prices.append(buy_price)
        self.quantity_purchased.append(buy_quantity)
        self.trade_type.append("Buy")
        print("Bought some ", self.symbol)



        
        

 """
 sell: This function executes a sell order for the specified symbol on the Robinhood platform, selling all of the previously purchased shares.

 """
        
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
