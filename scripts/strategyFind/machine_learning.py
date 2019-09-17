import pandas as pd
import numpy as np
import datetime

from pandas_datareader import data as web
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.metrics import accuracy_score

# To plot
import seaborn

def machineLearningTest(stock, start, end):

    df = web.DataReader(stock, 'yahoo', start, end)

    if (end != datetime.date.today()):
        print (df[-2:], '\n')
    else:
        print (df[-1:], '\n')

    df = df[['Adj Close']]
    dfActual = np.array(df['Adj Close'])
    #print (dfActual)
    #print (dfActual)
    #print(df.tail())

    forecast_out = int(1) # predicting n days into future

    X = []
    y = []

    if (end != datetime.date.today()):
        #-------------------------------TESTING PURPOSES----------------------------

        df['Prediction'] = df[['Adj Close']].shift(-forecast_out) #  label column with data shifted n units up

        X = np.array(df[['Adj Close']])
        # X = np.array(df.drop(['Prediction'], 1))
        X = preprocessing.scale(X)

        #------------------------------------
        #example, if we are trying to predict if the 3rd will go up or down, need to get every
        #data in the set except for the 3rd and 4th so we can train the data, and then predict if the 3rd
        #will go up or down. we will use the 4th datapoint to see if we were correct
        X_forecast = X[(-forecast_out - 1):]

        #just for testing purposes
        # X_forecast = X[(-forecast_out):]
        #------------------------------------

        X = X[:(-forecast_out - 1)] # remove last n days from X since we will use these values to predict n days into future
        #print (X)

        y = np.array(df['Prediction'])
        y = y[:(-forecast_out - 1)] #same for y

        #also get last two data points for adj closed to see if our prediction was right
        dfActual = dfActual[(-forecast_out - 1):]
        #print (dfActual)

    else:
        #----------------------PREDICT IF TODAYS PRICE WILL GO UP OR DOWN TOMORROW----------------

        df['Prediction'] = df[['Adj Close']].shift(-forecast_out) #  label column with data shifted n units up

        X = np.array(df[['Adj Close']])
        # X = np.array(df.drop(['Prediction'], 1))
        X = preprocessing.scale(X)

        #------------------------------------
        X_forecast = X[(-forecast_out):]
        #this is to predict if today's price will go up or down tomorrow

        #just for testing purposes
        # X_forecast = X[(-forecast_out):]
        #------------------------------------

        #keep X the same
        X = X[:(-forecast_out)]
        #print (X)

        y = np.array(df['Prediction'])

        #also keep y the same
        y = y[:(-forecast_out)]

        #also get last two data points for adj closed to see if our prediction was right
        dfActual = dfActual[(-forecast_out):]
        #print (dfActual)

    forecast_prediction = []
    confidence = []
    #do the machine learning algo 10 times and then average the results to get a better understanding
    #of what the stock is going to do
    for i in range(0, 10):

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)
        # X_train, X_test, y_train, y_test = train_test_split(X, y)

        # if (i == 0):
        #     print (len(X_train))
        #     print (len(X_test))
        #     print (len(y_train))
        #     print (len(y_test))

        # Training
        clf = LinearRegression()
        clf.fit(X_train,y_train)

        # Testing
        confidence.append(clf.score(X_test, y_test))

        forecast = clf.predict(X_forecast)
        forecast_prediction.append(forecast[0])

    confidence = np.mean(confidence)
    print("confidence: " + str(round(confidence * 100,2)) + '%')

    forecast_prediction = np.mean(forecast_prediction)
    #print (forecast_prediction)
    #forecast_prediction = np.append(y_test[-1:], forecast_prediction)
    #print(forecast_prediction)


    _predictedDifference = 0
    _predictedDifference = forecast_prediction - dfActual[0]

    if (end != datetime.date.today()):

        _realDifference = 0
        # _realDifference = dfActual[1] - dfActual[0]
        _realDifference = dfActual[1] - dfActual[0]
        print ("Real Difference: ", str(_realDifference))
        percent_change = ((dfActual[1] - dfActual[0]) / dfActual[0]) * 100
        print ("Real Percent Difference: " + str(round(percent_change, 2)) + "%")
        # for k in range(1, len(forecast_prediction)):
        #     if (forecast_prediction[k] > forecast_prediction[k - 1] and dfActual[k] > dfActual[k - 1]):
        #         success_up += 1
        #     elif (forecast_prediction[k] < forecast_prediction[k - 1] and dfActual[k] < dfActual[k - 1]):
        #         success_down += 1
        #print (success_up)
        #print (success_down)

    print ("Predicted Difference: ", str(_predictedDifference))
    #print ("Predicted Difference2: ", str(_predictedDifference2))
    #percent_change = ((forecast_prediction[1] - forecast_prediction[0]) / forecast_prediction[0]) * 100
    percent_change = ((forecast_prediction - dfActual[0]) / dfActual[0]) * 100
    percent_change = str(round(percent_change, 2)) + "%"
    print ("Predicted Percent Difference: " + percent_change)

    print ("------------------------\n")

    forecast_prediction = [dfActual[0], forecast_prediction]

    #--------return predicted difference and predicte percent difference -------
    return _predictedDifference, percent_change

if __name__ == '__main__':

    #end = datetime.datetime(2019, 6, 26)
    end = datetime.date.today() + datetime.timedelta(-20)

    #200 / 252 = 0.79. 0.79 * 365 = 7289 real days. This strategy needs to go back 200 legit trading days
    # (or 289 real days) to back test and come up with buy or sell signal
    start = end + datetime.timedelta(-289)
    #start = datetime.datetime(2019, 4, 1)

    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil']

    # if (end != datetime.date.today()):
    #     print ('\nTesting for day: ' + str(end + datetime.timedelta(-1)) + '\n')
    # else:
    print ('\nTesting for day: ' + str(end + datetime.timedelta(0)) + '\n')

    for x in range(0, len(stocks)):
        print (names[x], '\n')
        machineLearningTest(stocks[x], start, end)
