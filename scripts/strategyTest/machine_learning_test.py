import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import math

from models.testData import (
    ThirdStrategyTestObject
)

#from pandas_datareader import data as web
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.metrics import accuracy_score

import seaborn

def findWinningPercentage(stock, start, end):

    WIN_COUNT = 0.0
    LOSS_COUNT = 0.0

    dfMain = web.DataReader(stock, 'yahoo', start, end)

    #print(dfMain.to_string())

    timeframe = 200
    num_days = 1
    #we need to stop the loop at  len(dfMain) - n because the end date needs enough room to calculate
    #the buy or sell signals
    i = len(dfMain) - (timeframe - 1)
    # i = len(dfMain) - (27)
    j = 0
    # test_data = 0
    # test_data2 = 0
    while j < i:
        #need to add j to the start date to keep changing the dataframe to test a new day
        # start = start + datetime.timedelta(num_days)
        # end = start + datetime.timedelta(timeframe)

        #df = web.DataReader(stocks[x], 'yahoo', start, end)
        df = dfMain[j:j + timeframe]
        # print (df)
        # print ('----')

        dfActual = np.array(df['Adj Close'])
        df = df[['Adj Close']]

        # df = df[['Adj Close']]
        # df['Moving Average'] = df.rolling(window=5).mean()
        # df = df[['Moving Average']]
        # df.fillna(df.mean(), inplace=True)

        forecast_out = int(1) # predicting n days into future
        #print (len(df))
        df['Prediction'] = df[['Adj Close']].shift(-forecast_out) #  label column with data shifted n units up

        X = np.array(df.drop(['Prediction'], 1))
        X = preprocessing.scale(X)

        #example, if we are trying to predict if the 3rd will go up or down, need to get every
        #data in the set except for the 3rd and 4th so we can train the data, and then predict if the 3rd
        #will go up or down. we will use the 4th datapoint to see if we were correct
        X_forecast = X[(-forecast_out - 1):]

        X = X[:(-forecast_out - 1)] # remove last n days from X since we will use these values to predict n days into future
        #print (X)

        y = np.array(df['Prediction'])
        y = y[:(-forecast_out - 1)] #same for y

        #also get last two data points for adj closed to see if our prediction was right
        dfActual = dfActual[(-forecast_out - 1):]

        forecast_prediction = []
        confidence = []
        #do the machine learning algo 10 times and then average the results to get a better understanding
        #of what the stock is going to do
        for k in range(0, 10):

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)
            # X_train, X_test, y_train, y_test = train_test_split(X, y)

            # Training
            clf = LinearRegression()
            clf.fit(X_train,y_train)

            # Testing
            confidence.append(clf.score(X_test, y_test))

            forecast = clf.predict(X_forecast)
            forecast_prediction.append(forecast[0])

        confidence = np.mean(confidence)
        #print("confidence: " + str(round(confidence * 100,2)) + '%')

        forecast_prediction = np.mean(forecast_prediction)
        #print (forecast_prediction)
        #forecast_prediction = np.append(y_test[-1:], forecast_prediction)
        #print(forecast_prediction)

        _predictedDifference = 0
        _predictedDifference = forecast_prediction - dfActual[0]
        # if (_predictedDifference < 0):
        #     test_data += 1

        #if (end != datetime.date.today()):

        #----------all this crap below should be inside if statement

        #dfActual = dfActual[:len(forecast_prediction)]
        #print (dfActual)

        _realDifference = 0
        _realDifference = dfActual[1] - dfActual[0]
        # if (_realDifference < 0):
        #     test_data2 += 1
        if (_realDifference > 0 and _predictedDifference > 0):
            WIN_COUNT += 1
        elif (_realDifference < 0 and _predictedDifference < 0):
            WIN_COUNT += 1
        else:
            LOSS_COUNT += 1
        #print ("Win percentage: " + str(round(WIN_COUNT / (WIN_COUNT + LOSS_COUNT), 2)) + '%')


        #----------all this crap above should be inside if statement

        j += num_days

    # print (j)
    # print (test_data)
    # print (test_data2)

    print ('\n')
    print ("Wins: " + str(WIN_COUNT))
    print ("Losses: " + str(LOSS_COUNT))
    WIN_PERCENTAGE = round((WIN_COUNT / (WIN_COUNT + LOSS_COUNT) * 100), 2)
    print ("Win Percentage: " + str(WIN_PERCENTAGE) + "%")
    print ("------------------------\n")

    newTest = ThirdStrategyTestObject(WIN_COUNT, LOSS_COUNT, WIN_PERCENTAGE)
    return newTest

if __name__ == '__main__':

    #end = datetime.date.today()
    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil']

    WINS = 0
    LOSS = 0
    PROFIT = 0

    print ("------------------------")

    end = datetime.date.today() + datetime.timedelta(0)
    #end = datetime.datetime(2019, 1, 15)
    #start = datetime.datetime(2018, 1, 1)
    start = end + datetime.timedelta(-600)

    # for x in range(0, len(stocks)):
    #     print (str(names[x]) + "\n")
    #     WIN_COUNT, LOSS_COUNT = findWinningPercentage(stocks[x], start, end)
    #     WINS += WIN_COUNT
    #     LOSS += LOSS_COUNT


    TOTAL = WINS + LOSS

    print ("------------------------")
    print ("Wins " + str(WINS))
    print ("Losses " + str(LOSS))
    print ("Total: " + str(TOTAL) + '\n')

    TOTAL = float(TOTAL)
    WIN_PERCENTAGE = (WINS / TOTAL)
    WIN_PERCENTAGE *= 100
    print ("Win Percentage: " + str(round(WIN_PERCENTAGE, 2)) + "%")

    #print ("Net Profit " + str(PROFIT) + '\n')

    print ("------------------------")
