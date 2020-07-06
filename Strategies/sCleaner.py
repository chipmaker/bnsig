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
from Utils.helpers import date_to_milliseconds
from datetime import datetime

class sCleaner(object):

    def __init__(self):
        self.strategy_name = 'sCleaner'
        logging.info("Initializing sCleaner")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.current_date_utc = str(datetime.utcnow())
        self.current_timestamp = date_to_milliseconds(self.current_date_utc)
        self.current_interval = 86400
        self.latest_timestamp = (self.current_timestamp - self.current_timestamp % self.current_interval)

    def run(self, df, row):
        logging.info("Initializing sCleaner")
        df = self.sCleaner(df)
        #print('df={}'.format(df))
        return self.scoreboard(df, row)

    def sCleaner(self, df):
        if(df.shape[0] < 100):
            df['BUY'] = False
            df['SELL'] = True
        else:
            last_timestamp = int(df['Timestamp'].iloc[-1])
            since_lastrec_timestamp = (self.latest_timestamp - last_timestamp)
            if(since_lastrec_timestamp > self.current_interval*299):    ##Is last run older than 128 records
               df['BUY'] = False
               df['SELL'] = True
            else:
               df['BUY'] = True
               df['SELL'] = False
        return df

    def scoreboard(self, df, row):
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

        if 'Notes' in row:
            normaltimevar = str(normaltimevar) + '  ' + str(row['Notes'])
        #print('udShow={}, sellvar={}, buyvar={}, normalvar={}'.format(self.udShow, sellvar, buyvar, normaltimevar))
        return [sellvar, buyvar, normaltimevar]

#df2 = df.tail(self.withinBars)
#df2['BUY'].any()
#df2['SELL'].any()
#return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
#return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]
