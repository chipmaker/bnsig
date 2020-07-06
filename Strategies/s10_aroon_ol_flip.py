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

from testScenarios.strategy import Strategy
from Utils.mylogger import *


class s10_AROON_OL_FLIP(Strategy):

    def __init__(self, config2tf):
        self.strategy_name = 'S10_AROON_OL_FLIP'
        logger.info("Initializing s10_AROON_OL_FLIP")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf
        self.withinBars = 1

    def run(self, df):
        logger.info("Initializing s10_AROON_OL_FLIP")
        return self.AROON_OL_FLIP(df)

    def AROON_OL_FLIP(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['ARDN'], df['ARUP'] = self.AROON(df, periods=10)
        df['AR5DN'], df['AR5UP'] = self.AROON(df, periods=5)

        df['AR10BUY'] = ((df['ARUP'] > df['ARDN']) & (df['ARUP'] > 85)) & ((df['ARUP'].shift(1) < 5) | (df['ARUP'].shift(2) < 5))
        df['AR10SELL'] = ((df['ARDN'] > df['ARUP']) & (df['ARDN'] > 85)) & ((df['ARDN'].shift(1) < 5) | (df['ARDN'].shift(2) < 5))

        df['AR5BUY'] = ((df['AR5UP'] > df['AR5DN']) & (df['AR5UP'] > 85)) & ((df['AR5UP'].shift(1) < 5) | (df['AR5UP'].shift(2) < 5))
        df['AR5SELL'] = ((df['AR5DN'] > df['AR5UP']) & (df['AR5DN'] > 85)) & ((df['AR5DN'].shift(1) < 5) | (df['AR5DN'].shift(2) < 5))

        df['AR5BC'] = (df['AR5BUY'] | df['AR5BUY'].shift(1) | df['AR5BUY'].shift(2))
        df['AR5SC'] = (df['AR5SELL'] | df['AR5SELL'].shift(1) | df['AR5SELL'].shift(2))

        df['BUY'] = df['AR10BUY'] & df['AR5BC']
        df['SELL'] = df['AR10SELL'] & df['AR5SC']

        df2 = df.tail(self.withinBars)
        df2['BUY'].any()
        df2['SELL'].any()
        #return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
        return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]

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

