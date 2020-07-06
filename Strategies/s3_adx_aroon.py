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
from testScenarios.strategy import Strategy
from Utils.mylogger import *

class s3_ADX5_AROON(Strategy):

    def __init__(self, config2tf):
        self.strategy_name = 'S3_ADX_AROON'
        logger.info("Initializing s3_ADX5_AROON")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf

    def run(self):
        logger.info("Initializing s3_ADX5_AROON")
        self.config2tfObjPtr.return_bs_dict={}

        for symbol in self.config2tfObjPtr.all_symbols:
            self.config2tfObjPtr.symbol = symbol
            self.config2tfObjPtr.make_symbol_data_paths()
            df_current = self.symbolObj.read_record_wchks(self.config2tfObjPtr)
            self.config2tfObjPtr.return_bs_dict[symbol] = self.ADX5_AROON(df_current)

        self.config2tfObjPtr.strategy_name = self.strategy_name
        self.tg_logger(self.config2tfObjPtr)

    def ADX5_AROON(self, df):
        adx5_exLevel = 95
        adx5_brLevel = 10

        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['PLUS_DI'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['MINUS_DI'] = talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX5'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ARDN'], df['ARUP'] = talib.AROON(df['High'].values, df['Low'].values, timeperiod=10)

        df['ADX5SHIFTED'] = df['ADX5'].shift(1)
        df['ARDNSHIFTED'] = df['ARDN'].shift(1)
        df['ARUPSHIFTED'] = df['ARUP'].shift(1)

        columns = ['PLUS_DI', 'MINUS_DI', 'ADX5', 'AROONDN', 'AROONUP', 'ADX5SHIFTED', 'ARDNSHIFTED', 'ARUPSHIFTED']

        def adx5_aroon_cond(row, columns):
            df1_adx5_cond = (row['ADX5'] > row['ADX5SHIFTED']) & (row['ADX5'] > adx5_brLevel) & (
                        row['ADX5'] < adx5_exLevel)
            arbuy = (row['ARUPSHIFTED'] < 5) & (row['ARUP'] > 85) & (row['ARUP'] > row['ARDN'])
            arsell = (row['ARDNSHIFTED'] < 5) & (row['ARDN'] > 85) & (row['ARUP'] < row['ARDN'])
            buy = (row['PLUS_DI'] > row['MINUS_DI']) & df1_adx5_cond & arbuy
            sell = (row['PLUS_DI'] < row['MINUS_DI']) & df1_adx5_cond & arsell
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: adx5_aroon_cond(row, columns), axis=1))

        df2 = df.tail(self.withinBars)
        df2['BUY'].any()
        df2['SELL'].any()

        #return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
        return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]
