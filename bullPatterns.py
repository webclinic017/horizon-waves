import yfinance as yf
import matplotlib.pyplot as plt
import statistics
import math
import csv
from Alpacas import Alpacas
from datetime import datetime
import time

class posTechnicalAnalysis:
    def __init__(self, hist):
        self.stockHist = hist

    def inverseHeadAndShoulder(self):
        self.searchRange = self.stockHist[-5:]

        if (self.searchRange[2] < min(self.searchRange[0:2]+self.searchRange[3:]) and max(self.searchRange[0:5:4]) < min(self.searchRange[1:4:2])) and (((max(self.searchRange) - min(self.searchRange))/(abs(self.searchRange[0] - self.searchRange[len(self.searchRange)-1])))>=4) and (((max(self.searchRange) - min(self.searchRange))/(abs(self.searchRange[1] - self.searchRange[len(self.searchRange)-2])))>=4):
            return("InverseHeadAndShoulder", [[len(self.stockHist)-5+i, self.searchRange[i]] for i in range(len(self.searchRange))], "r", self.searchRange)
        else:
            return(self.searchRange)

    def broadeningBottom(self):
        self.searchRange = self.stockHist[-5:]
        
        if (self.searchRange[4] < self.searchRange[2] and self.searchRange[2] < self.searchRange[0]) and (self.searchRange[3] > self.searchRange[1]) and (self.searchRange[0] < self.searchRange[1]) and (self.searchRange[2] < self.searchRange[3]):
            return("broadeningBottom", [[len(self.stockHist)-5+i, self.searchRange[i]] for i in range(len(self.searchRange))], "g", self.searchRange)
        else:
            return(self.searchRange)

    def triangleTop(self):
        self.searchRange = self.stockHist[-5:]

        if (self.searchRange[0] < self.searchRange[2] < self.searchRange[4]) and (self.searchRange[1] > self.searchRange[3]) and (self.searchRange[4] < self.searchRange[3]) and (self.searchRange[2] < self.searchRange[1]) and (self.searchRange[0] < self.searchRange[1]):
            return("triangleTop", [[len(self.stockHist)-5+i, self.searchRange[i]] for i in range(len(self.searchRange))], "y", self.searchRange)
        else:
            return(self.searchRange)

    def rectangleTop(self):
        self.searchRange = self.stockHist[-5:]

        if (min(self.searchRange[1::2]) > max(self.searchRange[2::2])) and (((max(self.searchRange)-min(self.searchRange))/(max(self.searchRange[1::2])-min(self.searchRange[1::2]))) >= 20) and (((max(self.searchRange)-min(self.searchRange))/(max(self.searchRange[2::2])-min(self.searchRange[2::2]))) >= 20):
            return("rectangleTop", [[len(self.stockHist)-5+i, self.searchRange[i]] for i in range(len(self.searchRange))], "p", self.searchRange)
        else:
            return(self.searchRange)
 

    def callAll(self):
        self.info = []

        self.info.append(self.inverseHeadAndShoulder())
        self.info.append(self.broadeningBottom())
        self.info.append(self.triangleTop())
        #self.info.append(self.rectangleTop())

        return(self.info)
                
def main():

    while True:
        time.sleep(1)
        now = datetime.now()
        print("In pre cycle at {}".format(str(now)))
        if int(now.strftime("%M").split("/")[0]) > 40 and now.strftime("%H").split("/")[0] == "15" and datetime.datetime.today().weekday() < 5:
            break
                
    tickerList = []

    with open('tickers.csv') as file:
        file = csv.reader(file)
        for line in file:
            tickerList.append(str(line[0]).strip())

    count = 1

    orderList = []

    for z in tickerList:
        print(z)
        try:
            ticker = yf.Ticker(z)

            hist = ticker.history(
                start="2020-07-27",
                interval="1d"
            )

            print(z)

            trueHist = list(hist.loc[:, "Open"])

            stdev = statistics.pstdev(trueHist)

            mainPoints = [trueHist[0]]

            for i in range(1, len(trueHist)):
                if abs(trueHist[i-1] - trueHist[i]) >= stdev/5:
                    mainPoints.append(trueHist[i])

            tick = posTechnicalAnalysis(hist=mainPoints)

            patternInfo = tick.callAll()

            

            print(patternInfo, count, z)

            with plt.style.context("fivethirtyeight"):
                #fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(14, 4))

                for i in patternInfo:
                    if len(i) == 4:
                        for l in i[1]:
                            pass
                            #ax[0].scatter(l[0], l[1], color=i[2], zorder=2, s=50)
                    break

                #ax[0].plot(mainPoints, zorder=1)
                #ax[1].plot(trueHist)
                
                index = None

                for i in range(len(patternInfo)):
                    if type(patternInfo[i][0]) == str:
                        index = i

                if index != None:
                # ax[2].plot(patternInfo[index][-1])
                    #plt.savefig('graphs/{}.png'.format(z), dpi=300, bbox_inches='tight')
                    #plt.show()
                    #plt.close()
                    orderList.append(z)
                else:
                    #ax[2].plot(patternInfo[-1])
                    #plt.close()
                    pass

            

            count += 1


        except Exception as e:
            print(e)
            count += 1

    tradingAlpaca = Alpacas('PKO0LCNE1EXA2I416OSW', 'Sn8QODNTF3DmC8heyjE5u9rz8PGbM23T64gIu8Eq')
    tradingRatio = tradingAlpaca.createRatios(orderList)
    print(tradingRatio)

    while True:
        now = datetime.now()
        if int(now.strftime("%M").split("/")[0]) > 57 and now.strftime("%H").split("/")[0] == "15":
            break
    tradingAlpaca.buyStocks(tradingRatio)

if __name__ == "__main__":
    while True:
        main()
