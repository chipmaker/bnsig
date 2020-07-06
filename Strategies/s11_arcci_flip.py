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

from Utils.mylogger import *
from numpy import fabs as npfabs
import pandas as pd

class s11_ArCCI_FLIP(object):

    def __init__(self):
        self.strategy_name = 'S11_ArCCI_FLIP'
        logger.info("Initializing s11_ArCCI_FLIP")
        """Constructor for $class$"""
        self.withinBars = 1
        self.udShow = 0

    def run(self, df, row):
        logger.info("Initializing s11_ArCCI_FLIP")
        df = self.ArCCI_FLIP(df)
        return self.scoreboard(df)

    def ArCCI_FLIP(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['ARDN'], df['ARUP'] = self.AROON(df, periods=10)
        df['AR5DN'], df['AR5UP'] = self.AROON(df, periods=5)
        df['CCI'] = self.fcci(df['High'], df['Low'], df['Close'], 100)
        df['CCIEMA200'] = self.ema(df['CCI'], 4)

        df['CCIEMABUY'] = (df['CCIEMA200'] < 0)
        df['CCIEMASELL'] = (df['CCIEMA200'] > 0)

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

        df['BUY'] = df['AR10BUY'] & df['AR5BC'] & df['CCIEMABUY']
        df['SELL'] = df['AR10SELL'] & df['AR5SC'] & df['CCIEMASELL']

        return df

    def scoreboard(self, df):
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
        aroon_up = 100 * (df['High'].rolling(periods).apply(lambda x: x.argmax(), raw=True) / (periods - 1))
        aroon_down = 100 * (df['Low'].rolling(periods).apply(lambda x: x.argmin(), raw=True) / (periods - 1))
        return [aroon_down, aroon_up]

    def verify_series(self, series: pd.Series):
        """If a Pandas Series return it."""
        if series is not None and isinstance(series, pd.core.series.Series):
            return series

    def get_offset(self, x: int):
        """Returns an int, otherwise defaults to zero."""
        return int(x) if x else 0

    def signed_series(self, series: pd.Series, initial: int = None):
        """Returns a Signed Series with or without an initial value"""
        series = verify_series(series)
        sign = series.diff(1)
        sign[sign > 0] = 1
        sign[sign < 0] = -1
        sign.iloc[0] = initial
        return sign

    def hlc3(self, high, low, close, offset=None):
        """Indicator: HLC3"""
        # Validate Arguments
        high = self.verify_series(high)
        low = self.verify_series(low)
        close = self.verify_series(close)
        offset = self.get_offset(offset)

        # Calculate Result
        hlc3 = (high + low + close) / 3

        # Offset
        if offset != 0:
            hlc3 = hlc3.shift(offset)

        # Name & Category
        hlc3.name = "HLC3"
        hlc3.category = 'overlap'

        return hlc3

    def mad(self, close, length=None, offset=None, **kwargs):
        """Indicator: Mean Absolute Deviation"""
        # Validate Arguments
        close = self.verify_series(close)
        length = int(length) if length and length > 0 else 30
        min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs[
            'min_periods'] is not None else length
        offset = self.get_offset(offset)

        # Calculate Result
        def mad_(series):
            """Mean Absolute Deviation"""
            return npfabs(series - series.mean()).mean()

        mad = close.rolling(length, min_periods=min_periods).apply(mad_, raw=True)

        # Offset
        if offset != 0:
            mad = mad.shift(offset)

        # Name & Category
        mad.name = "MAD_{length}"
        mad.category = 'statistics'

        return mad

    def sma(self, close, length=None, offset=None, **kwargs):
        """Indicator: Simple Moving Average (SMA)"""
        # Validate Arguments
        close = self.verify_series(close)
        length = int(length) if length and length > 0 else 10
        min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs[
            'min_periods'] is not None else length
        offset = self.get_offset(offset)

        # Calculate Result
        sma = close.rolling(length, min_periods=min_periods).mean()

        # Offset
        if offset != 0:
            sma = sma.shift(offset)

        # Name & Category
        sma.name = "SMA_{length}"
        sma.category = 'overlap'

        return sma

    def ema(self, close, length=None, offset=None, **kwargs):
        """Indicator: Exponential Moving Average (EMA)"""
        # Validate Arguments
        length = int(length) if length and length > 0 else 10
        min_periods = kwargs.pop('min_periods', length)
        adjust = kwargs.pop('adjust', True)

        # Mathematical Implementation of an Exponential Weighted Moving Average
        ema = close.ewm(span=length, min_periods=min_periods, adjust=adjust).mean()
        return ema

    def fcci(self, high, low, close, length=None, c=None, offset=None, **kwargs):
        """Indicator: Commodity Channel Index (CCI)"""
        # Validate Arguments
        high = self.verify_series(high)
        low = self.verify_series(low)
        close = self.verify_series(close)
        length = int(length) if length and length > 0 else 20
        c = float(c) if c and c > 0 else 0.015
        min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs[
            'min_periods'] is not None else length
        offset = self.get_offset(offset)

        # Calculate Result
        typical_price = self.hlc3(high=high, low=low, close=close)
        mean_typical_price = self.sma(typical_price, length=length)
        mad_typical_price = self.mad(typical_price, length=length)

        cci = typical_price - mean_typical_price
        cci /= c * mad_typical_price

        # Offset
        if offset != 0:
            cci = cci.shift(offset)

        # Handle fills
        if 'fillna' in kwargs:
            cci.fillna(kwargs['fillna'], inplace=True)
        if 'fill_method' in kwargs:
            cci.fillna(method=kwargs['fill_method'], inplace=True)

        # Name and Categorize it
        cci.name = "CCI_{length}_{c}"
        cci.category = 'momentum'

        return cci
