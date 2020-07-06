#   ///////////////////////////////////////////////////////////////////////
#   Author: KAL GANDIKOTA
#  #
#   Kal’s bnsig is a Python program to interface with binanceus exchange
#   pull the data and analyze the data through Technical Analysis Algorithms
#   Copyright (C) NOV 2019 KAL GANDIKOTA
#  #
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  #
#   Please Kindly Donate for my Daily Expenses and Greater Works Than These
#  #
#   BTC Wallet: 1NeDC1GvpFa49DFLuT1v28ohFjqtoWXNQ5
#   ETH Wallet: 0x35e557F39A998e7d35dD27c6720C3553e1c65053
#   NEO Wallet: AUdiNJDW7boeUyYYNhX86p2T8eWwuELSGr
#   SteemID: chipmaker
#   https://www.twitter.com/chipmaker_tweet
#   https://steemit.com/@chipmaker
#   https://www.tradingview.com/u/KalGandikota/
#   ///////////////////////////////////////////////////////////////////////

import pandas as pd
import logging

class s300_STOCHRSI(object):

   def __init__(self):
        self.strategy_name = 'S300_STOCHRSI'
        logging.info("Initializing s300_STOCHRSI")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.srTOS = 20
        self.srTOB = 80

   def run(self, df, row):
        #logging.info("Running s300_STOCHRSI")
        df = self.STOCHRSI(df)
        return self.monitor(df)

   def STOCHRSI(self, df):
        srTOS = self.srTOS
        srTOB = self.srTOB
        smoothK = 3
        smoothD = 3

        df['RSI'] = self.RSI(df)
        df['STOCH'] = self.STOCH(df)

        df['k'] = self.SMA(df, smoothK, 'STOCH')
        df['d'] = self.SMA(df, smoothD, 'k')

        df['kSH'] = df['k'].shift(1)
        df['dSH'] = df['d'].shift(1)

        columns = ['k', 'd', 'kSH', 'dSH']

        def rsi_cond(row, columns):
            buy = (row['kSH'] <= row['dSH']) & (row['k'] > row['d']) & (row['d'] < srTOS)
            sell = (row['kSH'] >= row['dSH']) & (row['k'] < row['d']) & (row['d'] > srTOB)
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: rsi_cond(row, columns), axis=1))

        return df

   def monitor(self, df):
        if (self.udShow == -1):
            df['BUY'] = False
        elif (self.udShow == 1):
            df['SELL'] = False

        columns = ['normal_time', 'BUY', 'SELL']
        df2 = df[columns].tail(self.withinBars)
        dfBS = df2[df2['BUY'] | df2['SELL']]
        # print('dfBS={}'.format(dfBS))
        if (dfBS.size == 0):
            sellvar = df['SELL'].iloc[-1]
            buyvar = df['BUY'].iloc[-1]
            normaltimevar = df['normal_time'].iloc[-1]
        else:
            sellvar = dfBS['SELL'].iloc[-1]
            buyvar = dfBS['BUY'].iloc[-1]
            normaltimevar = dfBS['normal_time'].iloc[-1]

        # print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

   def SMA(self, ohlc: pd.DataFrame, period: int = 3, column: str = "Close") -> pd.Series:
       """
       Simple moving average - rolling mean in pandas lingo. Also known as 'MA'.
       The simple moving average (SMA) is the most basic of the moving averages used for trading.
       """

       return pd.Series(
           ohlc[column]
               .rolling(window=period)
               .mean(),
           name="{0} period SMA".format(period),
       )


   def RSI(self, ohlc: pd.DataFrame, period: int = 14):
        ## get the price diff
        delta = ohlc["Close"].diff()

        ## positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # EMAs of ups and downs
        _gain = up.ewm(span=period).mean()
        _loss = down.abs().ewm(span=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")


   def STOCH(self, ohlc: pd.DataFrame, period: int = 14):
        """Stochastic oscillator %K
         The stochastic oscillator is a momentum indicator comparing the closing price of a security
         to the range of its prices over a certain period of time.
         The sensitivity of the oscillator to market movements is reducible by adjusting that time
         period or by taking a moving average of the result.
        """

        highest_high = ohlc["RSI"].rolling(center=False, window=period).max()
        lowest_low = ohlc["RSI"].rolling(center=False, window=period).min()

        STOC = pd.Series(
            (ohlc["RSI"] - lowest_low) / (highest_high - lowest_low),
            name="{0} period STOCH %K".format(period),
        )
        return 100 * STOC
