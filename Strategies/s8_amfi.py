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

class s8_AMFI(object):

   def __init__(self):
        self.strategy_name = 'S8_AMFI'
        logging.info("Initializing s8_AMFI")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0

   def run(self, df, row):
        #logging.info("Running s8_AMFI")
        df = self.AMFI(df)
        return self.monitor(df)

   def AMFI(self, df):

        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['MFI20'] = self.money_flow_index(df, length=20)
        df['MFI20EMA'] = self.ema(df['MFI20'], 19)
        df['MFI10'] = self.money_flow_index(df, length=10)
        df['MFI10EMA'] = self.ema(df['MFI10'], 9)

        df['MFI_BC'] = df['MFI10EMA'] > df['MFI20EMA']
        df['MFI_SC'] = df['MFI10EMA'] < df['MFI20EMA']

        df['ARDN'], df['ARUP'] = self.AROON(df, periods=10)
        df['AR5DN'], df['AR5UP'] = self.AROON(df, periods=5)

        df['AR10BUY'] = ((df['ARUP'] > df['ARDN']) & (df['ARUP'] > 85)) & \
                        ((df['ARUP'].shift(1) < 5) | (df['ARUP'].shift(2) < 5))
        df['AR10SELL'] = ((df['ARDN'] > df['ARUP']) & (df['ARDN'] > 85)) & \
                         ((df['ARDN'].shift(1) < 5) | (df['ARDN'].shift(2) < 5))

        df['AR5BUY'] = ((df['AR5UP'] > df['AR5DN']) & (df['AR5UP'] > 85)) & \
                       ((df['AR5UP'].shift(1) < 5) | (df['AR5UP'].shift(2) < 5))
        df['AR5SELL'] = ((df['AR5DN'] > df['AR5UP']) & (df['AR5DN'] > 85)) & \
                        ((df['AR5DN'].shift(1) < 5) | (df['AR5DN'].shift(2) < 5))

        df['AR5BC'] = (df['AR5BUY'] | df['AR5BUY'].shift(1) | df['AR5BUY'].shift(2))
        df['AR5SC'] = (df['AR5SELL'] | df['AR5SELL'].shift(1) | df['AR5SELL'].shift(2))

        df['BUY'] = df['AR10BUY'] & df['AR5BC'] & df['MFI_BC']
        df['SELL'] = df['AR10SELL'] & df['AR5SC'] & df['MFI_SC']

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

   def AROON(self, df, periods = 25):
        # Returns a dataframe read from filepath with aroon indicator put in columns from col_name
        # col_name - 2 element list, where the first element is the name for aroon up column,
        # and the second is the name for aroon down column
        # Aroon Up = ( N - Nhc) / N * 100
        # Aroon Down = ( N - Nlc) / N * 100
        # where N - periods provided by the function,
        # Nhc, Nlc - periods since N-period high and periods since N-period low respectively
        aroon_up = df['High'].rolling(periods+1).apply(lambda x: x.argmax(), raw=True) / periods * 100
        aroon_down = df['Low'].rolling(periods+1).apply(lambda x: x.argmin(), raw=True) / periods * 100
        return [aroon_down, aroon_up]

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

            # Name and Categorize it
            mfi.name = "MFI_{length}"
            mfi.category = 'volume'

            return mfi

   def ema(self, close, length=None, offset=None, **kwargs):
        """Indicator: Exponential Moving Average (EMA)"""
        # Validate Arguments
        length = int(length) if length and length > 0 else 10
        min_periods = kwargs.pop('min_periods', length)
        adjust = kwargs.pop('adjust', True)

        # Mathematical Implementation of an Exponential Weighted Moving Average
        ema = close.ewm(span=length, min_periods=min_periods, adjust=adjust).mean()
        return ema

