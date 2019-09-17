import math
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import time
import datetime
import pandas_datareader.data as web

from datetime import date, datetime, time, timedelta
from matplotlib import pyplot as plt
from pylab import rcParams
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from tqdm import tqdm_notebook

test_size = 0.2                 # proportion of dataset to be used as test set
cv_size = 0.2                   # proportion of dataset to be used as cross-validation set
Nmax = 2                       # for feature at day t, we use lags from t-1, t-2, ..., t-N as features
                                # Nmax is the maximum N we are going to test
fontsize = 14
ticklabelsize = 14


def get_preds_mov_avg(df, target_col, N, pred_min, offset):
    """
    Given a dataframe, get prediction at timestep t using values from t-1, t-2, ..., t-N.
    Using simple moving average.
    Inputs
        df         : dataframe with the values you want to predict. Can be of any length.
        target_col : name of the column you want to predict e.g. 'adj_close'
        N          : get prediction at timestep t using values from t-1, t-2, ..., t-N
        pred_min   : all predictions should be >= pred_min
        offset     : for df we only do predictions for df[offset:]. e.g. offset can be size of training set
    Outputs
        pred_list  : list. The predictions for target_col. np.array of length len(df)-offset.
    """
    pred_list = df[target_col].rolling(window = N, min_periods=1).mean() # len(pred_list) = len(df)
    
    # Add one timestep to the predictions
    pred_list = np.concatenate((np.array([np.nan]), np.array(pred_list[:-1])))
    
    # If the values are < pred_min, set it to be pred_min
    pred_list = np.array(pred_list)
    pred_list[pred_list < pred_min] = pred_min
    
    return pred_list[offset:]

def get_mape(y_true, y_pred): 
    """
    Compute mean absolute percentage error (MAPE)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# end = datetime.today() + timedelta(0)
# start = end + timedelta(-730)
end = datetime(2019, 8, 20)
start = datetime(2017, 8, 20)
df = web.DataReader('^IXIC', 'yahoo', start, end)
df = df.reset_index()

# Convert Date column to datetime
df.loc[:, 'Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d')

# Change all column headings to be lower case, and remove spacing
df.columns = [str(x).lower().replace(' ', '_') for x in df.columns]

# # Get month of each sample
# df['month'] = df['date'].dt.month

# Sort by datetime
df.sort_values(by='date', inplace=True, ascending=True)

# Get sizes of each of the datasets
num_cv = int(cv_size*len(df))
num_test = int(test_size*len(df))
num_train = len(df) - num_cv - num_test
print("num_train = " + str(num_train))
print("num_cv = " + str(num_cv))
print("num_test = " + str(num_test))

# Split into train, cv, and test
train = df[:num_train]
cv = df[num_train:num_train+num_cv]
train_cv = df[:num_train+num_cv]
test = df[num_train+num_cv:]
print("train.shape = " + str(train.shape))
print("cv.shape = " + str(cv.shape))
print("train_cv.shape = " + str(train_cv.shape))
print("test.shape = " + str(test.shape))


# Plot adjusted close over time
# rcParams['figure.figsize'] = 10, 8 # width 10, height 8
# matplotlib.rcParams.update({'font.size': 14})

# ax = train.plot(x='date', y='adj_close', style='b-', grid=True)
# ax = cv.plot(x='date', y='adj_close', style='y-', grid=True, ax=ax)
# ax = test.plot(x='date', y='adj_close', style='g-', grid=True, ax=ax)
# ax.legend(['train', 'validation', 'test'])
# ax.set_xlabel("date")
# ax.set_ylabel("USD")

# plt.show()

RMSE = []
mape = []
for N in range(1, Nmax+1): # N is no. of samples to use to predict the next value
    est_list = get_preds_mov_avg(train_cv, 'adj_close', N, 0, num_train)
    
    cv['est' + '_N' + str(N)] = est_list
    RMSE.append(math.sqrt(mean_squared_error(est_list, cv['adj_close'])))
    mape.append(get_mape(cv['adj_close'], est_list))
print('RMSE = ' + str(RMSE))
print('MAPE = ' + str(mape))


# Set optimum N
N_opt = 1


# Plot adjusted close over time
# rcParams['figure.figsize'] = 10, 8 # width 10, height 8
# matplotlib.rcParams.update({'font.size': 14})

# ax = train.plot(x='date', y='adj_close', style='b-', grid=True)
# ax = cv.plot(x='date', y='adj_close', style='y-', grid=True, ax=ax)
# ax = test.plot(x='date', y='adj_close', style='g-', grid=True, ax=ax)
# ax = cv.plot(x='date', y='est_N1', style='r-', grid=True, ax=ax)
# ax = cv.plot(x='date', y='est_N2', style='m-', grid=True, ax=ax)
# ax.legend(['train', 'validation', 'test', 'predictions with N=1', 'predictions with N=2'])
# ax.set_xlabel("date")
# ax.set_ylabel("USD")

# plt.show()

est_list = get_preds_mov_avg(df, 'adj_close', N_opt, 0, num_train+num_cv)
test['est' + '_N' + str(N_opt)] = est_list
print("RMSE = %0.3f" % math.sqrt(mean_squared_error(est_list, test['adj_close'])))
print("MAPE = %0.3f%%" % get_mape(test['adj_close'], est_list))

# Plot adjusted close over time
# rcParams['figure.figsize'] = 10, 8 # width 10, height 8

# ax = train.plot(x='date', y='adj_close', style='b-', grid=True)
# ax = cv.plot(x='date', y='adj_close', style='y-', grid=True, ax=ax)
# ax = test.plot(x='date', y='adj_close', style='g-', grid=True, ax=ax)
# ax = test.plot(x='date', y='est_N1', style='r-', grid=True, ax=ax)
# ax.legend(['train', 'validation', 'test', 'predictions with N_opt=1'])
# ax.set_xlabel("date")
# ax.set_ylabel("USD")
# matplotlib.rcParams.update({'font.size': 14})

# Plot adjusted close over time
# rcParams['figure.figsize'] = 10, 8 # width 10, height 8

# ax = train.plot(x='date', y='adj_close', style='bx-', grid=True)
# ax = cv.plot(x='date', y='adj_close', style='yx-', grid=True, ax=ax)
# ax = test.plot(x='date', y='adj_close', style='gx-', grid=True, ax=ax)
# ax = test.plot(x='date', y='est_N1', style='rx-', grid=True, ax=ax)
# ax.legend(['train', 'validation', 'test', 'predictions with N_opt=1'], loc='upper left')
# ax.set_xlabel("date")
# ax.set_ylabel("USD")
# ax.set_xlim([date(2019, 4, 1), date(2019, 8, 20)])
# ax.set_ylim([7500, 8500])
# ax.set_title('Zoom in to test set')

# Plot adjusted close over time, only for test set
rcParams['figure.figsize'] = 10, 8 # width 10, height 8
matplotlib.rcParams.update({'font.size': 14})

ax = test.plot(x='date', y='adj_close', style='gx-', grid=True)
ax = test.plot(x='date', y='est_N1', style='rx-', grid=True, ax=ax)
ax.legend(['test', 'predictions using last value'], loc='upper left')
ax.set_xlabel("date")
ax.set_ylabel("USD")
ax.set_xlim([date(2019, 4, 1), date(2019, 8, 20)])
ax.set_ylim([7500, 8500])

plt.show()
