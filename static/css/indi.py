import pandas as pd
import numpy as np
from scipy import stats
import datetime as dt
from util import get_data, plot_data

def normalize_date(df):
    return df/df.ix[0,:]

def get_prices(start_date, end_date, syms):
    print("we are in get prices function!!")
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    for sym in syms:
        prices_all[sym].fillna(method='ffill', inplace=True)
        prices_all[sym].fillna(method='backfill', inplace=True)

    # print("PRICES ALL BEGINNING AFTER BACKFILL")
    # print(prices_all)
    prices_all = prices_all.drop(['SPY'], axis=1)
    print(prices_all)
    return prices_all
pricetest = get_prices(start_date=dt.datetime(2008, 1, 1), end_date=dt.datetime(2009, 12, 31), syms=['AAPL'])

def get_price_to_sma(df, symbol, lookback):
    print("We are in get price to SMA!!")
    normalize_price = normalize_date(df)
    normalize_price.index.name = "Date"
    rolling_mean = normalize_price[symbol].rolling(window=lookback).mean()
    rolling_mean.fillna(method='ffill', inplace=True)
    rolling_mean.fillna(method='backfill', inplace=True)
    print("ROlling mean type == ", type(rolling_mean))
    sma = normalize_price / rolling_mean
    print("sma type == ", type(sma))
    print(sma)
    return sma
get_price_to_sma(pricetest, ['AAPL'], lookback =10)

def get_bollinger(df, symbol, lookback):
    print("You are in get Bollinger function!!")
    normalize_price = normalize_date(df)
    normalize_price.index.name = "Date"
    rolling_mean = normalize_price[symbol].rolling(window=lookback).mean()
    rolling_mean.fillna(method='ffill', inplace=True)
    rolling_mean.fillna(method='backfill', inplace=True)
    rolling_std = normalize_price[symbol].rolling(window=lookback, min_periods=lookback).std()
    upper_band = rolling_mean + (2 * rolling_std)
    lower_band = rolling_mean - (2 * rolling_std)
    bollinger_indicator = (normalize_price - lower_band)/(upper_band - lower_band)
    bollinger_indicator.fillna(method='ffill', inplace=True)
    bollinger_indicator.fillna(method='backfill', inplace=True)
    print("bollinger_indicator type == ", type(bollinger_indicator))
    print(bollinger_indicator)
    return bollinger_indicator

get_bollinger(pricetest, ['AAPL'], lookback=10)

def get_momentum(df, window=5):
    print("You are in get MOmemntum function!!")
    normalize_price = normalize_date(df)
    normalize_price.index.name = "Date"
    normalize_price[window:] = normalize_price[window:] / normalize_price.values[:-window]
    df[window:] = df[window:] / df.values[:-window] - 1
    print(df)
    return df

get_momentum(pricetest, window=10)

def n_day_return(df,symbol, nday):
    print("N DAY RETURN!")
    #daily_ret=((prices[symbol].shift(-1*Nday))/prices[symbol])-1
    nday_return = ((df[symbol].shift(-1 * nday)) / df[symbol]) - 1
    nday_return.fillna(method='ffill', inplace=True)
    print(nday_return)
    return nday_return
n_day_return(pricetest,['AAPL'], 3)

def get_momentum2(price, window=5):
    """Calculate momentum indicator:
    momentum[t] = (price[t]/price[t-window]) - 1
    Parameters:
    price: Price, typically adjusted close price, series of a symbol
    window: Number of days to look back

    Returns: Momentum, series of the same size as input data
    """
    #momentum = pd.Series(np.nan, index=price.index)
    momentum = price
    momentum.iloc[window:] = (price.iloc[window:] / price.values[:-window]) - 1
    print("window == ", window)
    print("REAL MOMENTUM")
    print(momentum)
    return momentum
get_momentum2(pricetest,window=10)


