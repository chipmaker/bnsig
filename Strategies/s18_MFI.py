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

class s18_MFI(object):

   def __init__(self):
        self.strategy_name = 'S18_MFI'
        logging.info("Initializing s18_MFI")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.mfiPeriod = 5
        self.mfiOS = 10
        self.mfiOB = 90

   def run(self, df, row):
        #logging.info("Running s18_MFI")
        df = self.MFI(df)
        return self.monitor(df)

   def MFI(self, df):
        mfiOS = self.mfiOS
        mfiOB = self.mfiOB

        df['MFI10'] = self.money_flow_index(df, length=self.mfiPeriod)
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

   def get_drift(self, x: int):
       """Returns an int if not zero, otherwise defaults to one."""
       return int(x) if x and x != 0 else 1

   def get_offset(self, x: int):
        """Returns an int, otherwise defaults to zero."""
        return int(x) if x else 0

   def money_flow_index(self, data, length=14, vol_col='Volume', high_col='High', low_col='Low', close_col='Close',
                             drift=None,
                             offset=None, **kwargs):
            length = int(length) if length and length > 0 else 14

            drift = self.get_drift(drift)
            offset = self.get_offset(offset)

            # Calculate Result
            typical_price = (data[high_col] + data[low_col] + data[close_col]) / 3
            raw_money_flow = typical_price * data[vol_col]

            tdf = pd.DataFrame({'diff': 0, 'rmf': raw_money_flow, '+mf': 0, '-mf': 0})

            tdf.loc[(typical_price.diff(drift) > 0), 'diff'] = 1
            tdf.loc[tdf['diff'] == 1, '+mf'] = raw_money_flow

            tdf.loc[(typical_price.diff(drift) < 0), 'diff'] = -1
            tdf.loc[tdf['diff'] == -1, '-mf'] = raw_money_flow

            psum = tdf['+mf'].rolling(length).sum()
            nsum = tdf['-mf'].rolling(length).sum()
            tdf['mr'] = psum / nsum
            mfi = 100 * psum / (psum + nsum)
            tdf['mfi'] = mfi

            # Offset
            if offset != 0:
                mfi = mfi.shift(offset)

            # Handle fills
            if 'fillna' in kwargs:
                mfi.fillna(kwargs['fillna'], inplace=True)
            if 'fill_method' in kwargs:
                mfi.fillna(method=kwargs['fill_method'], inplace=True)

            return mfi

