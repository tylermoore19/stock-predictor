class SecondStrategyTestObject(object):
    winPercentageWhenTodayOpenPriceIsGreaterThanClose = 0.0
    winPercentageWhenTodayOpenPriceisLessThanClose = 0.0
    wins = 0
    losses = 0
    winPercentage = 0.0
    avgWin = 0.0
    avgLoss = 0.0
    avgPercentWin = 0.0
    avgPercentLoss = 0.0
    profit = 0.0

    
    def __init__(self, winPercentageWhenTodayOpenPriceIsGreaterThanClose, 
    winPercentageWhenTodayOpenPriceisLessThanClose, wins, losses, winPercentage, 
    avgWin, avgLoss, avgPercentWin, avgPercentLoss, profit):
        self.winPercentageWhenTodayOpenPriceIsGreaterThanClose = winPercentageWhenTodayOpenPriceIsGreaterThanClose
        self.winPercentageWhenTodayOpenPriceisLessThanClose = winPercentageWhenTodayOpenPriceisLessThanClose
        self.wins = wins 
        self.losses = losses
        self.winPercentage = winPercentage
        self.avgWin = avgWin
        self.avgLoss = avgLoss
        self.avgPercentWin = avgPercentWin
        self.avgPercentLoss = avgPercentLoss
        self.profit = profit

class ThirdStrategyTestObject(object):
    wins = 0
    losses = 0
    winPercentage = 0.0

    def __init__(self, wins, losses, winPercentage):
        self.wins = wins
        self.losses = losses
        self.winPercentage = winPercentage