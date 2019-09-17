class Stock(object):
    def __init__(self, stockName, basicHistoricalData, fibonacciNumbers, strategies, links):
        self.stockName = stockName
        self.basicHistoricalData = basicHistoricalData
        self.fibonacciNumbers = fibonacciNumbers
        self.strategies = strategies
        self.links = links

class Links(object):
    secondStrategyTest = ""
    thirdStrategyTest = ""

    def __init__(self, secondStrategyTestLink, thirdStrategyTestLink):
        self.secondStrategyTest = secondStrategyTestLink
        self.thirdStrategyTest = thirdStrategyTestLink

class BasicHistoricalData(object):
    openPrice = 0.0
    closePrice = 0.0
    prevClose = 0.0
    difference = 0.0
    percentChange = 0.0
    volume = 0.0
    tenDayAverageDifference = 0.0
    twentyDayAverageDifference = 0.0
    thirtyDayChange = 0.0

    # The class "constructor" - It's actually an initializer
    def __init__(self, openPrice, closePrice, prevClose, difference, percentChange, volume, tenDayAverageDifference,
        twentyDayAverageDifference, thirtyDayChange):
        self.openPrice = openPrice
        self.closePrice = closePrice
        self.prevClose = prevClose
        self.difference = difference
        self.percentChange = percentChange
        self.volume = volume
        self.tenDayAverageDifference = tenDayAverageDifference
        self.twentyDayAverageDifference = twentyDayAverageDifference
        self.thirtyDayChange = thirtyDayChange

class FibonacciNumbers(object):
    closePrice = 0.0
    fibHigh = 0.0
    fib78 = 0.0
    fib62 = 0.0
    fib50 = 0.0
    fib38 = 0.0
    fib24 = 0.0
    fibLow = 0.0

    def __init__(self, closePrice, fibHigh, fib78, fib62, fib50, fib38, fib24, fibLow):
        self.closePrice = closePrice
        self.fibHigh = fibHigh
        self.fib78 = fib78
        self.fib62 = fib62
        self.fib50 = fib50
        self.fib38 = fib38
        self.fib24 = fib24
        self.fibLow = fibLow

class Strategies(object):
    firstStrategyBuyOrSellSignal = ""
    firstStrategyWinPercentageForEntireYear = ""
    firstStrategyWinPercentageForFiftyDays = ""
    firstStrategyWinPercentageForFifteenDays = ""
    secondStrategyBuyOrSellSignal = ""
    thirdStrategyPredictedDifference = ""
    thirdStrategyPredictedPercentDifference = ""

    def __init__(self, firstStrategyBuyOrSellSignal, firstStrategyWinPercentageForEntireYear, firstStrategyWinPercentageForFiftyDays,
                    firstStrategyWinPercentageForFifteenDays, secondStrategyBuyOrSellSignal, thirdStrategyPredictedDifference,
                    thirdStrategyPredictedPercentDifference):
        self.firstStrategyBuyOrSellSignal = firstStrategyBuyOrSellSignal
        self.firstStrategyWinPercentageForEntireYear = firstStrategyWinPercentageForEntireYear
        self.firstStrategyWinPercentageForFifteenDays = firstStrategyWinPercentageForFifteenDays
        self.firstStrategyWinPercentageForFiftyDays = firstStrategyWinPercentageForFiftyDays
        self.secondStrategyBuyOrSellSignal = secondStrategyBuyOrSellSignal
        self.thirdStrategyPredictedDifference = thirdStrategyPredictedDifference
        self.thirdStrategyPredictedPercentDifference = thirdStrategyPredictedPercentDifference