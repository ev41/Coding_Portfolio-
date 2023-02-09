"""
This code is an implementation of a trading bot that trades cryptocurrency. 
It uses the Moving Average Frustration Index (MFI) to determine when to buy or sell the user-selected digital asset.
"""

from bot_class import *


print("\n\n\n\n\n\n\n\n\n\n\n")
print("\nprogram has been started at: ", datetime.datetime.now())


"""
The code first initializes variables pull, first_buy, second_buy, and third_buy to 
keep track of the state of the bot's trading actions. 

Then, it creates an instance of the trading_bot class (tb).
"""

pull = 0
first_buy = 0
second_buy = 0
third_buy = 0

tb = trading_bot()





"""
The bot enters an infinite loop and waits until the current second of the system clock is equal to 0 (first code block below this text). 
Then, it retrieves historical and current data and calculates the MFI (second code block below this text).
"""

while True:
    while pull == 0:
        if datetime.datetime.now().second == 00:
            tb.hist_data()
            pull += 1
            tb.rlogin()
            time.sleep(50)



    while pull == 1:
        if datetime.datetime.now().second == 00:
            tb.curr_data()
            tb.mfi()


            
            
            
            
            
            
    """
    If the current MFI is less than or equal to 20 and first_buy is 0, 
    the bot buys the user-selected digital asset and records the trade. It sets first_buy to 1 and sets next_purch_time to be 60 minutes later.
    """

            if tb.relevant_mfi[-1] <= 20 and first_buy ==0:
                trade1 = trading_bot()
                trade1.buy()
                trade1.record()
                first_buy +=1
                print("Ladies and Gents, we got a buy")
                time_bought = datetime.datetime.now()
                next_purch_time = time_bought + timedelta(minutes=60)

    
    
    
    
                
                
"""
If first_buy is 1 and the current MFI is greater than or equal to 80, the bot checks the current value of the user-selected digital asset. 
If it is less than or equal to 96% of the purchase price or greater than or equal to 101% of the purchase price, 
the bot sells the user-selected digital asset and records the trade.
"""
                
                

            elif tb.relevant_mfi[-1] >= 80 and first_buy == 1:
                #building the stop-loss order
                dct = rs.get_crypto_quote('ETH', info=None)
                val = dct['mark_price']
                if val <= (self.purchase_prices[-1] * 0.96) or val >= (self.purchase_prices[-1] * 1.01):
                    trade1.sell()
                    trade1.record()
                    first_buy -= 1
                    print("Ladies and gents! We got a sale!")
                    print(datetime.datetime.now())
                else:
                    pass

                
                
                
                
                
 """
 Similarly, if first_buy is 1 and second_buy is 0, and the current MFI is less than or equal to 20 and 
 the current time is greater than or equal to next_purch_time, the bot buys more Ethereum, records the trade, and sets second_buy to 1. 
 It also sets third_purch_time to be 60 minutes later.
 """

            elif first_buy == 1 and tb.relevant_mfi[-1] <= 20 and second_buy == 0 and datetime.datetime.now() >= next_purch_time:
                trade2 = trading_bot()
                trade2.buy()
                trade2.record()
                second_buy += 1
                time_bought_again = datetime.datetime.now()
                third_purch_time = time_bought_again + timedelta(minutes=60)
                print("Purchased more ETH")
                print(datetime.datetime.now())


                
                
                
                
                
 """
 If second_buy is 1 and the current MFI is greater than or equal to 80, the bot checks the digital asset's value 
 and sells if necessary.
 """

            elif second_buy == 1 and tb.relevant_mfi[-1] >= 80:
                dct = rs.get_crypto_quote('ETH', info=None)
                val = dct['mark_price']
                if val <= (self.purchase_prices[-1] * 0.96) or val >= (self.purchase_prices[-1] * 1.01):
                    trade2.sell()
                    trade2.record()
                    sec_purch -= 1
                    print("Ladies and gents! We got more sales!")
                    print(datetime.datetime.now())
                else:
                    pass


                
                
                
   """
   If first_buy is 1, second_buy is 1, and third_buy is 0, and the current MFI is less than or equal to 20 
   and the current time is greater than or equal to third_purch_time, the bot buys even more Ethereum, records the trade, and sets third_buy to 1.
   """

            elif first_buy == 1 and second_buy == 1 and third_buy == 0 and tb.relevant_mfi[-1] <=20 and datetime.datetime.now() >= third_purch_time:
                trade3 = trading_bot()
                trade3.buy()
                trade3.record()
                third_purch += 1
                print("We've got another buy order")
                print(datetime.datetime.now())


                
                
                
"""
If third_buy is 1 and the current MFI is greater than or equal to 80, the bot checks the value of Ethereum and sells if necessary.
"""

            elif third_purch == 1 and tb.relevant_mfi[-1=] >= 80:
                dct = rs.get_crypto_quote('ETH', info=None)
                val = dct['mark_price']
                if val <= (self.purchase_prices[-1] * 0.96) or val >= (self.purchase_prices[-1] * 1.01):
                    trade3.sell()
                    trade3.record()
                    third_purch -= 1
                    print("Completed another sell")
                    print(datetime.datetime.now())
            time.sleep(60)
            
            
            
            
"""
The bot continues this loop, checking the MFI and making trades as necessary, every 60 seconds.
"""
