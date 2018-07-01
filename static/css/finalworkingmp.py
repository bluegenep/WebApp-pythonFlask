"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
from assess_portfolio import analysis

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    #read in Data from the csv file
    #df = pd.read_csv(orders_file, index_col='Date',parse_dates=True, na_values=['nan'])
    #df['Date'] = df.index
    #df(index='Date')
    #print(df)

    df_temp = pd.read_csv(orders_file, parse_dates=True)
    df_temp = df_temp.sort_values(by='Date')
    #print("DF TEMP == \n", df_temp)

    #get unique stocks from the orders file
    symbols = (df_temp['Symbol'].unique()).tolist()
    #print(type(symbols))
    #print("Symbols == ", symbols)

    #get Dates
    df_temp['Date']
    #print(df_temp['Date'])
    startDate = df_temp['Date'].iloc[0]
    endDate =  df_temp['Date'].iloc[-1]
    #print("Start Date == " , startDate, "End date == ", endDate)
    #print(pd.date_range(startDate, endDate))
    dates = pd.date_range(startDate, endDate)
    #getting dataframe with prices
    prices_df = get_data(symbols, dates)
    #Drop SPY
    prices_df = prices_df.drop(['SPY'], axis=1)

    #frontfill and backfill
    for sym in symbols:
        prices_df[sym].fillna(method='ffill', inplace=True)
        prices_df[sym].fillna(method='backfill', inplace=True)

    prices_df['CASH'] = 0
    #prices_df = prices_df.rename(columns={prices_df.columns[0]: "Date"})
    #print("INDEX VALUES == ", prices_df.index.get_values())
    prices_df.index.name = "Date"
    print("Prices DF")
    print(prices_df)

    #create a copy of DF for trading DF and holding DF
    df_copy = prices_df.copy(deep=True)
    for sym in symbols:
        df_copy[sym] =0
    #print("COPY  Dataframe")
    #print(df_copy)

    #create a trades_df
    trades_df = df_copy
    trades_df.index.name = "Date"
    #print("BEFORE Trades Dataframe")
    #print(trades_df)

    orders_df = df_temp
    orders_df.index.name = "Date"
    for index, row in orders_df.iterrows():
        #print(trades_df.index, row)
        #print("Index == ", index)
        #print(row['Date'])
        traded_share = row['Symbol']
        #print("Traded share for this day is == ", traded_share)
        #print(trades_df.loc[row['Date'], "CASH"])
        #if row['Date'] ==
        if row['Order'] == "BUY" :
            trades_df.loc[row['Date'], row['Symbol']] += row['Shares']
            trades_df.loc[row['Date'], "CASH"] = trades_df.loc[row['Date'], "CASH"] + (row['Shares'] * prices_df.loc[row['Date'], traded_share] * (1+ impact) * (-1)) - ( commission)
        elif row['Order'] == "SELL" :
            trades_df.loc[row['Date'], row['Symbol']] += (row['Shares'] * (-1))
            trades_df.loc[row['Date'], "CASH"] = trades_df.loc[row['Date'], "CASH"] + (row['Shares'] * prices_df.loc[row['Date'], traded_share] * (1-impact)) - ( commission )

        #print(orders_df.loc[index, row['Symbol']])
        # print("ROW == ", row['Date'])
        # if row['Date'] in trades_df.index:
        #     print("YES")
        #     #trades_df.set_value(index, 'x', 10)
        #     trades_df.loc[row['Symbol']] = row['Shares']
        # else:
        #     print("NO")

    print(" AFTER Trades Dataframe")
    print(trades_df)

    #holding dataframe
    holdings_df = trades_df

    #holdings_df[0] = 100
    print("FIRST ROW == ", holdings_df.iloc[0, -1])
    holdings_df.iloc[0, -1] = holdings_df.iloc[0, -1] + start_val
    holdings_df = holdings_df.cumsum()
    print(" Holdings Dataframe")
    print(holdings_df)

    new_prices_df = prices_df
    new_prices_df['CASH'] = 1
    print(new_prices_df.head())
    print(holdings_df.head())
    values_df = new_prices_df * holdings_df
    print(values_df.head())

    #port Values
    port_vals_df = values_df
    port_vals_df['VALUE'] = port_vals_df.sum(axis=1)
    print(port_vals_df)

    portvals = pd.DataFrame(port_vals_df['VALUE'])
    print("FINAL PORTFOLIO \n")
    print(portvals)
    print(type(portvals))
    print(portvals.iloc[3])
    #holdings_df['VALUE'] = 0
    # for i in range(1,len(holdings_df)):
    #     holdings_df.iloc[i, -1] = holdings_df.iloc[i-1, -1] + holdings_df.iloc[i, -2]
    #
    #
    # print(" Holdings Dataframe")
    # print(holdings_df)



    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    # start_date = dt.datetime(2008,1,1)
    # end_date = dt.datetime(2008,6,1)
    # portvals = get_data(['IBM'], pd.date_range(start_date, end_date))
    # portvals = portvals[['IBM']]  # remove SPY
    # rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())
    #
    # return rv
    return portvals

