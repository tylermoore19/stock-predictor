import datetime
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import math

#need to import strategy files to see how they have perfomed recently
import temp
import strategy_first
import strategy_second
# import strategy_second_test
import machine_learning
# import machine_learning_test

from models.stockData import (
    Stock, Links, BasicHistoricalData, FibonacciNumbers, Strategies
)

def findBasicHistoricalData(stockSymbol, start, end):
    df = web.DataReader(stockSymbol, 'yahoo', start, end)

    dates =[]
    for k in range(len(df)):
        newdate = str(df.index[k])
        newdate = newdate[0:10]
        dates.append(newdate)

    df['dates'] = dates

    df['Difference'] = df['Close'].diff()

    dfDifference = df['Difference']
    dfTodayDifference = df['Close'] - df['Open']
    dfClose = df['Close']
    dfOpen = df['Open']
    dfHigh = df['High']
    dfLow = df['Low']
    dfVolume = df['Volume']

    CLOSE = 0
    OPEN = 0
    LONG_OPEN = 0
    LONG_CLOSE = 0
    LONG_DIFFERENCE = 0
    PREVIOUS_CLOSE = 0
    DIFFERENCE = 0
    AVG_VOLUME = 0
    VOLUME = 0
    AVG_DIFFERENCE = 0
    AVG_DIFFERENCE2 = 0

    #make sure there are no NaN's in the dataset
    dfDifference.fillna(0, inplace=True)
    dfTodayDifference.fillna(0, inplace=True)
    dfClose.fillna(dfClose.mean(), inplace=True)
    dfHigh.fillna(dfHigh.mean(), inplace=True)
    dfLow.fillna(dfLow.mean(), inplace=True)
    dfOpen.fillna(dfOpen.mean(), inplace=True)

    #need to make sure DIFFERENCE is positive when we are comparing it to AVG_DIFFERENCE, cuz
    #that is also positive
    if (DIFFERENCE < 0):
        DIFFERENCE *= -1

    #need to set i to what todays date so we figure out if we should invest or not
    # ************ IMPORTANT: do not change this variable ****************
    i = len(df) - 1

    #this algorithm finds the average difference from the last 20 days
    AVG_DIFFERENCE = 0
    AVG_VOLUME = 0
    TEMP_DIFFERENCE = 0
    COUNT = 0
    j = i - 9
    while j <= i:
        #finding absolute avg difference which means we need to make sure everything is positive
        TEMP_DIFFERENCE = dfTodayDifference[j]
        if (TEMP_DIFFERENCE < 0):
            TEMP_DIFFERENCE *= -1
        AVG_DIFFERENCE += TEMP_DIFFERENCE
        AVG_VOLUME += dfVolume[j]
        COUNT += 1
        j += 1

    AVG_DIFFERENCE /= COUNT
    AVG_VOLUME /= COUNT

    AVG_DIFFERENCE2 = 0
    COUNT = 0
    j = i - 19
    while j <= i:
        #finding absolute avg difference which means we need to make sure everything is positive
        TEMP_DIFFERENCE = dfTodayDifference[j]
        if (TEMP_DIFFERENCE < 0):
            TEMP_DIFFERENCE *= -1
        AVG_DIFFERENCE2 += TEMP_DIFFERENCE
        COUNT += 1
        j += 1

    AVG_DIFFERENCE2 /= COUNT

    OPEN = dfOpen[i]
    CLOSE = dfClose[i]
    VOLUME = dfVolume[i]
    DIFFERENCE = dfDifference[i]
    TODAY_DIFFERENCE = dfTodayDifference[i]
    PREVIOUS_CLOSE = dfClose[i-1]
    NET_CHANGE = round((float(TODAY_DIFFERENCE) / float(OPEN) * 100), 2)

    LONG_OPEN = dfOpen[i - 30]
    LONG_CLOSE = dfClose[i]
    LONG_DIFFERENCE = LONG_CLOSE - LONG_OPEN

    print ("Open: " + str(OPEN))
    print ("Close: " + str(CLOSE))
    print ("Prev Close: " + str(PREVIOUS_CLOSE))
    print ("Today Difference: " + str(TODAY_DIFFERENCE))
    print ("Percent Change: " + str(NET_CHANGE) + "%")
    print ("Volume: " + str(VOLUME))
    print ("10 Day Avg Difference: " + str(AVG_DIFFERENCE))
    print ("20 Day Avg Difference: " + str(AVG_DIFFERENCE2))
    print ("30 Day Change: " + str(LONG_DIFFERENCE))

    print ('\n')
    print ("-----------\n")

    newHistoricalData = BasicHistoricalData(float(OPEN), float(CLOSE), float(PREVIOUS_CLOSE),
        float(TODAY_DIFFERENCE), (str(NET_CHANGE) + "%"), float(VOLUME), float(AVG_DIFFERENCE),
        float(AVG_DIFFERENCE2), float(LONG_DIFFERENCE))

    return newHistoricalData

