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
import talib
from Utils.mylogger import *

class s18_MFI_talib(object):

   def __init__(self):
        self.strategy_name = 'S18_MFI_talib'
        logger.info("Initializing s18_MFI_talib")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.mfiPeriod = 5
        self.mfiOS = 10
        self.mfiOB = 90

   def run(self, df, row):
        df = self.MFI(df)
        return self.monitor(df)

   def MFI(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        mfiOS = self.mfiOS
        mfiOB = self.mfiOB

        df['MFI10'] = talib.MFI(df['High'], df['Low'], df['Close'], df['Volume'], timeperiod=self.mfiPeriod)

        #df['MFI10'] = self.money_flow_index(df, length=self.mfiPeriod)
        df['MFI10SH'] = df['MFI10'].shift(1)

        df['MFI_BC'] = (df['MFI10'] > mfiOS) & (df['MFI10SH'] <= mfiOS)
        df['MFI_SC'] = (df['MFI10'] < mfiOB) & (df['MFI10SH'] >= mfiOB)

        df['BUY'] =  df['MFI_BC']
        df['SELL'] = df['MFI_SC']
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

