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

class s200_UO(object):

   def __init__(self):
        self.strategy_name = 'S200_UO'
        logging.info("Initializing s200_UO")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0
        self.TP1 = 5
        self.TP2 = 10
        self.TP3 = 21
        self.uoOS = 25
        self.uoOB = 75

   def run(self, df, row):
        #logging.info("Running s200_UO")
        df = self.UO(df)
        return self.monitor(df)

   def UO(self, df):
        OS = self.uoOS
        OB = self.uoOB

        df['UO'] = self.UO2(df['High'], df['Low'], df['Close'], fast=self.TP1, medium=self.TP2, slow=self.TP3, drift=1)

        #df['UOSH'] = df['UO'].shift(1)
        #df['UO_BC'] = (df['UO'] < OS) & (df['UOSH'] >= OS)
        #df['UO_SC'] = (df['UO'] < OB) & (df['UOSH'] >= OB)

        df['UO_BC'] = (df['UO'] < OS)
        df['UO_SC'] = (df['UO'] > OB)

        df['BUY'] =  df['UO_BC']
        df['SELL'] = df['UO_SC']
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

   def get_drift(self, x:int):
        """Returns an int if not zero, otherwise defaults to one."""
        return int(x) if x and x != 0 else 1

   def get_offset(self, x:int):
        """Returns an int, otherwise defaults to zero."""
        return int(x) if x else 0

   def UO2(self, high, low, close, fast=None, medium=None, slow=None, fast_w=None, medium_w=None, slow_w=None, drift=None, offset=None, **kwargs):
        """Indicator: Ultimate Oscillator (UO)"""
        # Validate arguments
        drift = self.get_drift(drift)
        offset = self.get_offset(offset)

        fast = int(fast) if fast and fast > 0 else 7
        fast_w = float(fast_w) if fast_w and fast_w > 0 else 4.0

        medium = int(medium) if medium and medium > 0 else 14
        medium_w = float(medium_w) if medium_w and medium_w > 0 else 2.0

        slow = int(slow) if slow and slow > 0 else 28
        slow_w = float(slow_w) if slow_w and slow_w > 0 else 1.0

        # Calculate Result
        tdf = pd.DataFrame({'high': high, 'low': low, f"close_{drift}": close.shift(drift)})
        max_h_or_pc = tdf.loc[:, ['high', f"close_{drift}"]].max(axis=1)
        min_l_or_pc = tdf.loc[:, ['low', f"close_{drift}"]].min(axis=1)
        del tdf

        bp = close - min_l_or_pc
        tr = max_h_or_pc - min_l_or_pc

        fast_avg = bp.rolling(fast).sum() / tr.rolling(fast).sum()
        medium_avg = bp.rolling(medium).sum() / tr.rolling(medium).sum()
        slow_avg = bp.rolling(slow).sum() / tr.rolling(slow).sum()

        total_weight =  fast_w + medium_w + slow_w
        weights = (fast_w * fast_avg) + (medium_w * medium_avg) + (slow_w * slow_avg)
        uo = 100 * weights / total_weight

        # Offset
        if offset != 0:
            uo = uo.shift(offset)

        # Handle fills
        if 'fillna' in kwargs:
            uo.fillna(kwargs['fillna'], inplace=True)
        if 'fill_method' in kwargs:
            uo.fillna(method=kwargs['fill_method'], inplace=True)

        # Name and Categorize it
        uo.name = f"UO_{fast}_{medium}_{slow}"
        uo.category = 'momentum'

        return uo



