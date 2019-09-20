from flask import Flask, render_template, request, jsonify, url_for
#from flask_cors import CORS
import json
import datetime

import pandas as pd
import pandas_datareader.data as web
import numpy as np

import sys
sys.path.insert(0, 'scripts/strategyTest')
from stockTestingData import getTestDataForSecondStrategy, getTestDataForThirdStrategy

import sys
sys.path.insert(0, 'scripts/strategyFind/')
from stockFindData import checkStrategies

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
#CORS(app)

def getListOfStockData(shouldShowStocks):

    print ("------------------------")

    # stocks = ['FXE', 'FXB', 'FXA', 'YCS']
    # names = ['EUR/USD', 'GBP/USD', 'AUD/USD', 'USD/JPY']

    # if (includeRussell == 'true'):
    #     stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO', 'GLD', 'SLV']
    #     names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil', 'Gold', 'Silver']
    # else: 
    #     stocks = ['^IXIC', '^GSPC', 'DIA', 'UNG', 'USO', 'GLD', 'SLV']
    #     names = ['Nasdaq', 'S&P 500', 'Dow', 'Natural Gas', 'Crude Oil', 'Gold', 'Silver']

    if (shouldShowStocks):
        stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA']
        names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow']
    else:
        stocks = ['UNG', 'USO', 'GLD', 'SLV']
        names = ['Natural Gas', 'Crude Oil', 'Gold', 'Silver']
    

    # print (str(end) + '\n')

    listOfStocks = []
    for x in range(0, len(stocks)):
        print ("--------------------------------- " + str(names[x]) + " ---------------------------------\n\n")

        stockObject = checkStrategies(stocks[x], names[x])
        listOfStocks.append(stockObject.__dict__)

        # print ('FIRST STRATEGY')
        # strategy_first.findWinningPercentage(stocks[x], start1, end)
        # print ('SECOND STRATEGY')
        # strategy_second.findWinningPercentage(stocks[x], start2, end)
        # print ('THIRD STRATEGY')
        # machine_learning_test.findWinningPercentage(stocks[x], start4, end)

    return listOfStocks


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/stocks", methods=['GET'])
def stocks():
    # includeRussell = request.args.get('includeRussell')
    # listOfStocks = getListOfStockData(includeRussell)
    shouldShowStocks = True
    open("triggers.txt", "w").close()
    listOfStocks = getListOfStockData(shouldShowStocks)
    return jsonify(listOfStocks)

@app.route("/commodities", methods=['GET'])
def commodities():
    # includeRussell = request.args.get('includeRussell')
    # listOfStocks = getListOfStockData(includeRussell)
    shouldShowStocks = False
    open("triggers.txt", "w").close()
    listOfStocks = getListOfStockData(shouldShowStocks)
    return jsonify(listOfStocks)

@app.route("/secondstrategytest/<stockSymbol>/<n>", methods=['GET'])
def testingSecondStrategy(stockSymbol, n):
    testData = getTestDataForSecondStrategy(stockSymbol, int(n))
    # ************** TODO put other stuff in model, not just wins losses and profit
    return jsonify(testData)

@app.route("/thirdstrategytest/<stockSymbol>/<n>", methods=['GET'])
def testingThirdStrategy(stockSymbol, n):
    testData = getTestDataForThirdStrategy(stockSymbol, int(n))

    return jsonify(testData)

if __name__ == "__main__":
    app.run(debug=True)
