import requests
import pandas as pd
import arrow
import datetime
from ta import rsi, stoch_signal, cci, wr, macd_diff, uo, money_flow_index, ao

def calculateStrategy(stockSymbol):

    one_day = get_quote_data(stockSymbol, '1d', '15m')
    one_day.dropna(inplace=True) #removing NaN rows
    buyOrSellSignalFirstStrategy = calculate_fib_numbers(one_day, stockSymbol)

    return buyOrSellSignalFirstStrategy

def get_quote_data(symbol, data_range, data_interval):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    body = data['chart']['result'][0]
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('EST').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)

    return df.loc[:, ('open', 'high', 'low', 'close', 'volume')]

def calculate_fib_numbers(data, stock):

    #-------------------calculate how closely stock finished near its daily high or low--------
    FIB_HIGH = 0
    FIB_LOW = 10000000000
    for j in range(0, len(data)):
        if data['high'][j] > FIB_HIGH:
            FIB_HIGH = data['high'][j]
        if data['low'][j] < FIB_LOW:
            FIB_LOW = data['low'][j]

    DIFFERENCE_FROM_HIGH_TO_LOW = FIB_HIGH - FIB_LOW

    #calculate close and open for the day
    CLOSE = data['close'][-1:].values
    OPEN = data['open'][0]

    percent_change = 0
    percentChangeString = ""
    if ((CLOSE - OPEN) > 0):
        difference_from_top = FIB_HIGH - CLOSE[0]
        percent_change = round(((difference_from_top / DIFFERENCE_FROM_HIGH_TO_LOW) * 100),2)
        percentChangeString = (str(percent_change) + '% from the high of the day')
        print (str(percent_change) + '% from the high of the day')
    else:
        difference_from_bottom = CLOSE[0] - FIB_LOW
        percent_change = round(((difference_from_bottom / DIFFERENCE_FROM_HIGH_TO_LOW) * 100),2)
        percentChangeString = (str(percent_change) + '% from the low of the day')
        print (str(percent_change) + '% from the low of the day')

    #now see if strategy should go up or down from the last 5 days of data
    two_days = get_quote_data(stock, '5d', '15m')
    two_days.dropna(inplace=True) #removing NaN rows
    buyOrSellSignal = calculate_strength_of_stocks(two_days, percent_change)

    return percentChangeString, buyOrSellSignal

    #----------------------------------------------------------------------------------

