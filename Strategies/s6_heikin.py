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

class s6_Heikin(Strategy):

    def __init__(self, config2tf):
        logger.info("Initializing s1_ADX_Overlap")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf
        #print(self.config2tfObjPtr)

    def run(self):
        logger.info("Running s1_ADX_Overlap")
        self.config2tfObjPtr.return_bs_dict={}

        for symbol in self.config2tfObjPtr.all_symbols:
            self.config2tfObjPtr.symbol = symbol
            #self.config2tfObjPtr.symbol_out = symbol.replace("/", "")
            this_symbol = self.config2tfObjPtr.symbol_out
            self.config2tfObjPtr.make_symbol_data_paths(this_symbol)
            df_current = self.symbolObj.read_record_wchks(self.config2tfObjPtr)
            self.config2tfObjPtr.return_bs_dict[symbol] = self.ADX_Overlap(df_current)

        self.config2tfObjPtr.strategy_name = 's1_adx_overlap'
        self.tg_logger(self.config2tfObjPtr)

    def ADX_Overlap(self, df):
        adx5_exLevel = 70
        adx5_brLevel = 25
        adx14_exLevel = 45
        adx14_brLevel = 15

        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['PLUS_DI'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['MINUS_DI'] = talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX5'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX14'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=14)

        df['ADX5SHIFTED'] = df['ADX5'].shift(1)
        df['ADX14SHIFTED'] = df['ADX14'].shift(1)

        columns = ['PLUS_DI', 'MINUS_DI', 'ADX5', 'ADX14', 'ADX5SHIFTED', 'ADX14SHIFTED']

        def adx5_14_ol_cond(row, columns):
            df1_adx5_cond = (row['ADX5'] > row['ADX5SHIFTED']) & (row['ADX5'] > adx5_brLevel) & (
                        row['ADX5'] < adx5_exLevel)
            df2_adx14_cond = (row['ADX14'] > row['ADX14SHIFTED']) & (row['ADX14'] > adx14_brLevel) & (
                        row['ADX14'] < adx14_exLevel)
            df3_adx5_14_ol = df1_adx5_cond & df2_adx14_cond
            df4_buy = (row['PLUS_DI'] > row['MINUS_DI']) & df3_adx5_14_ol
            df5_sell = (row['PLUS_DI'] < row['MINUS_DI']) & df3_adx5_14_ol
            return df4_buy, df5_sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: adx5_14_ol_cond(row, columns), axis=1))
        new_buy_entry  = (df['BUY'].iloc[-1]==True) & (df['BUY'].iloc[-2]==False)
        new_sell_entry = (df['SELL'].iloc[-1]==True) & (df['SELL'].iloc[-2]==False)
        return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], new_sell_entry, new_buy_entry]

    def ADX_Overlap_old(self, args):
        adx5_exLevel = 70
        adx5_brLevel = 25
        adx14_exLevel = 45
        adx14_brLevel = 15

        df = args.df_current
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['PLUS_DI'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['MINUS_DI'] = talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX5'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX14'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=14)
        df['ADX5_Cond'] = (df.ADX5 > df.ADX5.shift(1)) & (df.ADX5 > adx5_brLevel) & (df.ADX5 < adx5_exLevel)
        df['ADX14_Cond'] = (df.ADX14 > df.ADX14.shift(1)) & (df.ADX14 > adx14_brLevel) & (df.ADX14 < adx14_exLevel)
        df['ADX5_14_OL'] = df['ADX5_Cond'] & df['ADX14_Cond']

        df['BUY'] = (df['PLUS_DI'] > df['MINUS_DI']) & df['ADX5_14_OL']
        df['SELL'] = (df['PLUS_DI'] < df['MINUS_DI']) & df['ADX5_14_OL']
        return [df['SELL'].iloc[-1], df['BUY'].iloc[-1]]
