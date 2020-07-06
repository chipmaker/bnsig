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

import logging
class s500_barLB(object):

    def __init__(self):
        self.strategy_name = 'S500_barLB'
        logging.info("Initializing s500_barLB")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.nBuy = 4
        self.nSell = 5

    def run(self, df, row):
        logging.info("Initializing s500_barLB")
        df = self.barLB(df)
        return self.monitor(df)

    def barLB(self, df):
        nBuy = self.nBuy
        nSell = self.nSell

        n = nBuy
        buylist = []
        for i in range(n):
            buylist.append(False)

        for i in range(n, (len(df['Close']))):
            p = 0
            for j in range(n):
                j = i - j - 1
                # condC = (df['Close'].iloc[j] < df['Close'].iloc[i]) and (df['Open'].iloc[j] < df['Close'].iloc[i])
                # condO = (df['Open'].iloc[j] > df['Open'].iloc[i]) and (df['Close'].iloc[j] > df['Open'].iloc[i])
                condC = (df['Close'].iloc[j] < df['Close'].iloc[i])
                condO = (df['Open'].iloc[j] > df['Open'].iloc[i])
                if (condC & condO):
                    p = p + 1
                # print('i={}, j={}, condC={}, p = {}'.format(i, j, condC, p))
            if (p >= n):
                buylist.append(True)
            else:
                buylist.append(False)

        df['BUY'] = buylist

        u = nSell
        slist = []
        for i in range(u):
            slist.append(False)

        for i in range(u, (len(df['Close']))):
            p = 0
            for j in range(u):
                j = i - j - 1
                # condC = (df['Close'].iloc[j] < df['Close'].iloc[i]) and (df['Open'].iloc[j] < df['Close'].iloc[i])
                # condO = (df['Open'].iloc[j] > df['Open'].iloc[i]) and (df['Close'].iloc[j] > df['Open'].iloc[i])
                condC = (df['Close'].iloc[j] > df['Close'].iloc[i])
                condO = (df['Open'].iloc[j] < df['Open'].iloc[i])
                if (condC & condO):
                    p = p + 1
                # print('i={}, j={}, condC={}, p = {}'.format(i, j, condC, p))
            if (p >= u):
                slist.append(True)
            else:
                slist.append(False)

        df['SELL'] = slist

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
