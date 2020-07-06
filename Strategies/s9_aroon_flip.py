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

class s9_AROON_FLIP(Strategy):

    def __init__(self, config2tf):
        self.strategy_name = 'S9_AROON_FLIP'
        logger.info("Initializing s9_AROON_FLIP")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf

    def run(self):
        logger.info("Initializing s9_AROON_FLIP")
        self.config2tfObjPtr.return_bs_dict={}

        for symbol in self.config2tfObjPtr.all_symbols:
            self.config2tfObjPtr.symbol = symbol
            self.config2tfObjPtr.make_symbol_data_paths()
            df_current = self.symbolObj.read_record_wchks(self.config2tfObjPtr)
            self.config2tfObjPtr.return_bs_dict[symbol] = self.AROON_FLIP(df_current)

        self.config2tfObjPtr.strategy_name = self.strategy_name
        self.tg_logger(self.config2tfObjPtr)

    def AROON_FLIP(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['ARDN'], df['ARUP'] = self.AROON(df, 10)

        df['BUY'] = (df['ARUP'].shift(1) < 5) & ((df['ARUP'] > 85) & (df['ARUP'] > df['ARDN']))
        df['SELL'] = (df['ARDN'].shift(1) < 5) & ((df['ARDN'] > 85) & (df['ARUP'] < df['ARDN']))

        df2 = df.tail(self.withinBars)
        df2['BUY'].any()
        df2['SELL'].any()
        #return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
        return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]

    def AROON_FLIP2(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['ARDN'], df['ARUP'] = self.AROON(df, 10)
        df['ARDNSHIFTED']=df['ARDN'].shift(1)
        df['ARUPSHIFTED']=df['ARUP'].shift(1)

        columns =['AROONDN', 'AROONUP', 'ARDNSHIFTED', 'ARUPSHIFTED']

        def aroon_cond(row, columns):
            arbuy = (row['ARUPSHIFTED'] < 5) & (row['ARUP'] > 85) & (row['ARUP'] > row['ARDN'])
            arsell = (row['ARDNSHIFTED'] < 5) & (row['ARDN'] > 85) & (row['ARUP'] < row['ARDN'])
            buy  = arbuy
            sell = arsell
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: aroon_cond(row, columns), axis=1))
        df2 = df.tail(self.withinBars)
        df2['BUY'].any()
        df2['SELL'].any()
        #return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
        return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]

    def AROON2(self, df, periods = 25):
        arup = 100 * (periods-1 + df['High'].rolling(periods).apply(lambda x: x.argmax(), raw=True)) / (periods-1)
        ardn = 100 * (periods-1 + df['Low'].rolling(periods).apply(lambda x: x.argmin(), raw=True)) / (periods-1)
        return ardn, arup

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
