import numpy as np
import datetime as dt
import pandas as pd
from util import get_data

def normalize_date(df):
    return df/df.ix[0,:]

def get_prices(dates, syms):
    prices_all = get_data(syms, dates)  # automatically adds SPY

    for sym in syms:
        prices_all[sym].fillna(method='ffill', inplace='True')
        prices_all[sym].fillna(method='backfill', inplace='True')

    # print("PRICES ALL BEGINNING AFTER BACKFILL")
    # print(prices_all)
    prices_all = prices_all.drop(['SPY'], axis=1)
    return prices_all


def simple_moving_avg(dates,df_prices):
    pass

def bollinger_band(df_prices):
    print("BOllinger setup")
    rolling_mean = pd.rolling_mean(df_prices, window=15)

    print(rolling_mean)
    rolling_std = pd.rolling_std(df_prices, window=30)
    bollinger_upper_band = rolling_mean + (2 * rolling_std)
    bollinger_lower_band = rolling_mean - (2 * rolling_std)

def oldSchoolCalculators(price, symbols, lookback=14):
    print("OLD SCHOOL")
    print(symbols)

    sma = price.copy()
    print(sma)
    for day in range(price.shape[0]):
        for sym in symbols:
            sma.ix[day,sym] = 0

    print("SET 0 ", sma)

    #loop over all days...
    for day in range(price.shape[0]):

        #this day is too early to calculate the full SMA
        if day < lookback:
            for sym in symbols:
                sma.ix[day,sym] = np.nan
            continue

        #loop over the lookback from this day and accumulate price.
        for sym in symbols:
            for prev_day in range(day - lookback+1, day+1):
                sma.ix[day,sym] = sma.ix[day,sym] + price.ix[prev_day, sym]

            #Calculate SMA for this day and symbol
            sma.ix[day,sym] = sma.ix[day,sym] / lookback

    print("CALCULATION OF SMA == ")
    print(sma)

if __name__=="__main__":
    print ("Remember Q from Star Trek? Well, this isn't him")
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    # symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    dates = pd.date_range(start_date, end_date)
    df_prices = get_prices(dates, symbols)
    # print(type(df_prices))
    # print(df_prices)
    oldSchoolCalculators(df_prices, symbols, lookback=14)
    print("BS")
    bollinger_band(df_prices)