def compute_functions(df, symbol, lookback):
    normalize_price = normalize_date(df)
    normalize_price.index.name = "Date"

    rolling_mean = normalize_price[symbol].rolling(window=lookback).mean()
    print("ROlling mean type == ", type(rolling_mean))

    sma = (normalize_price[symbol] / rolling_mean) - 1
    print("sma type == ", type(sma))
    print(sma)

    rolling_std = normalize_price[symbol].rolling(window=lookback, min_periods=lookback).std()

    bollinger_indicator = (normalize_price[symbol] - rolling_mean) / rolling_std
    print("bollinger_indicator type == ", type(bollinger_indicator))

    print("SMA == ", sma)
    print("BBV == ", bollinger_indicator)
    print(type(sma))

    # daily_rets = (df / df.shift(1)) - 1
    # daily_rets = daily_rets[1:]
    # daily_rets.ix[0] = 0

    daily_rets = df.copy()
    daily_rets[1:] = (daily_rets[1:] / daily_rets[:-1].values) - 1
    daily_rets.ix[0] = 0
    print("Daily Returns == ")
    print(daily_rets)

    #RSI
    up_gain = daily_rets.copy()
    down_gain = daily_rets.copy()

    up_gain[up_gain < 0] = 0
    down_gain[down_gain > 0] = 0

    rolling_mean_up_gain = up_gain.rolling(lookback).mean()
    rolling_mean_down_gain = down_gain.rolling(lookback).mean()
    rsi = 100 - (100 / (1 + (rolling_mean_up_gain/rolling_mean_down_gain)))
    print("RSI == ")
    print(rsi)

    Z_score_daily_returns = stats.zscore(daily_rets)
    Z_score_daily_returns = pd.DataFrame(Z_score_daily_returns)
    print("Z_score_daily_returns == \n", type(Z_score_daily_returns), Z_score_daily_returns)

    indicators_df = pd.concat((bollinger_indicator, sma, rsi, daily_rets, Z_score_daily_returns[:,-1]), axis=1)
    indicators_df.columns = ["SMA", "BBL", "RSI", "Daily Returns", "Z Score"]
    #indicators_df = pd.DataFrame(indicators_series,columns = ['SMA','BOLL'])
    print(type(indicators_df))
    print(indicators_df)



def compute_prices(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), lookback=21, syms=['AAPL'],
                   gen_plot=False):
    # Read in adjusted closing prices for given symbols, date range
    print("We are in compute prices")
    dates = pd.date_range(sd, ed)

    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparision later
    print(prices)
    return prices, prices_all, prices_SPY
#compute_prices(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), lookback=21, syms=['AAPL'])

###calculate the stochastic indicator
def stochastic_indicator(price, syms=['AAPL'], lookback=21):
    ###
    stoch_max = price.rolling(window=lookback, min_periods=lookback).max()
    stoch_min = price.rolling(window=lookback, min_periods=lookback).min()

    stochk = 100 * (price - stoch_min) / (stoch_max - stoch_min)
    stochd = stochk.rolling(window=3, min_periods=3).mean()
    stochk = stochk.fillna(method='bfill')
    stochd = stochd.fillna(method='bfill')

    return stochk, stochd


# create sma array, zero it out
def sma_indicator(price, syms=['AAPL'], lookback=10):
    ###calculate SMA-21 for the entire date range for all symbols
    sma = price.rolling(window=lookback, min_periods=lookback).mean()
    sma = sma.fillna(method='bfill')

    return sma


###Turn SMA into Price/SMA ratio
def price_sma_indicator(price):
    print("PRICE_SMA_INDI")
    sma = sma_indicator(price)
    price_sma = price / sma
    print(price_sma)
    return price_sma
smaVal = price_sma_indicator(pricetest)

