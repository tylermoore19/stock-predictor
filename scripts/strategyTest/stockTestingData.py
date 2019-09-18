import datetime
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import math

import strategy_second_test
import machine_learning_test

from models.testData import (
    SecondStrategyTestObject, ThirdStrategyTestObject
)

def getTestDataForSecondStrategy(stockSymbol, n):
    end = datetime.date.today() + datetime.timedelta(0)
    #going back 365 days because that means 252 trading days, which means 52 days of data
    #because this strategy needs to go back 200 days to be effective (252 - 200)
    start = end + datetime.timedelta(-n)
    
    newTestData = strategy_second_test.findWinningPercentage(stockSymbol, start, end)

    return (newTestData.__dict__)

def getTestDataForThirdStrategy(stockSymbol, n):
    end = datetime.date.today() + datetime.timedelta(0)
    #going back n days to see how often this strategy is correct
    start = end + datetime.timedelta(-n)

    newTestData = machine_learning_test.findWinningPercentage(stockSymbol, start, end)

    return (newTestData.__dict__)
