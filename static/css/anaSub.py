"""Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt




# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=True):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    print("SYMBOLS TYPE == ", type(syms))
    prices_all = get_data(syms, dates)  # automatically adds SPY
    #prices_all = prices_all.dropna() #dropping NA values
    print(prices_all)
    #prices_all = prices_all.fillna(method='ffill', inplace='TRUE')
    #start frontfill and backfill

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values

    # Get portfolio statistics (note: std_daily_ret = volatility)
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    ## My coding begins
    #Read in adjusted closing prices for the equities.

    for sym in syms:
        prices_all[sym].fillna(method='ffill', inplace='True')
        prices_all[sym].fillna(method='backfill', inplace='True')

    print("PRICES ALL BEGINNING AFTER BACKFILL")
    print(prices_all)

    adj_close_data = prices_all
    print(prices_all)

    #Normalize the prices according to the first day. The first row for each stock should have a value of 1.0 at this point.
    norm_prices = normalize_date(prices_all)
    print("normalized prices")
    print(norm_prices)

    #Multiply each column by the allocation to the corresponding equity.
    norm_prices_alloc = norm_prices[syms] * allocs
    print("normalized prices allocation")
    print(norm_prices_alloc)

    #Multiply these normalized allocations by starting value of overall portfolio, to get position values.
    norm_prices_alloc_port_val = norm_prices_alloc * sv
    print(norm_prices_alloc_port_val)

    #Sum each row (i.e. all position values for each day). That is your daily portfolio value.
    daily_port_val = norm_prices_alloc_port_val.sum(axis=1)
    #daily_port_val = '{:f}'.format(daily_port_val)
    print("Daily Portfolio Value == \n",daily_port_val )


    #Compute statistics from the total portfolio value.
    total_port_val = daily_port_val.sum(axis=0)
    print("TOTAL PORTFOLIO VALUE == " , total_port_val)

    #daily return
    # daily_port_return = (daily_port_val / daily_port_val.shift(1)) - 1
    #     # daily_port_return.ix[0, :] = 0
    dfCopy = daily_port_val.copy()
    print("daily_port_val[1:] ==", daily_port_val[1:])
    print("daily_port_val[:-1].values ==", daily_port_val[:-1].values)
    dfCopy[1:] = (daily_port_val[1:] / daily_port_val[:-1].values) - 1
    dfCopy.ix[0] = 0
    print("Daily portfolio return \n" , dfCopy)
    print("Average Daily portfolio return \n", dfCopy.mean())
    avg_daily_return = dfCopy[1:].mean()


    print("Standard deviation of daily portfolio return == " , dfCopy.std() )
    std_daily_return = dfCopy[1:].std()
    sharpe_ratio = (sf)**(1.0/2.0) *((avg_daily_return -rfr)/std_daily_return)
    print("Sharpe ratio ==", sharpe_ratio)

    #cumulative return
    # print("total_port_val[-1]", float(daily_port_val[-1]))
    # print("total_port_val[0]", float(daily_port_val[0]))
    cum_return = float((daily_port_val[-1] - daily_port_val[0])/daily_port_val[0])
    print("CUM RETURN == ", cum_return)
    # Compare daily portfolio value with SPY using a normalized plot
    norm_portfolio_value = normalize_date(daily_port_val)
    SPY_portfolio_value =  norm_prices['SPY'] * 1 * sv
    norm_SPY_portfolio_value = normalize_date(SPY_portfolio_value)
    print("NORM PORTFOLIO VALUE---")
    print(norm_portfolio_value)
    print("NORM SPY PORTFOLIO VALUE---")
    print(norm_SPY_portfolio_value)

    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([norm_portfolio_value, norm_SPY_portfolio_value], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.plot()
        plt.show()
        #pass

    # Add code here to properly compute end value
    ev = total_port_val
    cr = cum_return
    adr = avg_daily_return
    sddr = std_daily_return
    sr = sharpe_ratio


    return cr, adr, sddr, sr, ev

def normalize_date(df):
    return df/df.ix[0,:]

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    # start_date = dt.datetime(2009,1,1)
    # end_date = dt.datetime(2009,1,15)
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2010, 12, 31)
    #symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    #allocations = [0.2, 0.3, 0.4, 0.1]
    allocations = [0.0, 0.0, 0.0, 1.0]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print ("Start Date:", start_date)
    print ("End Date:", end_date)
    print ("Symbols:", symbols)
    print ("Allocations:", allocations)
    print ("Sharpe Ratio:", sr)
    print ("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)

if __name__ == "__main__":
    test_code()