def author():
    return 'pbhatta3' #Change this to your user ID

def get_portfolio_stats(port_val):
    print("PORTFOLIO STATUS")
    print("PORTFOLIO Value DF \n ==", port_val)
    daily_rets = (port_val / port_val.shift(1)) - 1
    daily_rets = daily_rets[1:]
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
    cum_return = float((port_val[-1] - port_val[0]) / port_val[0])
    #cum_return = (port_val.ix[-1]/port_val.ix[0]) - 1
    return avg_daily_ret, std_daily_ret,  sharpe_ratio, cum_return

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    #of = "./orders/orders2.csv"
    #of = "/Users/sadichha/GTechClasses/ML4TSummer/ML4T_2018SpringP0/marketsim/orders/orders-short.csv"

    of = "/Users/sadichha/GTechClasses/ML4TSummer/ML4T_2018SpringP0/marketsim/orders/orders2.csv"

    #of = "/Users/sadichha/GTechClasses/ML4TSummer/ML4T_2018SpringP0/marketsim/orders/orders-02.csv"

    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.

    # start_date = dt.datetime(2008,1,1)
    # end_date = dt.datetime(2008,6,1)

    print("PORTVALS TYPE == ", type(portvals))
    avg_daily_ret, std_daily_ret, sharpe_ratio, cum_ret = get_portfolio_stats(portvals)

    # get data for SPY
    #portvals = pd.DataFrame(portvals)
    df_temp = pd.read_csv(of, parse_dates=True)
    df_temp = df_temp.sort_values(by='Date')
    # print("DF TEMP == \n", df_temp)

    # get unique stocks from the orders file
    symbols = (df_temp['Symbol'].unique()).tolist()
    print(type(portvals))
    start_date = portvals.index[0]
    end_date = portvals.index[-1]
    print("Start Date == " , start_date, "End date == ", end_date)
    # print(pd.date_range(startDate, endDate))
    dates = pd.date_range(start_date, end_date)
    symbols  = ['$SPX']
    prices_SPX = get_data(symbols, dates, addSPY=True)
    for sym in symbols:
        prices_SPX[sym].fillna(method='ffill', inplace='True')
        prices_SPX[sym].fillna(method='backfill', inplace='True')
    prices_SPX = prices_SPX.drop(['SPY'], axis=1)

    #print(type(prices_SPY.iloc[0,:]), "PRICES SPY == /n", prices_SPY.iloc[:,:])
    prices_SPX = pd.Series(prices_SPX['$SPX'])
    print("Portfolio type == " , type(prices_SPX))
    avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY, cum_ret_SPY = get_portfolio_stats(prices_SPX)



    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    #cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print("Date Range: {} to {}".format(start_date, end_date))
    print()
    print("Sharpe Ratio of Fund: {}".format(sharpe_ratio))
    print ("Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY))
    print()
    print ("Cumulative Return of Fund: {}".format(cum_ret))
    print ("Cumulative Return of SPY : {}".format(cum_ret_SPY))
    print
    print ("Standard Deviation of Fund: {}".format(std_daily_ret))
    print ("Standard Deviation of SPY : {}".format(std_daily_ret_SPY))
    print
    print ("Average Daily Return of Fund: {}".format(avg_daily_ret))
    print ("Average Daily Return of SPY : {}".format(avg_daily_ret_SPY))
    print
    print ("Final Portfolio Value: {}".format(portvals[-1]))

if __name__ == "__main__":
    test_code()
