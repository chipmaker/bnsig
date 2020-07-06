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

import talib
from Utils.mylogger import *

class s13_BB_RSI(object):

    def __init__(self):
        self.strategy_name = 'S13_BB_RSI'
        logger.info("Initializing s13_BB_RSI")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.rsiTol = 0

    def run(self, df, row):
        logger.info("Initializing s13_BB_RSI")
        df = self.BB_RSI(df)
        return self.scoreboard(df)

    def BB_RSI(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)
        rsiTol = self.rsiTol
        rsi30L = 30 + rsiTol
        rsi40L = 40 + rsiTol
        rsi50L = 50
        rsi60L = 60 - rsiTol
        rsi70L = 70 - rsiTol

        df['BBU_20'], df['BBM_20'], df['BBL_20'] = talib.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)

        df['RSI_14SH'] =df['RSI_14'].shift(1)
        df['BBL_20SH'] =df['BBL_20'].shift(1)
        df['BBU_20SH'] =df['BBU_20'].shift(1)
        df['CloseSH'] =df['Close'].shift(1)

        columns =['BBL_20', 'BBL_20SH', 'BBU_20', 'BBU_20SH', 'Close', 'CloseSH' 'RSI_14', 'RSI_14SH']

        def bb_rsi_cond(row, columns):
            bbBuy  = (row['CloseSH'] <= row['BBL_20SH']) & (row['Close'] > row['BBL_20'])
            bbSell = (row['CloseSH'] >= row['BBU_20SH']) & (row['Close'] < row['BBU_20'])

            rsiBuy = ((row['RSI_14SH'] <= rsi30L) & (row['RSI_14'] > rsi30L)) & (row['RSI_14SH'] < rsi30L)
            rsiSell = ((row['RSI_14SH'] >= rsi70L) & (row['RSI_14'] < rsi70L)) & (row['RSI_14SH'] > rsi70L)

            buy = (bbBuy & rsiBuy)
            sell = (bbSell & rsiSell)
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: bb_rsi_cond(row, columns), axis=1))
        return df

    def scoreboard(self, df):
        if(self.udShow==-1):
            df['BUY'] = False
        elif(self.udShow==1):
            df['SELL'] = False

        columns = ['normal_time', 'BUY', 'SELL']
        df2 = df[columns].tail(self.withinBars)
        dfBS = df2[df2['BUY'] | df2['SELL']]
        #print('dfBS={}'.format(dfBS))
        if(dfBS.size == 0):
            sellvar = df['SELL'].iloc[-1]
            buyvar =  df['BUY'].iloc[-1]
            normaltimevar = df['normal_time'].iloc[-1]
        else:
            sellvar = dfBS['SELL'].iloc[-1]
            buyvar =  dfBS['BUY'].iloc[-1]
            normaltimevar = dfBS['normal_time'].iloc[-1]

        #print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

