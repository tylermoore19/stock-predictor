import pandas as pd
import datetime
import numpy as np
from ta import rsi, stoch_signal, cci, wr, macd_diff, uo, money_flow_index, ao
import pandas_datareader.data as web

def calculateStrategy(stockSymbol, stockName, start, end):
    df = web.DataReader(stockSymbol, 'yahoo', start, end)

    dates =[]
    for k in range(len(df)):
        newdate = str(df.index[k])
        newdate = newdate[0:10]
        dates.append(newdate)

    df['dates'] = dates

    df['Difference'] = df['Close'].diff()

    dfClose = df['Close']
    dfHigh = df['High']
    dfLow = df['Low']
    dfVolume = df['Volume']

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

    #need to set i to what todays date so we figure out if we should invest or not
    # ************ IMPORTANT: do not change this variable ****************
    i = len(df) - 1

    #--------RULES-------
    #plus 1 means buy stock (or invest up)
    #minus 1 means sell stock (or invest down)

    MOVING_AVERAGE_COUNT = 0
    OSCILLATOR_COUNT = 0

    #-----------------find moving averages-----------------
    if (EMA_5[i] > EMA_5[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_10[i] > EMA_10[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_20[i] > EMA_20[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_30[i] > EMA_30[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_50[i] > EMA_50[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_100[i] > EMA_100[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_200[i] > EMA_200[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1

    if (SMA_5[i] > SMA_5[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_10[i] > SMA_10[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_20[i] > SMA_20[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_30[i] > SMA_30[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_50[i] > SMA_50[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_100[i] > SMA_100[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_200[i] > SMA_200[i-1]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    #-----------------find moving averages-----------------

    #-----------------find oscillators---------------------
    if (RSI[i] < 30):
        OSCILLATOR_COUNT += 1
    elif (RSI[i] > 70):
        OSCILLATOR_COUNT -= 1
    if (STOK[i] < 30):
        OSCILLATOR_COUNT += 1
    elif (STOK[i] > 70):
        OSCILLATOR_COUNT -= 1
    if (CCI[i] < -100 and CCI[i] > CCI[i-1]):
        OSCILLATOR_COUNT += 1
    elif (CCI[i] > 100 and CCI[i] < CCI[i-1]):
        OSCILLATOR_COUNT -= 1
    # maybe do this instead (AWESOME[i] > AWESOME[i] and AWESOME[i] > 0)
    if (AWESOME[i] > AWESOME[i-1]):
        OSCILLATOR_COUNT += 1
    elif (AWESOME[i] < AWESOME[i-1]):
        OSCILLATOR_COUNT -= 1
    if (MACDHIST[i] > 0):
        OSCILLATOR_COUNT += 1
    elif (MACDHIST[i] < 0):
        OSCILLATOR_COUNT -= 1
    if (WILLIAMS[i] > -100 and WILLIAMS[i] < -75 and WILLIAMS[i] > WILLIAMS[i-1]):
        OSCILLATOR_COUNT += 1
    elif (WILLIAMS[i] < 0 and WILLIAMS[i] > -25 and WILLIAMS[i] < WILLIAMS[i-1]):
        OSCILLATOR_COUNT -= 1
    if (ULTIMATE[i] > 70):
        OSCILLATOR_COUNT += 1
    elif (ULTIMATE[i] < 30):
        OSCILLATOR_COUNT -= 1
    #-----------------find oscillators---------------------

    #-----------------now need to calculate overall summary of stock-----------
    SECOND_STRATEGY_SUMMARY = 0
    MOVING_AVERAGE_SUMMARY = 0
    OSCILLATOR_SUMMARY = 0

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

    SECOND_STRATEGY_SUMMARY = (MOVING_AVERAGE_SUMMARY + OSCILLATOR_SUMMARY) / 2

    buyOrSellSignalSecondStrategy = ""
    if (SECOND_STRATEGY_SUMMARY >= 0 and MFI[i] < 80):
        buyOrSellSignalSecondStrategy = ("Invest Up for second strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
        print ("Invest Up for second strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
    elif (SECOND_STRATEGY_SUMMARY < 0 and MFI[i] > 20):
        buyOrSellSignalSecondStrategy = ("Invest Down for second strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
        print ("Invest Down for second strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
    else:
        buyOrSellSignalSecondStrategy = ("Don't Invest for second strategy")
        print ("Don't Invest for second strategy")

    print ('\n')
    return buyOrSellSignalSecondStrategy

if __name__ == '__main__':

    #end = datetime.datetime(2019, 6, 26)
    end = datetime.date.today() + datetime.timedelta(0)

    #200 / 252 = 0.79. 0.79 * 365 = 289 real days. This strategy needs to go back 200 legit trading days
    # (or 289 real days) to back test and come up with buy or sell signal
    start = end + datetime.timedelta(-300)
    #start = datetime.datetime(2019, 4, 1)

    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil']

    for x in range(0, len(stocks)):
        print (names[x], '\n')
        calculateStrategy(stocks[x], names[x], start, end)
