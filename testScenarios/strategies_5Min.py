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

import time
from .strategy import Strategy
####Strategies
#from .s3_adx_aroon import s3_ADX5_AROON

###TestScenarios for 5Min
from testScenarios.bb_rsi_Buy_testScenario import bb_rsi_buy_testScenario
from testScenarios.bb_rsi_Sell_testScenario import bb_rsi_sell_testScenario
from testScenarios.fib_ext_15m_Sell_testScenario import fib_ext_15m_sell_testscenario
from testScenarios.bb_rsi_cci_testScenario import bb_rsi_cci_testScenario
from testScenarios.simple_testScenario import simple_testScenario

class Strategies_5Min(Strategy):

    def __init__(self, args, cbIF):
       """Constructor for $class$"""
       super().__init__(args, cbIF)
       self.name = 'Strategies_5Min'
       self.set_strategies()

    def set_strategies(self):
      ######simple_testScenario
      sym_filename_only = '5MinSimpleTS.csv'
      TS1Obj = simple_testScenario(self.Config2tfObj, sym_filename_only)
      self.tsObjList.append(TS1Obj)
      ####End of Test Scenario1

#      #####Test Scenario1
#      sym_filename_only = '5MinTS1.csv'
#      TS1Obj = bb_rsi_buy_testScenario(self.Config2tfObj, sym_filename_only)
#      self.tsObjList.append(TS1Obj)
#      ###End of Test Scenario1
#
#      #####Test Scenario2
#      sym_filename_only = '5MinTS2.csv'
#      TS2Obj = bb_rsi_sell_testScenario(self.Config2tfObj, sym_filename_only)
#      self.tsObjList.append(TS2Obj)
#      ###End of Test Scenario2
#
#      # #####Test Scenario3
#      # sym_filename_only = '5MinTS3.csv'
#      # TS3Obj = bb_rsi_cci_testScenario(self.config2tfPtr, sym_filename_only)
#      # self.tsObjList.append(TS3Obj)
#      # ###End of Test Scenario3
#
#      #####Test Scenario3
#      sym_filename_only = '15MinFibsTS4.csv'
#      TS4Obj = fib_ext_15m_sell_testscenario(self.Config2tfObj, sym_filename_only)
#      self.tsObjList.append(TS4Obj)
#      ###End of Test Scenario3
