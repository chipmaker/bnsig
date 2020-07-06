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
import logging

class sEMA(object):

    def __init__(self):
        self.strategy_name = 'sEMA'
        logging.info("Initializing sEMA")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0

    def run(self, df, row):
        logging.info("Initializing sEMA")
        df = self.sEMA(df)
        return self.scoreboard(df, row)

    def sEMA(self, df):
        def crossover(myline, mylineSH, src, srcSH):
            return (srcSH <= mylineSH) & (src > myline)

        def crossunder(myline, mylineSH, src, srcSH):
            return (srcSH >= mylineSH) & (src < myline)

        df['EMA50'] = talib.EMA(df['Close'], timeperiod=50)
        df['EMA50SH'] = df['EMA50'].shift(1)

        df['EMA100'] = talib.EMA(df['Close'], timeperiod=100)
        df['EMA100SH'] = df['EMA100'].shift(1)

        df['EMA200'] = talib.EMA(df['Close'], timeperiod=200)
        df['EMA200SH'] = df['EMA200'].shift(1)

        df['CloseSH'] = df['Close'].shift(1)

        columns = ['Close', 'EMA50', 'EMA100', 'EMA200', 'EMA50SH', 'EMA100SH', 'EMA200SH', 'CloseSH']

        def ma_cond(row, columns):
            cuEMA50 = crossunder(row['EMA50'], row['EMA50SH'], row['Close'], row['CloseSH'])
            cuEMA50Str = 'crossedDn EMA50Str'
            cuEMA100 = crossunder(row['EMA100'], row['EMA100SH'], row['Close'], row['CloseSH'])
            cuEMA100Str = 'crossedDn EMA100Str'
            cuEMA200 = crossunder(row['EMA200'], row['EMA200SH'], row['Close'], row['CloseSH'])
            cuEMA200Str = 'crossedDn EMA200Str'

            coEMA50 = crossover(row['EMA50'], row['EMA50SH'], row['Close'], row['CloseSH'])
            coEMA50Str = 'crossedUp EMA50Str'
            coEMA100 = crossover(row['EMA100'], row['EMA100SH'], row['Close'], row['CloseSH'])
            coEMA100Str = 'crossedUp EMA100Str'
            coEMA200 = crossover(row['EMA200'], row['EMA200SH'], row['Close'], row['CloseSH'])
            coEMA200Str = 'crossedUp EMA200Str'

            stru = cuEMA50Str if (cuEMA50) else \
                cuEMA100Str if (cuEMA100) else \
                    cuEMA200Str if (cuEMA200) else 'dumb'

            stro = coEMA50Str if (coEMA50) else \
                coEMA100Str if (coEMA100) else \
                    coEMA200Str if (coEMA200) else 'dumb'

            sell = (cuEMA50 | cuEMA100 | cuEMA200)
            buy = (coEMA50 | coEMA100 | coEMA200)
            string = stro if (buy) else \
                stru if (sell) else 'dumb'

            return buy, sell, string

        df['BUY'], df['SELL'], df['mystring'] = zip(*df.apply(lambda row: ma_cond(row, columns), axis=1))

        return df

    def scoreboard(self, df, row):
        if(self.udShow==-1):
            df['BUY'] = False
        elif(self.udShow==1):
            df['SELL'] = False

        columns = ['normal_time', 'BUY', 'SELL', 'mystring']

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
            normaltimevar = str(dfBS['normal_time'].iloc[-1])+'  '+dfBS['mystring'].iloc[-1]

        if 'Notes' in row:
            normaltimevar = str(normaltimevar) + '  ' + str(row['Notes'])

        #print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