###calculate bollinger bands
def bollinger_band_indicator(price, syms=['AAPL'], lookback=21):
    sma = sma_indicator(price)
    # price = compute_prices()

    ###calculate bolling bands(21 day) over the entire period
    rolling_std = price.rolling(window=lookback, min_periods=lookback).std()
    # rolling_std = pd.rolling_std(price, window = lookback, min_periods = lookback)
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp = (price - bottom_band) / (top_band - bottom_band)
    bbp = bbp.fillna(method='bfill')
    print("BBP IND")
    print(bbp)

    return bbp, top_band, bottom_band
bollinger_band_indicator(pricetest, ['AAPL'], lookback=10)


###Calculate relative strength, then RSI
def rsi_indicator(price, syms=['AAPL'], lookback=21):
    # price, price_SPY = compute_prices()
    rsi = price.copy()

    daily_rets = price.copy()
    daily_rets.values[1:, :] = price.values[1:, :] - price.values[:-1, :]
    daily_rets.values[0, :] = np.nan

    ###final vectorize code
    up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
    down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()

    up_gain = price.copy()
    up_gain.ix[:, :] = 0
    up_gain.values[lookback:, :] = up_rets.values[lookback:, :] - up_rets.values[:-lookback, :]

    down_loss = price.copy()
    down_loss.ix[:, :] = 0
    down_loss.values[lookback:, :] = down_rets.values[lookback:, :] - down_rets.values[:-lookback, :]

    # Now we can  calculate the RS and RSI all at once
    rs = (up_gain / lookback) / (down_loss / lookback)
    rsi = 100 - (100 / (1 + rs))
    rsi.ix[:lookback, :] = np.nan

    # Inf results mean down_loss was 0. Those should be RSI 100
    rsi[rsi == np.inf] = 100
    rsi = rsi.fillna(method='bfill')

    return rsi


### Use the three indicators to make some kind of trading decision for each day
def build_orders(syms=['AAPL'], lookback=21):
    price, price_all, price_SPY = compute_prices()

    sma = price_sma_indicator(price_all)
    bbp, top_band, bottom_band = bollinger_band_indicator(price_all)
    rsi = rsi_indicator(price_all)

    # Orders starts as a NaN array of the same shape/index as price
    orders = price.copy()
    orders.ix[:, :] = np.NaN

    # Create a copy of RSI but with the SPY column copied to all columns
    spy_rsi = rsi.copy()
    spy_rsi.values[:, :] = spy_rsi.ix[:, ['SPY']]

    ###create a binary(0-1) array showing when price is above SMA-21
    sma_cross = pd.DataFrame(0, index=sma.index, columns=sma.columns)
    sma_cross[sma >= 1] = 1

    ###Turn that array into one that only shows the crossings (-1 == croos down, +1 == cross up)
    sma_cross[1:] = sma_cross.diff()
    sma_cross.ix[0] = 0

    ##now we can calculate the results of entire strategy at once
    # Apply our entry order conditions all at once. This represents our TARGET SHARES
    # at this moment in time, not an actual order
    orders[(sma < 0.95) & (bbp < 0) & (rsi < 30) & (spy_rsi > 30)] = 200
    orders[(sma > 1.05) & (bbp > 1) & (rsi > 70) & (spy_rsi < 70)] = -200

    # Apply our exit order conditions all at once. Again, this represents Target Shares.
    orders[(sma_cross != 0)] = 0

    # we now have -200, 0, or +200 target shares on all days that "we care about". (i.e. those
    # days when our strategy tells us something) all other days are NaN, meaning "hold whatever
    # you have".

    ###NaN meant "stand pat", so we should forward fill those
    # Forward fill NaNs with previous values, then fill remaining NaNs with 0
    orders.ffill(inplace=True)
    orders.fillna(0, inplace=True)

    # we now have a dataframe with our target shares on every day, including holding periods.
    ###But we wanted orders, not target holdings!
    # Now take the diff, which will give us an order to place only when the target shares changed.
    orders[1:] = orders.diff()
    orders.ix[0] = 0

    ###and now we have our orders array, just as we wanted it, with no iteration

    ###Dump the orders to stdout (redirect to a file if you wish)

    ###we can at least drop the SPY column
    # del orders['SPY']
    # syms.remove('SPY')

    ###And more importantly, drop all rows with no non-zero values(i.e. no orders)
    orders = orders.loc[(orders != 0).any(axis=1)]

    ###Now we have only the days that have orders. That's better, at least!
    order_list = []
    for day in orders.index:
        for sym in syms:
            if orders.ix[day, sym] > 0:
                order_list.append([day.date(), sym, 'BUY', 200])
            elif orders.ix[day, sym] < 0:
                order_list.append([day.date(), sym, 'SELL', 200])
    # Dump the orders to stdout. (redirect to a file if you wish)
    for order in order_list:
        print "   ".join(str(x) for x in order)


