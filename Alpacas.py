import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as si
import math


class Alpacas():
    def __init__(self, api_key, api_secret):
        #authentication and connection details
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://paper-api.alpaca.markets'

        #instantiate REST API
        self.api = tradeapi.REST(self.api_key, self.api_secret, self.base_url, api_version='v2')

    def createRatios(self, stockList):
        self.stockList = stockList

        self.totalCost = (1250*len(self.stockList)) + 50000
        self.perStockAmount = self.totalCost/len(self.stockList)
        self.stockRatios = []
        for i in self.stockList:
            self.stockPrice = si.get_live_price(i)
            self.stockRatios.append([i, math.floor(self.perStockAmount/self.stockPrice)])

        return(self.stockRatios)

    def buyStocks(self, orderList):
        self.orderList = orderList

        for i in self.orderList:
            self.api.submit_order(
                symbol=i[0], 
                qty=i[1], 
                side='buy', 
                time_in_force='day',
                type='market',
                order_class="oto",
                stop_loss={'stop_price': si.get_live_price(i[0]) * 0.99}
            )

    def sellStocks(self, orderList):
        self.orderList = orderList

        for i in self.orderList:
            self.api.close_position(i)
        
    def getPositions(self):
        return(self.api.list_positions())

    def cancelAll(self):
        self.api.cancel_all_orders()

    def closeAll(self):
        self.api.close_all_positions()
