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
from numpy import NaN as npNaN
import pandas as pd

class sOBVEMA(object):

    def __init__(self):
        self.strategy_name = 'sOBVEMA'
        logging.info("Initializing sOBVEMA")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0

    def run(self, df, row):
        logging.info("Initializing sOBVEMA")
        df = self.sOBVEMA(df)
        return self.scoreboard(df, row)

    def sOBVEMA(self, df):
        df['OBV'] = self.obv(df['Close'], df['Volume'])
        df['OBVEMA'] = self.ema(df['OBV'], 9)

        df['OBVSH'] = df['OBV'].shift(1)
        df['OBVEMASH'] = df['OBVEMA'].shift(1)

        columns = ['OBV', 'OBVEMA', 'OBVSH', 'OBVEMASH']

        def obvCond(row, columns):
            buy = (row['OBVSH'] <= row['OBVEMASH']) & (row['OBV'] > row['OBVEMA'])
            sell = (row['OBVSH'] >= row['OBVEMASH']) & (row['OBV'] < row['OBVEMA'])
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: obvCond(row, columns), axis=1))
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

    def get_offset(self, x:int):
        """Returns an int, otherwise defaults to zero."""
        return int(x) if x else 0

    def signed_series(self, series:pd.Series, initial:int =None):
        """Returns a Signed Series with or without an initial value"""
        series = self.verify_series(series)
        sign = series.diff(1)
        sign[sign > 0] = 1
        sign[sign < 0] = -1
        sign.iloc[0] = initial
        return sign

    def verify_series(self, series:pd.Series):
        """If a Pandas Series return it."""
        if series is not None and isinstance(series, pd.core.series.Series):
            return series

    def obv(self, close, volume, offset=None, **kwargs):
        """Indicator: On Balance Volume (OBV)"""
        # Validate arguments
        close = self.verify_series(close)
        volume = self.verify_series(volume)
        offset = self.get_offset(offset)

        # Calculate Result
        signed_volume = self.signed_series(close, initial=1) * volume
        obv = signed_volume.cumsum()

        # Offset
        if offset != 0:
            obv = obv.shift(offset)

        # Handle fills
        if 'fillna' in kwargs:
            obv.fillna(kwargs['fillna'], inplace=True)
        if 'fill_method' in kwargs:
            obv.fillna(method=kwargs['fill_method'], inplace=True)

        # Name and Categorize it
        obv.name = f"OBV"
        obv.category = 'volume'

        return obv

    def ema(self, close, length=None, offset=None, **kwargs):
        """Indicator: Exponential Moving Average (EMA)"""
        # Validate Arguments
        close = self.verify_series(close)
        length = int(length) if length and length > 0 else 10
        min_periods = kwargs.pop('min_periods', length)
        adjust = kwargs.pop('adjust', True)
        offset = self.get_offset(offset)
        sma = kwargs.pop('sma', True)
        ewm = kwargs.pop('ewm', False)

        # Calculate Result
        if ewm:
            # Mathematical Implementation of an Exponential Weighted Moving Average
            ema = close.ewm(span=length, min_periods=min_periods, adjust=adjust).mean()
        else:
            alpha = 2 / (length + 1)
            close = close.copy()

            def ema_(series):
                # Technical Anaylsis Definition of an Exponential Moving Average
                # Slow for large series
                series.iloc[1] = alpha * (series.iloc[1] - series.iloc[0]) + series.iloc[0]
                return series.iloc[1]

            seed = close[0:length].mean() if sma else close.iloc[0]

            close[:length - 1] = npNaN
            close.iloc[length - 1] = seed
            ma = close[length - 1:].rolling(2, min_periods=2).apply(ema_, raw=False)
            ema = close[:length].append(ma[1:])

        # Offset
        if offset != 0:
            ema = ema.shift(offset)

        # Name & Category
        ema.name = f"EMA_{length}"
        ema.category = 'overlap'

        return ema