def standardization_indicator(df):
    df_stand = (df - df.mean()) / df.std()
    return df_stand


def normalization_indicator(df):
    df_norm = df / df.ix[0, :]
    return df_norm


def plot_indicator(df, title="Stock Prices"):
    # sma = sma_indicator()

    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    # plt.show()





def test_run():
    # df = price_sma_indicator()
    # df = bollinger_band_indicator()
    price, price_all, price_SPY = compute_prices()
    sma = sma_indicator(price)
    price_sma = price_sma_indicator(price)

    # price_st = standardization_indicator(price)
    # price_SPY_st = standardization_indicator(price_SPY)
    # sma_st = standardization_indicator(sma)
    # plot_price_sma_indicator(price_st,price_SPY_st,sma_st,'sma.png')

    # plot price/SMA figure
    price_n = normalization_indicator(price)
    price_sma_n = normalization_indicator(price_sma)
    sma_n = normalization_indicator(sma)
    #plot_price_sma_indicator(price_n, sma_n, price_sma, 'sma.png')

    # plot bolling_band figure
    bbp, upper_band, bottom_band = bollinger_band_indicator(price)
    bbp_n = normalization_indicator(bbp)
    upper_band_n = normalization_indicator(upper_band)
    bottom_band_n = normalization_indicator(bottom_band)
    #plot_bollinger_band_indicator(price, sma, upper_band, bottom_band, bbp, 'bbp.png')

    # plot relative strength index
    rsi = rsi_indicator(price)
    #plot_rsi_indicator(price_n, sma_n, rsi, 'rsi.png')

    ###standardization sma, bb, rsi
    rsi_n = normalization_indicator(rsi)
    sma_st = standardization_indicator(sma)
    price_sma_st = standardization_indicator(price_sma)
    bbp_st = standardization_indicator(bbp)
    rsi_st = standardization_indicator(rsi)
    # rsi_st = (rsi - rsi.mean())/rsi.std()
    # print rsi.mean()
    # print rsi.std()
    """
    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.plot(sma_st)
    axes.plot(price_sma_st)
    #print bbp
    axes.plot(bbp_st)
    axes.plot(rsi_st)
    #print rsi
    """
    stochk, stochd = stochastic_indicator(price)
    #plot_stoch_indicator(price_n, sma_n, stochk, 'stoch.png')
    # bbp = bollinger_band_indicator(price)
    # bbp = rsi_indicator(price)
    # df = df[21:,]

    # df = df.fillna(method='bfill')
    # df, df_SPY = compute_prices()
    # df = df/df.ix[0,:]
    # print df
    # price_SPY_st = standardization_indicator(price_SPY)
    # price_st = standardization_indicator(price)
    # sma_st = standardization_indicator(sma)
    # bbp_st = standardization_indicator(bbp)
    # price = price/price.ix[0,:]
    # df = df/df.ix[0,:]
    # plot_indicator_two_graph(price_st,price_SPY_st,bbp_st,'rsi.png')
    # plot_indicator(df)
    build_orders()


if __name__ == "__main__":
    # build_orders()
    # price,price_all,price_SPY = compute_prices()
    # build_orders()
    test_run()
    print 'good job'