def findFibonacciNumbers(stockSymbol, start, end):
    df = web.DataReader(stockSymbol, 'yahoo', start, end)

    dates =[]
    for k in range(len(df)):
        newdate = str(df.index[k])
        newdate = newdate[0:10]
        dates.append(newdate)

    df['dates'] = dates

    df['Difference'] = df['Close'].diff()

    dfDifference = df['Difference']
    dfClose = df['Close']
    dfOpen = df['Open']
    dfHigh = df['High']
    dfLow = df['Low']

    #make sure there are no NaN's in the dataset
    dfDifference.fillna(0, inplace=True)
    dfClose.fillna(dfClose.mean(), inplace=True)
    dfHigh.fillna(dfHigh.mean(), inplace=True)
    dfLow.fillna(dfLow.mean(), inplace=True)
    dfOpen.fillna(dfOpen.mean(), inplace=True)

    #need to set i to what todays date so we figure out if we should invest or not
    # ************ IMPORTANT: do not change this variable ****************
    i = len(df) - 1

    #find high and low's for last n days to calculate fib numbers
    NUMBER_OF_DAYS_FOR_FIB = 29
    FIB_HIGH = 0
    FIB_LOW = 10000000000
    j = i - NUMBER_OF_DAYS_FOR_FIB
    while j <= i:
        if dfHigh[j] > FIB_HIGH:
            FIB_HIGH = dfHigh[j]
        if dfLow[j] < FIB_LOW:
            FIB_LOW = dfLow[j]

        j += 1

    j = i - 1

    #now calculate fib numbers
    FIB_78 = FIB_HIGH * 0.786 + FIB_LOW * 0.214
    FIB_62 = FIB_HIGH * 0.618 + FIB_LOW * 0.382
    FIB_50 = FIB_HIGH * 0.5 + FIB_LOW * 0.5
    FIB_38 = FIB_HIGH * 0.382 + FIB_LOW * 0.618
    FIB_24 = FIB_HIGH * 0.236 + FIB_LOW * 0.764

    CLOSE = dfClose[i]

    FIB_ABOVE_CLOSE = 100000
    FIB_BELOW_CLOSE = 0

    #go through each fib sequence to figure out where the stock currently is
    if (CLOSE <= FIB_HIGH):
        print (str(NUMBER_OF_DAYS_FOR_FIB + 1) + " day high: " + str(FIB_HIGH))
        FIB_ABOVE_CLOSE = FIB_HIGH
        FIB_BELOW_CLOSE = FIB_78
    if (CLOSE <= FIB_78):
        print ("Fib 78: " + str(FIB_78))
        FIB_ABOVE_CLOSE = FIB_78
        FIB_BELOW_CLOSE = FIB_62
    if (CLOSE <= FIB_62):
        print ("Fib 62: " + str(FIB_62))
        FIB_ABOVE_CLOSE = FIB_62
        FIB_BELOW_CLOSE = FIB_50
    if (CLOSE <= FIB_50):
        print ("Fib 50: " + str(FIB_50))
        FIB_ABOVE_CLOSE = FIB_50
        FIB_BELOW_CLOSE = FIB_38
    if (CLOSE <= FIB_38):
        print ("Fib 38: " + str(FIB_38))
        FIB_ABOVE_CLOSE = FIB_38
        FIB_BELOW_CLOSE = FIB_24
    if (CLOSE <= FIB_24):
        print ("Fib 24: " + str(FIB_24))
        FIB_ABOVE_CLOSE = FIB_24
        FIB_BELOW_CLOSE = FIB_LOW
    if (CLOSE <= FIB_LOW):
        print (str(NUMBER_OF_DAYS_FOR_FIB + 1) + " day low: " + str(FIB_LOW))
        FIB_ABOVE_CLOSE = FIB_LOW

    print (" ------------------------- ")
    print ("| Close: " + str(CLOSE) + ' |')
    print (" ------------------------- ")

    if (CLOSE > FIB_HIGH):
        print (str(NUMBER_OF_DAYS_FOR_FIB + 1) + " day high: " + str(FIB_HIGH))
    if (CLOSE > FIB_78):
        print ("Fib 78: " + str(FIB_78))
    if (CLOSE > FIB_62):
        print ("Fib 62: " + str(FIB_62))
    if (CLOSE > FIB_50):
        print ("Fib 50: " + str(FIB_50))
    if (CLOSE > FIB_38):
        print ("Fib 38: " + str(FIB_38))
    if (CLOSE > FIB_24):
        print ("Fib 24: " + str(FIB_24))
    if (CLOSE > FIB_LOW):
        print (str(NUMBER_OF_DAYS_FOR_FIB + 1) + " day low: " + str(FIB_LOW))

    print ("\n-----------")

    #find percent changes for fib high and fib low
    percentChangeUpper = round(((FIB_ABOVE_CLOSE - CLOSE) / CLOSE) * 100, 2)
    percentChangeLower = round(((FIB_BELOW_CLOSE - CLOSE) / CLOSE) * 100, 2)
    #find values for 80% of the fib numbers because this is when you need to start looking at the stock
    fibAboveClose80Percent = (FIB_ABOVE_CLOSE * 0.8) + (CLOSE * 0.2)
    fibBelowClose80Percent = (FIB_BELOW_CLOSE * 0.8) + (CLOSE * 0.2)
    percentChangeUpper80Percent = round(((fibAboveClose80Percent - CLOSE) / CLOSE) * 100, 2)
    percentChangeLower80Percent = round(((fibBelowClose80Percent - CLOSE) / CLOSE) * 100, 2)
    #save fibonacci numbers to text file so you know when to trigger the trade
    f = open("triggers.txt", "a+")
    f.write('--------\n')
    f.write(stockSymbol + '\n')
    f.write('Normal fib values: ' + str(round(FIB_ABOVE_CLOSE, 2)) + '(' + str(percentChangeUpper) + '%) - ' + 
            str(round(CLOSE, 2)) + ' - ' + str(round(FIB_BELOW_CLOSE, 2)) + '(' + str(percentChangeLower) + '%)\n')
    f.write('80 percent fib values: ' + str(round(fibAboveClose80Percent, 2)) + '(' + str(percentChangeUpper80Percent) + '%) - ' + 
            str(round(CLOSE, 2)) + ' - ' + str(round(fibBelowClose80Percent, 2)) + '(' + str(percentChangeLower80Percent) + '%)\n')
    f.close()

    newFibonacciNumbers = FibonacciNumbers(CLOSE, FIB_HIGH, FIB_78, FIB_62, FIB_50, FIB_38, FIB_24, FIB_LOW)

    return newFibonacciNumbers

