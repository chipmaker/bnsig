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

class s12_ADX5_RSI(Strategy):

    def __init__(self, config2tf):
        self.strategy_name = 'S12_ADX5_RSI'
        logger.info("Initializing s12_ADX5_RSI")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf

    def run(self, df):
        logger.info("Initializing s12_ADX5_RSI")
        return self.ADX5_RSI(df)

    def ADX5_RSI(self, df):
        rsi30L = 30
        rsi40L = 40
        rsi50L = 50
        rsi60L = 60
        rsi70L = 70

        dfADX = pta.adx(df['High'], df['Low'], df['Close'], length=5)
        dfRSI = pta.rsi(df['Close'], length=14)

        df = df.join(dfADX)
        df = df.join(dfRSI)

        df['DMP_5SH'] = df['DMP_5'].shift(1)
        df['DMN_5SH'] = df['DMN_5'].shift(1)
        df['RSI_14SH'] = df['RSI_14'].shift(1)

        columns = ['ADX_5', 'DMP_5', 'DMN_5', 'DMP_5SH', 'DMN_5SH', 'RSI_14', 'RSI_14SH']

        def adx5_rsi_cond(row, columns):
            # df1_adx5_cond= (row['ADX_5'] > row['ADX_5SH']) & (row['ADX_5'] > adx5_brLevel) & (row['ADX_5'] < adx5_exLevel)
            adxBuy = (row['DMP_5SH'] <= row['DMN_5SH']) & (row['DMP_5'] > row['DMN_5'])
            adxSell = (row['DMP_5SH'] >= row['DMN_5SH']) & (row['DMP_5'] < row['DMN_5'])
            rsiBuy = ((row['RSI_14SH'] <= rsi30L) & (row['RSI_14'] > rsi30L)) \
                     | ((row['RSI_14SH'] <= rsi40L) & (row['RSI_14'] > rsi40L)) \
                     | ((row['RSI_14SH'] <= rsi50L) & (row['RSI_14'] > rsi50L))
            rsiSell = ((row['RSI_14SH'] >= rsi70L) & (row['RSI_14'] < rsi70L)) \
                      | ((row['RSI_14SH'] >= rsi60L) & (row['RSI_14'] < rsi60L)) \
                      | ((row['RSI_14SH'] >= rsi50L) & (row['RSI_14'] < rsi50L))
            buy = (adxBuy & rsiBuy)
            sell = (adxSell & rsiSell)
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: adx5_rsi_cond(row, columns), axis=1))

        df2 = df.tail(self.withinBars)
        df2['BUY'].any()
        df2['SELL'].any()

        #return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
        return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time']]
