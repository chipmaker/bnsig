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
from app.config import Config2tf
from collections import defaultdict
from Utils.mylogger import *

class s5_ADX_MACD_1d_4h(Strategy):

    def __init__(self, config2tf):
        logger.info("Initializing s5_ADX_OL_MACD_1d_4h")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf
        #print(self.config2tfObjPtr)
        self.return_4h_dict =defaultdict(list)

        #Setting 1d Parameters
        self.config2tf_1d_Obj = Config2tf(self.config2tfObjPtr.get_args())
        #print(self.Config2tf_1dr_Obj)
        self.config2tf_1d_Obj.timeframe = self.config2tfObjPtr.second_timeframe
        self.config2tf_1d_Obj.run()

        self.flag_1d = 0
        self.return_1d_dict=defaultdict(list)

    def run(self):
        print("Running s5_ADX_OL_MACD_1d_4h")
        self.config2tfObjPtr.return_bs_dict={}
        self.return_4h_dict ={}
        if((self.flag_1d % 4)==0) :
            self.return_1d_dict={}

        for symbol in self.config2tfObjPtr.all_symbols:
            ###4h Params
            self.config2tfObjPtr.symbol = symbol
            this_symbol = self.config2tfObjPtr.symbol_out
            self.config2tfObjPtr.make_symbol_data_paths(this_symbol)
            #if os.path.isfile(self.config2tfObjPtr.currentRun_filename_path):
            #    print("CALLING s1_ADX_Overlap on {}".format(self.config2tfObjPtr.currentRun_filename_path))
            #    self.config2tfObjPtr.return_bs_dict[self.config2tfObjPtr.symbol] = self.ADX_Overlap(self.config2tfObjPtr)
            #else:
            df_current = self.symbolObj.read_record_wchks(self.config2tfObjPtr)
            self.return_4h_dict[symbol] = self.ADX_OL_MACD(df_current)

            ###1d_Params
            self.config2tf_1d_Obj.symbol = symbol
            self.config2tf_1d_Obj.symbol_out=this_symbol
            self.config2tf_1d_Obj.make_symbol_data_paths(this_symbol)
            if((self.flag_1d % 4)==0) :
                df_4hr = self.symbolObj.read_record_wchks(self.config2tf_1d_Obj)
                self.return_1d_dict[symbol] = self.ADX_MACDHist(df_4hr)

            self.config2tfObjPtr.return_bs_dict[symbol] = self.bs_intersection(self.return_1d_dict[symbol], self.return_4h_dict[symbol])

        self.config2tfObjPtr.strategy_name = 's5_adx_macd_1d_4h'
        self.tg_logger(self.config2tfObjPtr)
        self.flag_1d=self.flag_1d+1

        self.config2tfObjPtr.strategy_name = 's5_adx_macd_1d_4h:4hr_dict'
        self.config2tfObjPtr.return_bs_dict = self.return_4h_dict
        self.tg_logger(self.config2tfObjPtr)

        self.config2tf_1d_Obj.strategy_name = 's5_adx_macd_1d_4h:OnlyHist:1d_dict'
        self.config2tf_1d_Obj.return_bs_dict = self.return_1d_dict
        self.tg_logger(self.config2tf_1d_Obj)

    def bs_intersection(self, list1, list2):
        out0=list1[0] & list2[0]
        out1=list1[1] & list2[1]
        return [out0, out1]

    def ADX_OL_MACD(self, df):
        adx5_exLevel = 70
        adx5_brLevel = 25
        adx14_exLevel = 40
        adx14_brLevel = 15

        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['PLUS_DI'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['MINUS_DI'] = talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX5'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX14'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=14)

        df['ADX5SHIFTED'] = df['ADX5'].shift(1)
        df['ADX14SHIFTED'] = df['ADX14'].shift(1)

        df['macdLine'], df['macdSignal'], df['histLine'] =talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
        df['histLineSHIFTED'] = df['histLine'].shift(1)
        columns = ['PLUS_DI', 'MINUS_DI', 'ADX5', 'ADX14', 'ADX5SHIFTED', 'ADX14SHIFTED', 'macdLine', 'histLine', 'histLineSHIFTED']

        def adx5_14_ol_macd_cond(row, columns):
            df1_adx5_cond = (row['ADX5'] > row['ADX5SHIFTED']) & (row['ADX5'] > adx5_brLevel) & (row['ADX5'] < adx5_exLevel)
            df2_adx14_cond = (row['ADX14'] > row['ADX14SHIFTED']) & (row['ADX14'] > adx14_brLevel) & (row['ADX14'] < adx14_exLevel)
            df3_adx5_14_ol = df1_adx5_cond & df2_adx14_cond
            adx_buy = (row['PLUS_DI'] > row['MINUS_DI']) & df3_adx5_14_ol
            adx_sell = (row['PLUS_DI'] < row['MINUS_DI']) & df3_adx5_14_ol

            histA_IsUp = (row['histLine'] > row['histLineSHIFTED']) & (row['histLine'] > 0)
            histB_IsDown = (row['histLine'] < row['histLineSHIFTED']) & (row['histLine'] <= 0)

            macd_BuyCond = histA_IsUp & (row['macdLine'] > 0)
            macd_SellCond = histB_IsDown & (row['macdLine'] < 0)

            adx_macd_buy = adx_buy & macd_BuyCond
            adx_macd_sell = adx_sell & macd_SellCond

            return adx_macd_buy, adx_macd_sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: adx5_14_ol_macd_cond(row, columns), axis=1))

        return [df['SELL'].iloc[-1], df['BUY'].iloc[-1]]

    def ADX_MACDHist(self, df):
        adx5_exLevel = 70
        adx5_brLevel = 25

        df.drop(df.last_valid_index(), axis=0, inplace=True)

        df['PLUS_DI'] = talib.PLUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['MINUS_DI']= talib.MINUS_DI(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)
        df['ADX5'] = talib.ADX(df['High'].values, df['Low'].values, df['Close'].values, timeperiod=5)

        df['ADX5SHIFTED']=df['ADX5'].shift(1)

        df['macdLine'], df['macdSignal'], df['histLine'] = talib.MACD(df['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        columns =['PLUS_DI', 'MINUS_DI', 'ADX5', 'ADX5SHIFTED', 'histLine']

        def adx5_macd_cond(row, columns):
            df1_adx5_cond= (row['ADX5'] > row['ADX5SHIFTED']) & (row['ADX5'] > adx5_brLevel) & (row['ADX5'] < adx5_exLevel)
            adx_buy  = (row['PLUS_DI'] > row['MINUS_DI']) & df1_adx5_cond
            adx_sell = (row['PLUS_DI'] < row['MINUS_DI']) & df1_adx5_cond

            macd_BuyCond = row['histLine'] > 0
            macd_SellCond = row['histLine'] < 0

            adx_macd_buy = adx_buy & macd_BuyCond
            adx_macd_sell= adx_sell & macd_SellCond

            return adx_macd_buy, adx_macd_sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: adx5_macd_cond(row, columns), axis=1))

        return [df['SELL'].iloc[-1], df['BUY'].iloc[-1]]