def checkStrategies(stockSymbol, stockName):

    #end = datetime.datetime(2019, 1, 4)
    #start = datetime.datetime(2018, 1, 1)
    end = datetime.date.today() + datetime.timedelta(0)
    #50 / 365 = 0.137. 0.137 * 252 (trading days) = 34 legit trading days. This function
    #needs to go back 34 days to get basic historical data
    start = end + datetime.timedelta(-50)
    newHistoricalData = findBasicHistoricalData(stockSymbol, start, end)

    #50 / 365 = 0.137. 0.137 * 252 (trading days) = 34 legit trading days. This function
    #needs to go back 34 days to get basic fibonacci numbers
    start = end + datetime.timedelta(-50)
    newFibonacciNumbers = findFibonacciNumbers(stockSymbol, start, end)

    # #doesn't need start and end times because it already does that inside of the function
    # firstStrategyPercentChange, firstStrategyBuyOrSellSignal  = strategy_first.calculateStrategy(stockSymbol)

    # # eventually, i will make two calls to function to get 50 days back as well as 365 days back to see how it's been doing over  
    # # short term but also long term 
    # start = end + datetime.timedelta(-50)
    start = end + datetime.timedelta(-365)
    firstStrategyBuyOrSellSignal, firstStrategyWinPercentageForEntireYear = temp.findWinningPercentage(stockSymbol, start, end)
    start = end + datetime.timedelta(-50)
    firstStrategyBuyOrSellSignal, firstStrategyWinPercentageForFiftyDays = temp.findWinningPercentage(stockSymbol, start, end)
    start = end + datetime.timedelta(-15)
    firstStrategyBuyOrSellSignal, firstStrategyWinPercentageForFifteenDays = temp.findWinningPercentage(stockSymbol, start, end)


    # #200 / 252 = 0.79. 0.79 * 365 = 289 real days. This strategy needs to go back 200 legit trading days
    # # (or 289 real days) to back test and come up with buy or sell signal
    start = end + datetime.timedelta(-300)
    buyOrSellSignalSecondStrategy = strategy_second.calculateStrategy(stockSymbol, stockName, start, end)

    start = end + datetime.timedelta(-289)
    thirdStrategyPredictedDifference, \
    thirdStrategyPredictedPercentDifference = machine_learning.machineLearningTest(stockSymbol, start, end)

    newStrategies = Strategies(firstStrategyBuyOrSellSignal, firstStrategyWinPercentageForEntireYear, firstStrategyWinPercentageForFiftyDays,
                        firstStrategyWinPercentageForFifteenDays, buyOrSellSignalSecondStrategy, thirdStrategyPredictedDifference,
                        thirdStrategyPredictedPercentDifference)
    # create links object 
    numberOfDaysToGoBack = 365
    links = Links(f"http://localhost:5000/secondstrategytest/{stockSymbol}/{numberOfDaysToGoBack}", 
                    f"http://localhost:5000/thirdstrategytest/{stockSymbol}/{numberOfDaysToGoBack}")

    newStock = Stock(stockName, newHistoricalData.__dict__, newFibonacciNumbers.__dict__,
                    newStrategies.__dict__, links.__dict__)
    #newStock = Stock(newHistoricalData.__dict__, newFibonacciNumbers.__dict__, newStrategies.__dict__)

    return newStock

if __name__ == '__main__':

    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO', 'GLD', 'SLV']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil', 'Gold', 'Silver']

    for x in range(0, len(stocks)):
        print (names[x], '\n')
        checkStrategies(stocks[x], names[x])
