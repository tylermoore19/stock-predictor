import datetime
import pandas as pd
import pandas_datareader.data as web
import math
import numpy as np
from ta import rsi, stoch_signal, cci, wr, macd_diff, uo, money_flow_index, ao

from models.testData import (
    SecondStrategyTestObject
)


def findWinningPercentage(stock, start, end):
    PROFIT  = 0
    #variable to see if its swing high or swing low. swing low = 1, swing high = 2
    CLOSE = 0
    DIFFERENCE = 0
    AVG_DIFFERENCE = 0


    df = web.DataReader(stock, 'yahoo', start, end)

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


    AVG_LOSS = 0.0
    AVG_WIN = 0.0
    AVG_PERCENT_WIN = 0.0
    AVG_PERCENT_LOSS = 0.0
    WIN_COUNT = 0.0
    LOSS_COUNT = 0.0
    TEST1 = 0.0
    TEST2 = 0.0

    TOTAL_TEMP = 0.0
    TOTAL_TEMP2 = 0.0

    #make sure there are no NaN's in the dataset
    dfDifference.fillna(0, inplace=True)
    dfTodayDifference.fillna(0, inplace=True)
    dfClose.fillna(dfClose.mean(), inplace=True)
    dfHigh.fillna(dfHigh.mean(), inplace=True)
    dfLow.fillna(dfLow.mean(), inplace=True)
    dfVolume.fillna(dfVolume.mean(), inplace=True)

    EMA_5 = dfClose.ewm(span=5, adjust=False).mean()
    SMA_5 = dfClose.rolling(window=5).mean()
    EMA_10 = dfClose.ewm(span=10, adjust=False).mean()
    SMA_10 = dfClose.rolling(window=10).mean()
    EMA_20 = dfClose.ewm(span=20, adjust=False).mean()
    SMA_20 = dfClose.rolling(window=20).mean()
    EMA_30 = dfClose.ewm(span=30, adjust=False).mean()
    SMA_30 = dfClose.rolling(window=30).mean()
    EMA_50 = dfClose.ewm(span=50, adjust=False).mean()
    SMA_50 = dfClose.rolling(window=50).mean()
    EMA_100 = dfClose.ewm(span=100, adjust=False).mean()
    SMA_100 = dfClose.rolling(window=100).mean()
    EMA_200 = dfClose.ewm(span=200, adjust=False).mean()
    SMA_200 = dfClose.rolling(window=200).mean()

    RSI = rsi(dfClose, n=14, fillna=False)
    STOK = stoch_signal(dfHigh, dfLow, dfClose, n=14, d_n=3, fillna=False)
    # STOD = stoch(dfHigh, dfLow, dfClose, n=14, fillna=False)
    CCI = cci(dfHigh, dfLow, dfClose, n=20, c=0.015, fillna=False)
    WILLIAMS = wr(dfHigh, dfLow, dfClose, lbp=14, fillna=False)
    MACDHIST = macd_diff(dfClose, n_fast=12, n_slow=26, n_sign=9, fillna=False)
    ULTIMATE = uo(dfHigh, dfLow, dfClose, s=7, m=14, len=28, ws=4.0, wm=2.0, wl=1.0, fillna=False)
    MFI = money_flow_index(dfHigh, dfLow, dfClose, dfVolume, n=14, fillna=False)
    AWESOME = ao(dfHigh, dfLow, s=5, len=34, fillna=False)

    for i in range(200, len(df)):

        INVEST = 0

        AVG_DIFFERENCE = 0
        AVG_VOLUME = 0
        COUNT = 0

        LONG_HIGH = 0
        LONG_LOW = 10000000000
        HIGH = 0
        LOW = 10000000000
        TODAY_OPEN = 0
        DIFFERENCE = 0
        TEST_DIFFERENCE = 0

        LONG_HIGH = 0
        LONG_LOW = 10000000000
        j = i - 20
        while j < i:
            if dfHigh[j] > LONG_HIGH:
                LONG_HIGH = dfHigh[j]
            if dfLow[j] < LONG_LOW:
                LONG_LOW = dfLow[j]

            j += 1

        HIGH = 0
        LOW = 10000000000
        j = i - 15
        while j < (i-5):
            if dfHigh[j] > HIGH:
                HIGH = dfHigh[j]
            if dfLow[j] < LOW:
                LOW = dfLow[j]

            j += 1


        j = i - 6
        temp1 = 0
        while j < (i - 1):
            if (dfClose[j] > temp1):
                temp1 = dfClose[j]
            j += 1


        j = i - 1

        CLOSE = dfClose[j]
        DIFFERENCE = dfDifference[j]

        TODAY_OPEN = dfOpen[i]
        TEST_DIFFERENCE = dfDifference[i]
        TODAY_DIFFERENCE = dfTodayDifference[i]

        #need to make tmp_difference positive because avg_difference is positive
        #TMP_DIFFERENCE = DIFFERENCE * -1

        #need to make sure DIFFERENCE is positive when we are comparing it to AVG_DIFFERENCE, cuz
        #that is also positive
        if (DIFFERENCE < 0):
            DIFFERENCE *= -1

        COUNT = 0
        j = i - 10
        while j < i:
            AVG_DIFFERENCE += dfDifference[j]
            AVG_VOLUME += dfVolume[j]
            COUNT += 1
            j += 1

        AVG_DIFFERENCE /= COUNT
        AVG_VOLUME /= COUNT

        j = i - 1

        #-------------------------FIRST STRATEGY------------------------

        #--------RULES-------
        #plus 1 means buy stock (or invest up)
        #minus 1 means sell stock (or invest down)

        MOVING_AVERAGE_COUNT = 0
        OSCILLATOR_COUNT = 0

        #-----------------find moving averages-----------------
        if (EMA_5[j] > EMA_5[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (EMA_10[j] > EMA_10[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (EMA_20[j] > EMA_20[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (EMA_30[j] > EMA_30[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (EMA_50[j] > EMA_50[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (EMA_100[j] > EMA_100[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (EMA_200[j] > EMA_200[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1

        if (SMA_5[j] > SMA_5[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (SMA_10[j] > SMA_10[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (SMA_20[j] > SMA_20[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (SMA_30[j] > SMA_30[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (SMA_50[j] > SMA_50[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (SMA_100[j] > SMA_100[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        if (SMA_200[j] > SMA_200[j-1]):
            MOVING_AVERAGE_COUNT += 1
        else:
            MOVING_AVERAGE_COUNT -= 1
        #-----------------find moving averages-----------------

        #-----------------find oscillators---------------------
        if (RSI[j] < 30):
            OSCILLATOR_COUNT += 1
        elif (RSI[j] > 70):
            OSCILLATOR_COUNT -= 1
        if (STOK[j] < 30):
            OSCILLATOR_COUNT += 1
        elif (STOK[j] > 70):
            OSCILLATOR_COUNT -= 1
        if (CCI[j] < -100 and CCI[j] > CCI[j-1]):
            OSCILLATOR_COUNT += 1
        elif (CCI[j] > 100 and CCI[j] < CCI[j-1]):
            OSCILLATOR_COUNT -= 1
        if (AWESOME[j] > AWESOME[j-1]):
            OSCILLATOR_COUNT += 1
        elif (AWESOME[j] < AWESOME[j-1]):
            OSCILLATOR_COUNT -= 1
        if (MACDHIST[j] > 0):
            OSCILLATOR_COUNT += 1
        elif (MACDHIST[j] < 0):
            OSCILLATOR_COUNT -= 1
        if (WILLIAMS[j] > -100 and WILLIAMS[j] < -75 and WILLIAMS[j] > WILLIAMS[j-1]):
            OSCILLATOR_COUNT += 1
        elif (WILLIAMS[j] < 0 and WILLIAMS[j] > -25 and WILLIAMS[j] < WILLIAMS[j-1]):
            OSCILLATOR_COUNT -= 1
        if (ULTIMATE[j] > 70):
            OSCILLATOR_COUNT += 1
        elif (ULTIMATE[j] < 30):
            OSCILLATOR_COUNT -= 1
        #-----------------find oscillators---------------------

        #-----------------now need to calculate overall summary of stock-----------
        OVERALL_SUMMARY = 0
        MOVING_AVERAGE_SUMMARY = 0
        OSCILLATOR_SUMMARY = 0

        # if (MOVING_AVERAGE_COUNT >= 10):
        #     MOVING_AVERAGE_SUMMARY = 2
        # elif (MOVING_AVERAGE_COUNT >= 5 and MOVING_AVERAGE_COUNT < 10):
        #     MOVING_AVERAGE_SUMMARY = 1
        # elif (MOVING_AVERAGE_COUNT <= -10):
        #     MOVING_AVERAGE_SUMMARY = -2
        # elif (MOVING_AVERAGE_COUNT <= -5 and MOVING_AVERAGE_COUNT > -10):
        #     MOVING_AVERAGE_SUMMARY = -1
        # elif (MOVING_AVERAGE_COUNT > -5 and MOVING_AVERAGE_COUNT < 5):
        #     MOVING_AVERAGE_SUMMARY = 0
        #
        # if (OSCILLATOR_COUNT >= 4):
        #     OSCILLATOR_SUMMARY = 2
        # elif (OSCILLATOR_COUNT >= 2 and OSCILLATOR_COUNT < 4):
        #     OSCILLATOR_SUMMARY = 1
        # elif (OSCILLATOR_COUNT <= -4):
        #     OSCILLATOR_SUMMARY = -2
        # elif (OSCILLATOR_COUNT <= -2 and OSCILLATOR_COUNT > -4):
        #     OSCILLATOR_SUMMARY = -1
        # elif (OSCILLATOR_COUNT > -2 and OSCILLATOR_COUNT < 2):
        #     OSCILLATOR_SUMMARY = 0

        if (MOVING_AVERAGE_COUNT >= 5):
            MOVING_AVERAGE_SUMMARY = 1
        elif (MOVING_AVERAGE_COUNT <= -5):
            MOVING_AVERAGE_SUMMARY = -1
        else:
            MOVING_AVERAGE_SUMMARY = 0
        if (OSCILLATOR_COUNT >= 2):
            OSCILLATOR_SUMMARY = 1
        elif (OSCILLATOR_COUNT <= -2):
            OSCILLATOR_SUMMARY = -1
        else:
            OSCILLATOR_SUMMARY = 0

        OVERALL_SUMMARY = (MOVING_AVERAGE_SUMMARY + OSCILLATOR_SUMMARY) / 2

        #-------------------------FIRST STRATEGY------------------------


        if (OVERALL_SUMMARY >= 0 and MFI[j] < 80):
            INVEST = 2
        elif (OVERALL_SUMMARY < 0 and MFI[j] > 20):
            INVEST = 1


        if (INVEST == 2 and TODAY_OPEN > CLOSE and TEST_DIFFERENCE > 0):
            TEST1 += 1
        elif (INVEST == 1 and TODAY_OPEN < CLOSE and TEST_DIFFERENCE < 0):
            TEST1 += 1
        if (INVEST == 2 and TODAY_OPEN < CLOSE and TEST_DIFFERENCE > 0):
            TEST2 += 1
        elif (INVEST == 1 and TODAY_OPEN > CLOSE and TEST_DIFFERENCE < 0):
            TEST2 += 1
        if (INVEST == 2 and TODAY_OPEN > CLOSE):
            TOTAL_TEMP += 1
        elif (INVEST == 1 and TODAY_OPEN < CLOSE):
            TOTAL_TEMP += 1
        if (INVEST == 2 and TODAY_OPEN < CLOSE):
            TOTAL_TEMP2 += 1
        elif (INVEST == 1 and TODAY_OPEN > CLOSE):
            TOTAL_TEMP2 += 1

        #check to see if you won or not
        #we are using AVG_DIFFERENCE / 4 because in nadex, the stock price has to go up a little to win
        if (INVEST == 2 and TODAY_DIFFERENCE > 0.3):
            #WINS = WINS + 1
            WIN_COUNT += 1
            AVG_WIN += TODAY_DIFFERENCE
            AVG_PERCENT_WIN += (TODAY_DIFFERENCE / CLOSE)
            PROFIT = PROFIT + (60 * 100)
            #print "You correctly invested up! " + str(TEST_DIFFERENCE)
            #print "Close - Open: " + str(TODAY_NET)

            # print (dfDates[i])
            # print (2)

        elif (INVEST == 2 and TODAY_DIFFERENCE < 0.3):
            #LOSS = LOSS + 1
            LOSS_COUNT += 1
            TODAY_DIFFERENCE *= -1
            AVG_LOSS += TODAY_DIFFERENCE
            AVG_PERCENT_LOSS += (TODAY_DIFFERENCE / CLOSE)
            PROFIT = PROFIT - (30 * 100)
            #print "WRONG! " + str(-1 * TEST_DIFFERENCE)
            #print "Close - Open: " + str(TODAY_NET)

            # print (dfDates[i])
            # print (1)

        #TMP_DIFFERENCE is the negative version of AVG_DIFFERENCE cuz we are looking at investing down
        elif (INVEST == 1 and TODAY_DIFFERENCE < -0.3):
            #WINS = WINS + 1
            WIN_COUNT += 1
            TODAY_DIFFERENCE *= -1
            AVG_WIN += TODAY_DIFFERENCE
            AVG_PERCENT_WIN += (TODAY_DIFFERENCE / CLOSE)
            PROFIT = PROFIT + (60 * 100)
            #print "You correctly invested down! " + str(-1 * TEST_DIFFERENCE)
            #print "Close - Open: " + str(TODAY_NET)

            # print (dfDates[i])
            # print (2)

        elif (INVEST == 1 and TODAY_DIFFERENCE > -0.3):
            #LOSS = LOSS + 1
            LOSS_COUNT += 1
            AVG_LOSS += TODAY_DIFFERENCE
            AVG_PERCENT_LOSS += (TODAY_DIFFERENCE / CLOSE)
            PROFIT = PROFIT - (30 * 100)
            #print "WRONG! " + str(TEST_DIFFERENCE)
            #print "Close - Open: " + str(TODAY_NET)

            # print (dfDates[i])
            # print (1)

    WIN_PERCENTAGE = round((WIN_COUNT / (WIN_COUNT + LOSS_COUNT)) * 100, 2)
    if (TOTAL_TEMP == 0):
        TOTAL_TEMP = 1
    if (TOTAL_TEMP2 == 0):
        TOTAL_TEMP2 = 1

    print ("Investing when today open price is greater or less than close (depending on which direction you invested) and we win: " + str(round((TEST1 / TOTAL_TEMP) * 100, 2)) + "%")
    print ("Investing when today open price is opposite from above and we win: " + str(round((TEST2 / TOTAL_TEMP2) * 100, 2)) + "%")
    print ("Win Count: " + str(WIN_COUNT))
    print ("Loss Count: " + str(LOSS_COUNT))
    print ("Win Percentage: " + str(WIN_PERCENTAGE) + "%\n")

    if (LOSS_COUNT == 0 and WIN_COUNT == 0):
        print ("No trades")
    elif (LOSS_COUNT == 0):
        print ("Haven't lost\n")
        AVG_WIN = AVG_WIN / WIN_COUNT
        AVG_PERCENT_WIN = (AVG_PERCENT_WIN / WIN_COUNT) * 100
        print ("Avg Win: " + str(AVG_WIN))
        print ("Avg Percent Win: " + str(round(AVG_PERCENT_WIN, 2)) + "%")
    elif (WIN_COUNT == 0):
        print ("Haven't won\n")
        AVG_LOSS = AVG_LOSS / LOSS_COUNT
        AVG_PERCENT_LOSS = (AVG_PERCENT_LOSS / LOSS_COUNT) * 100
        print ("Avg Loss: " + str(AVG_LOSS))
        print ("Avg Percent Loss: " + str(round(AVG_PERCENT_LOSS, 2)) + "%")
    else:
        AVG_LOSS = AVG_LOSS / LOSS_COUNT
        AVG_WIN = AVG_WIN / WIN_COUNT
        AVG_PERCENT_WIN = (AVG_PERCENT_WIN / WIN_COUNT) * 100
        AVG_PERCENT_LOSS = (AVG_PERCENT_LOSS / LOSS_COUNT) * 100
        print ("Avg Win: " + str(AVG_WIN))
        print ("Avg Loss: " + str(AVG_LOSS) + "\n")
        print ("Avg Percent Win: " + str(round(AVG_PERCENT_WIN, 2)) + "%")
        print ("Avg Percent Loss: " + str(round(AVG_PERCENT_LOSS, 2)) + "%")
        #print "Wins " + str(WINS)
        #print "Losses " + str(LOSS) + '\n'
    print ("------------------------")

    investWhenOpenGreaterThanClose = round((TEST1 / TOTAL_TEMP) * 100, 2)
    investWhenOpenLessThanClose = round((TEST2 / TOTAL_TEMP2) * 100, 2)
    AVG_PERCENT_WIN = round(AVG_PERCENT_WIN, 2)
    AVG_PERCENT_LOSS = round(AVG_PERCENT_LOSS, 2)
    newTest = SecondStrategyTestObject(investWhenOpenGreaterThanClose, investWhenOpenLessThanClose, 
                WIN_COUNT, LOSS_COUNT, WIN_PERCENTAGE, AVG_WIN, AVG_LOSS, 
                AVG_PERCENT_WIN, AVG_PERCENT_LOSS, PROFIT)

    return newTest

if __name__ == '__main__':

    #start = datetime.date.today() + datetime.timedelta(-365)
    start = datetime.datetime(2018, 1, 1)
    #end = datetime.datetime(2019, 1, 1)
    end = datetime.date.today()

    print ("------------------------")

    #if it's any of the indices, natural gas or gold, invest in spreads. otherwise, do options

    #stocks = ['GLD', 'SLV', 'UNG', 'USO']
    #names = ['Gold', 'Silver', 'Natural Gas', 'Crude Oil']
    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil']
    # stocks = ['UNG']
    # names = ['Natural Gas']
    # stocks = ['FXA', 'FXE', 'FXB', 'YCS']
    # names = ['AUD/USD', 'EUR/USD', 'GBP/USD', 'USD/JPY']
    # stocks = ['FXA', 'FXE', 'FXB', 'FXA', 'YCS']
    # names = ['AUD/JPY', 'EUR/USD', 'GBP/USD', 'AUD/USD', 'USD/JPY']
    #test out ETF's following currency pairs
    #stocks = ['^IXIC', '^GSPC', '^RUT','DIA', 'GLD', 'SLV', 'CPER', 'UNG', 'USO', 'FXE', 'FXB', 'FXA', 'YCS']
    #names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Gold', 'Silver', 'Copper', 'Natural Gas', 'Crude Oil', 'EUR/USD', 'GBP/USD', 'AUD/USD', 'USD/JPY']
    #test out ETF's following currency pairs
    #FXE follows eur/usd, FXB for gbp/usd, FXA for aud/usd, YCS for usd/jpy

    WINS = 0.0
    LOSS = 0.0
    PROFIT = 0

    # for x in range(0, len(stocks)):
    #     print (str(names[x]) + "\n\n")
    #     WIN_COUNT, LOSS_COUNT, PROFIT_TEMP = findWinningPercentage(stocks[x], start, end)
    #     WINS += WIN_COUNT
    #     LOSS += LOSS_COUNT
    #     PROFIT += PROFIT_TEMP

    print ("------------------------")
    print ('\n')

    TOTAL = WINS + LOSS

    print ("Wins " + str(WINS))
    print ("Losses " + str(LOSS))
    print ("Total: " + str(TOTAL) + '\n')

    TOTAL = float(TOTAL)
    WIN_PERCENTAGE = (WINS / TOTAL)
    WIN_PERCENTAGE *= 100
    print ("Win Percentage: " + str(round(WIN_PERCENTAGE, 2)) + "%")

    print ("Net Profit " + str(PROFIT) + '\n')

    print ("------------------------")
