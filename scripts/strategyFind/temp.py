import requests
import pandas as pd
import pandas_datareader.data as web
import math
import numpy as np
import arrow
import datetime
from ta import acc_dist_index, chaikin_money_flow, force_index, negative_volume_index, on_balance_volume, put_call_ratio, volume_price_trend

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
    df['prevClose'] = df['Close'].shift(1)

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
    df = df.groupby(df.columns, axis = 1).transform(lambda x: x.fillna(x.mean()))

    df['percentChange'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    df['absPercentChange'] = abs(df['percentChange'])
    df['tomorrowAbsPercentChange'] = df['absPercentChange'].shift(-1)

    ADI = acc_dist_index(df['High'], df['Low'], df['Close'], df['Volume'], fillna=False)
    CMF = chaikin_money_flow(df['High'], df['Low'], df['Close'], df['Volume'], n=10, fillna=False)
    FI = force_index(df['Close'], df['Volume'], n=2, fillna=False)
    NVI = negative_volume_index(df['Close'], df['Volume'], fillna=False)
    OBV = on_balance_volume(df['Close'], df['Volume'], fillna=False)
    PCR = put_call_ratio()
    VPT = volume_price_trend(df['Close'], df['Volume'], fillna=False)
    # print (NVI)
    # print (df['absPercentChange'])

    strategy = df[['absPercentChange', 'tomorrowAbsPercentChange', 'Volume']].copy()
    strategy['3_MA_PRICE'] = df['absPercentChange'].rolling(window=3).mean()
    strategy['3_MA_VOLUME'] = df['Volume'].rolling(window=3).mean()

    # figure out which one of the two strategies to use

    strategy.loc[(strategy['3_MA_PRICE'] >= strategy['absPercentChange'], 'predictPrice')] = 1
    strategy.loc[(strategy['3_MA_PRICE'] < strategy['absPercentChange'], 'predictPrice')] = 0
    strategy.loc[(strategy['3_MA_VOLUME'] >= strategy['Volume'], 'predictVolume')] = 1
    strategy.loc[(strategy['3_MA_VOLUME'] < strategy['Volume'], 'predictVolume')] = 0

    # strategy.loc[(strategy['absPercentChange'] >= strategy['3_MA_PRICE'], 'predictPrice')] = 1
    # strategy.loc[(strategy['absPercentChange'] < strategy['3_MA_PRICE'], 'predictPrice')] = 0
    # strategy.loc[(strategy['Volume'] >= strategy['3_MA_VOLUME'], 'predictVolume')] = 1
    # strategy.loc[(strategy['Volume'] < strategy['3_MA_VOLUME'], 'predictVolume')] = 0

    

    strategy.loc[((strategy['predictPrice'] == 1) & (strategy['predictVolume'] == 1), 'predict')] = 1
    strategy.loc[((strategy['predictPrice'] == 0) | (strategy['predictVolume'] == 0), 'predict')] = 0

    #split up train and test dataset
    test = strategy.iloc[-1:]
    strategy = strategy.iloc[:-1]

    print (strategy.tail(15))
    print (test.to_string())
    print ('\n')
    print ('Prediction: ' + str(test['predict'][0]))


    # ****** TODO most of these show strong trends (up or down) when the number is higher or lower than usual. for example, if indicator 
    # is higher than 75% of the other data or lower than 25%, this could be a signal for a big price change the next day

    if (stock == 'UNG' or stock == 'USO'):   
        winPercentage = strategy.loc[(strategy['tomorrowAbsPercentChange'] > 1) & (strategy['predict'] == 1)].count() / strategy.loc[(strategy['predict'] == 1)].count()
        winPercentage = round((winPercentage * 100), 2)
        print ('Win Percentage: ' + str(winPercentage['predict']))
    elif (stock == 'GLD' or stock == 'SLV'):
        winPercentage = strategy.loc[(strategy['tomorrowAbsPercentChange'] > 0.5) & (strategy['predict'] == 1)].count() / strategy.loc[(strategy['predict'] == 1)].count()
        winPercentage = round((winPercentage * 100), 2)
        print ('Win Percentage: ' + str(winPercentage['predict']))
    else:
        # print (strategy.loc[(strategy['tomorrowAbsPercentChange'] > 0.4) & (strategy['predict'] == 1)].count())
        # print (strategy.loc[(strategy['predict'] == 1)].count())
        winPercentage = strategy.loc[(strategy['tomorrowAbsPercentChange'] > 0.4) & (strategy['predict'] == 1)].count() / strategy.loc[(strategy['predict'] == 1)].count()
        winPercentage = round((winPercentage * 100), 2)
        print ('Win Percentage: ' + str(winPercentage['predict']))
    return (test['predict'][0], winPercentage['predict'])

if __name__ == '__main__':
    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO', 'GLD', 'SLV']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil', 'Gold', 'Silver']

    #end = datetime.datetime(2019, 1, 1)
    end = datetime.date.today()

    for x in range(0, len(stocks)):
        print ("------------------------")
        print (names[x], '\n')
        # start = datetime.datetime(2018, 1, 1)
        start = end + datetime.timedelta(-365)
        prediction, winPercentageForEntireYear = findWinningPercentage(stocks[x], start, end)
        start = end + datetime.timedelta(-50)
        prediction, winPercentageForFiftyDays = findWinningPercentage(stocks[x], start, end)
        start = end + datetime.timedelta(-15)
        prediction, winPercentageForFifteenDays = findWinningPercentage(stocks[x], start, end)