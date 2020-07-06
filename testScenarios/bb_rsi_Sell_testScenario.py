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

from Strategies.s15_adx_rsi_cci import s15_ADX_RSI_CCI
from Strategies.s16_fib_ext import s16_FIB_EXT
from .testScenario import testScenario

class bb_rsi_sell_testScenario(testScenario):
    def __init__(self, Config2tf, sym_filename_only):
       """Constructor for $class$"""
       super().__init__(Config2tf)
       self.read_test_symbols(self.config2tfPtr.exchange_data_folder, sym_filename_only)
       self.set_scenarios()

    def set_scenarios(self):
        s15_ADX_RSI_CCIObj2 = s15_ADX_RSI_CCI()
        s15_ADX_RSI_CCIObj2.strategy_name = 'BBRSI_ADX_RSI_CCI_SELL_SHOW'
        s15_ADX_RSI_CCIObj2.withinBars = 1
        s15_ADX_RSI_CCIObj2.udShow = -1
        s15_ADX_RSI_CCIObj2.cciFilter = True
        s15_ADX_RSI_CCIObj2.cciEMALength = 4
        s15_ADX_RSI_CCIObj2.cciTOS = 0
        s15_ADX_RSI_CCIObj2.cciTOB = 0
        self.stObjList.append(s15_ADX_RSI_CCIObj2)

        s16_FIB_EXTObj2 = s16_FIB_EXT()
        s16_FIB_EXTObj2.strategy_name = 'BBRSI_FIB_EXT_SELL_SHOW'
        s16_FIB_EXTObj2.withinBars = 1
        s16_FIB_EXTObj2.udShow = -1
        self.stObjList.append(s16_FIB_EXTObj2)

