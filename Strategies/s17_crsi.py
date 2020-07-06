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

class s17_CRSI(object):

    def __init__(self):
        self.strategy_name = 'S17_CRSI'
        logger.info("Initializing s17_CRSI")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0

    def run(self, df, row):
        logger.info("Initializing s17_CRSI")
        df = self.CRSI(df)
        return self.monitor(df)

    def CRSI(self, df):
        Rank_Lookback = 100

        df['CloseSH'] = df['Close'].shift(1)

        df['RSI_3'] = talib.RSI(df['Close'], timeperiod=3)

        # Component 3: The percent rank of the current return
        columns = ['Close', 'CloseSH']

        def roc1(row, columns):
            roc1 = ((row['Close'] / row['CloseSH']) - 1) * 100
            return roc1

        df['ROC1'] = df.apply(lambda row: roc1(row, columns), axis=1)

        rank = []
        for j in range((len(df['ROC1']))):
            pr = 0
            for i in range(Rank_Lookback):
                i = i + 1
                pr = pr + (df['ROC1'].iloc[-i + j] < df['ROC1'].iloc[j])
            rank.append(pr)

        df['pctRank'] = rank

        ####Componen2
        columns = ['Close', 'CloseSH']

        def ud_cond(row, columns):
            ud = 1 if (row['Close'] > row['CloseSH']) else 0
            dd = -1 if (row['Close'] < row['CloseSH']) else 0
            return ud, dd

        df['upDay'], df['downDay'] = zip(*df.apply(lambda row: ud_cond(row, columns), axis=1))

        # def upStreak = if upDay != 0 then upStreak[1] + upDay else 0;
        i = 0
        def upCons(x):
            global i
            i = i + 1 if x != 0 else 0
            return i

        df['upStreak'] = df['upDay'].map(lambda x: upCons(x))

        # def downStreak = if downDay != 0 then downStreak[1] + downDay else 0;
        j = 0
        def dnCons(x):
            global j
            j = j - 1 if x != 0 else 0
            return j

        df['downStreak'] = df['downDay'].map(lambda x: dnCons(x))

        # def streak = upStreak + downStreak;
        df['streak'] = df['upStreak'] + df['downStreak']

        df['streakRSI'] = talib.RSI(df['streak'], timeperiod=2)

        df['CRSI'] = (df['pctRank'] + df['streakRSI'] + df['RSI_3']) / 3

        df['SELL'] = df['CRSI'] > 95
        df['BUY'] = df['CRSI'] < 5
        return df

    def monitor(self, df):
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

#df2 = df.tail(self.withinBars)
#df2['BUY'].any()
#df2['SELL'].any()
#return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
#return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]
