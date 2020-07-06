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

class s14_MFI_OL(Strategy):

    def __init__(self, config2tf):
        self.strategy_name = 'S14_MFI_OL'
        logger.info("Initializing s14_MFI_OL")
        """Constructor for $class$"""
        super().__init__(config2tf)
        self.config2tfObjPtr = config2tf

    def run(self, df):
        logger.info("Initializing s14_MFI_OL")
        return self.MFI_OL(df)

    def MFI_OL(self, df):
        df.drop(df.last_valid_index(), axis=0, inplace=True)

        mfiOB = 80
        mfiOS = 20

        dfMFI10 = pta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=10)
        dfMFI5 = pta.mfi(df['High'], df['Low'], df['Close'], df['Volume'], length=5)

        df=df.join(dfMFI10)
        df=df.join(dfMFI5)

        df['MFI_10SH'] =df['MFI_10'].shift(1)
        df['MFI_5SH'] =df['MFI_5'].shift(1)

        columns =['MFI_10', 'MFI_5', 'MFI_10SH', 'MFI_5SH']

        def mfi_cond(row, columns):
            MFI_10BC = (row['MFI_10SH'] <= mfiOS) & (row['MFI_10'] > mfiOS) & (row['MFI_10SH'] < mfiOS)
            MFI_10SC = (row['MFI_10SH'] >= mfiOB) & (row['MFI_10'] < mfiOB) & (row['MFI_10SH'] > mfiOB)
            MFI_5BC = (row['MFI_5SH'] <= mfiOS) & (row['MFI_5'] > mfiOS) & (row['MFI_5SH'] < mfiOS)
            MFI_5SC = (row['MFI_5SH'] >= mfiOB) & (row['MFI_5'] < mfiOB) & (row['MFI_5SH'] > mfiOB)

            buy = (MFI_10BC & MFI_5BC)
            sell = (MFI_10SC & MFI_5SC)
            return buy, sell

        df['BUY'], df['SELL'] = zip(*df.apply(lambda row: mfi_cond(row, columns), axis=1))

        df2 = df.tail(self.withinBars)
        print('WithinBars{}'.format(self.withinBars))
        df2['BUY'].any()
        df2['SELL'].any()
        #return [df['SELL'].iloc[-1], df['BUY'].iloc[-1], df['normal_time']]
        return [df2['SELL'].any(), df2['BUY'].any(), df['normal_time'].iloc[-1]]

