from bot_class import *


print("\n\n\n\n\n\n\n\n\n\n\n")
print("\nprogram has been started at: ", datetime.datetime.now())




pull = 0
first_buy = 0
second_buy = 0
third_buy = 0

tb = trading_bot()

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



            if tb.relevant_mfi[-1] <= 20 and first_buy ==0:
                trade1 = trading_bot()
                trade1.buy()
                trade1.record()
                first_buy +=1
                print("Ladies and Gents, we got a buy")
                time_bought = datetime.datetime.now()
                next_purch_time = time_bought + timedelta(minutes=60)



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



            elif first_buy == 1 and tb.relevant_mfi[-1] <= 20 and second_buy == 0 and datetime.datetime.now() >= next_purch_time:
                trade2 = trading_bot()
                trade2.buy()
                trade2.record()
                second_buy += 1
                time_bought_again = datetime.datetime.now()
                third_purch_time = time_bought_again + timedelta(minutes=60)
                print("Purchased more ETH")
                print(datetime.datetime.now())



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



            elif first_buy == 1 and second_buy == 1 and third_buy == 0 and tb.relevant_mfi[-1] <=20 and datetime.datetime.now() >= third_purch_time:
                trade3 = trading_bot()
                trade3.buy()
                trade3.record()
                third_purch += 1
                print("We've got another buy order")
                print(datetime.datetime.now())



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