def calculate_strength_of_stocks(data, percent_change):
    #---------------------------calculate moving averages and oscillators for this day -------------
    EMA_5 = data['close'].ewm(span=5, adjust=False).mean()
    SMA_5 = data['close'].rolling(window=5).mean()
    EMA_10 = data['close'].ewm(span=10, adjust=False).mean()
    SMA_10 = data['close'].rolling(window=10).mean()
    EMA_15 = data['close'].ewm(span=15, adjust=False).mean()
    SMA_15 = data['close'].rolling(window=15).mean()
    EMA_20 = data['close'].ewm(span=20, adjust=False).mean()
    SMA_20 = data['close'].rolling(window=20).mean()
    EMA_25 = data['close'].ewm(span=25, adjust=False).mean()
    SMA_25 = data['close'].rolling(window=25).mean()

    RSI = rsi(data['close'], n=14, fillna=False)
    STOK = stoch_signal(data['high'], data['low'], data['close'], n=14, d_n=3, fillna=False)
    # STOD = stoch(data['high'], data['low'], data['close'], n=14, fillna=False)
    CCI = cci(data['high'], data['low'], data['close'], n=20, c=0.015, fillna=False)
    WILLIAMS = wr(data['high'], data['low'], data['close'], lbp=14, fillna=False)
    MACDHIST = macd_diff(data['close'], n_fast=12, n_slow=26, n_sign=9, fillna=False)
    ULTIMATE = uo(data['high'], data['low'], data['close'], s=7, m=14, len=28, ws=4.0, wm=2.0, wl=1.0, fillna=False)
    MFI = money_flow_index(data['high'], data['low'], data['close'], data['volume'], n=14, fillna=False)
    AWESOME = ao(data['high'], data['low'], s=5, len=34, fillna=False)

    MOVING_AVERAGE_COUNT = 0
    OSCILLATOR_COUNT = 0

    #-----------------find moving averages-----------------
    #the -1 index is the last value in the dataset. the -2 index is the second to last value
    if (EMA_5[-1] > EMA_5[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_10[-1] > EMA_10[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_15[-1] > EMA_15[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_20[-1] > EMA_20[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (EMA_25[-1] > EMA_25[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1

    if (SMA_5[-1] > SMA_5[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_10[-1] > SMA_10[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_15[-1] > SMA_15[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_20[-1] > SMA_20[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1
    if (SMA_25[-1] > SMA_25[-2]):
        MOVING_AVERAGE_COUNT += 1
    else:
        MOVING_AVERAGE_COUNT -= 1

    #-----------------find moving averages-----------------

    #-----------------find oscillators---------------------
    if (RSI[-1] < 30):
        OSCILLATOR_COUNT += 1
    elif (RSI[-1] > 70):
        OSCILLATOR_COUNT -= 1
    if (STOK[-1] < 30):
        OSCILLATOR_COUNT += 1
    elif (STOK[-1] > 70):
        OSCILLATOR_COUNT -= 1
    if (CCI[-1] < -100 and CCI[-1] > CCI[-2]):
        OSCILLATOR_COUNT += 1
    elif (CCI[-1] > 100 and CCI[-1] < CCI[-2]):
        OSCILLATOR_COUNT -= 1
    if (AWESOME[-1] > AWESOME[-2]):
        OSCILLATOR_COUNT += 1
    elif (AWESOME[-1] < AWESOME[-2]):
        OSCILLATOR_COUNT -= 1
    if (MACDHIST[-1] > 0):
        OSCILLATOR_COUNT += 1
    elif (MACDHIST[-1] < 0):
        OSCILLATOR_COUNT -= 1
    if (WILLIAMS[-1] > -100 and WILLIAMS[-1] < -75 and WILLIAMS[-1] > WILLIAMS[-2]):
        OSCILLATOR_COUNT += 1
    elif (WILLIAMS[-1] < 0 and WILLIAMS[-1] > -25 and WILLIAMS[-1] < WILLIAMS[-2]):
        OSCILLATOR_COUNT -= 1
    if (ULTIMATE[-1] > 70):
        OSCILLATOR_COUNT += 1
    elif (ULTIMATE[-1] < 30):
        OSCILLATOR_COUNT -= 1
    #-----------------find oscillators---------------------

    #-----------------now need to calculate overall summary of stock-----------
    SECOND_STRATEGY_SUMMARY = 0
    MOVING_AVERAGE_SUMMARY = 0
    OSCILLATOR_SUMMARY = 0

    if (MOVING_AVERAGE_COUNT >= 4):
        MOVING_AVERAGE_SUMMARY = 1
    elif (MOVING_AVERAGE_COUNT <= -4):
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

    buyOrSellSignal = ""
    if (SECOND_STRATEGY_SUMMARY >= 0 and MFI[-1] < 80 and percent_change < 25):
        buyOrSellSignal =  ("Invest Up for first strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
        print ("Invest Up for first strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
    elif (SECOND_STRATEGY_SUMMARY < 0 and MFI[-1] > 20 and percent_change < 25):
        buyOrSellSignal = ("Invest Down for first strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
        print ("Invest Down for first strategy ---- " + "Moving Average Summary: "
        + str(MOVING_AVERAGE_SUMMARY)+ " - Oscillator Summary: " + str(OSCILLATOR_SUMMARY))
    else:
        buyOrSellSignal = ("Don't Invest for first strategy")
        print ("Don't Invest for first strategy")

    return buyOrSellSignal


if __name__ == '__main__':
    stocks = ['^IXIC', '^GSPC', '^RUT', 'DIA', 'UNG', 'USO']
    names = ['Nasdaq', 'S&P 500', 'Russell 2000', 'Dow', 'Natural Gas', 'Crude Oil']

    for x in range(0, len(stocks)):
        print ("------------------------")
        print (names[x], '\n')
        one_day = get_quote_data(stocks[x], '1d', '15m')
        one_day.dropna(inplace=True) #removing NaN rows
        calculate_fib_numbers(one_day, stocks[x])
        # plt.plot(df[['close']])
        # plt.show()
