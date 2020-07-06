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

from .strategy import Strategy
####Strategies
from Strategies.s1_adx_overlap import s1_ADX_Overlap
from Strategies.s2_adx_ol_macd import s2_ADX_OL_MACD
from Strategies.s3_adx_aroon import s3_ADX5_AROON
from Strategies.s4_adx_ol_macd_4h_1h import s4_ADX_OL_MACD_4h_1h
from Strategies.s5_adx_macd_1d_4h import s5_ADX_MACD_1d_4h
from Strategies.s9_aroon_flip import s9_AROON_FLIP
#from Strategies.s11_arcci_flip import s11_ArCCI_FLIP
#from Strategies.s10_aroon_ol_flip import s10_AROON_OL_FLIP
#from Strategies.s13_bb_rsi import s13_BB_RSI
from testScenarios.simple_testScenario import simple_testScenario
from testScenarios.adx_rsi_Buy_testScenario import adx_rsi_buy_testScenario
from testScenarios.BR_Buy_testScenario import BR_Buy_testScenario
from testScenarios.AR_Buy_testScenarios import AR_Buy_testScenarios
from testScenarios.crsi_testScenario import crsi_testScenario
from testScenarios.MFI_Buy_testScenario import MFI_Buy_testScenario
from testScenarios.fib_prj_Sell_testScenario import fib_prj_sell_testscenario
from testScenarios.UO_Buy_testScenario import UO_Buy_testScenario
from testScenarios.STOCHRSI_testScenario import STOCHRSI_testScenario
from testScenarios.barLB_testScenario import barLB_testScenario

class Strategies_1D(Strategy):

    def __init__(self, args, cbIF):
        """Constructor for $class$"""
        super().__init__(args, cbIF)
        self.name = 'Strategies_1D'
        self.set_strategies()

    def set_strategies(self):
        # ######simple_testScenario
        # sym_filename_only = '5MinSimpleTS.csv'
        # TS1Obj = simple_testScenario(self.Config2tfObj, sym_filename_only)
        # self.tsObjList.append(TS1Obj)
        # ####End of Test Scenario1
       # #####Test Scenario1
       # TS1Dict = {}
       # TS1Dict['sym_filename_only'] = 'allAssets.csv'
       # TS1Dict['withinBars'] = 4
       # TS1Obj = BR_Buy_testScenario(self.Config2tfObj, TS1Dict)
       # self.tsObjList.append(TS1Obj)
       # ###End of Test Scenario1

       # #####Test Scenario2
       # TS2Dict = {}
       # TS2Dict['sym_filename_only'] = 'allAssets.csv'
       # TS2Dict['withinBars'] = 2
       # TS2Obj = AR_Buy_testScenarios(self.Config2tfObj, TS2Dict)
       # self.tsObjList.append(TS2Obj)
       # ###End of Test Scenario2

       # #####Test Scenario3
       # TS3Dict = {}
       # TS3Dict['sym_filename_only'] = 'allAssets.csv'
       # TS3Dict['withinBars'] = 4
       # TS3Obj = adx_rsi_buy_testScenario(self.Config2tfObj, TS3Dict)
       # self.tsObjList.append(TS3Obj)
       # ##End of Test Scenario3

       # #####Test Scenario4
       # TS4Dict = {}
       # TS4Dict['sym_filename_only'] = 'allAssets.csv'
       # TS4Dict['withinBars'] = 3
       # TS4Obj = crsi_testScenario(self.Config2tfObj, TS4Dict)
       # self.tsObjList.append(TS4Obj)
       # ##End of Test Scenario4

       # #####Test Scenario5
       # TS5Dict = {}
       # TS5Dict['sym_filename_only'] = 'allAssets.csv'
       # TS5Dict['withinBars'] = 2
       # TS5Obj = MFI_Buy_testScenario(self.Config2tfObj, TS5Dict)
       # self.tsObjList.append(TS5Obj)
       # ##End of Test Scenario5

       # #####Test Scenario6
       # TS6Dict = {}
       # TS6Dict['sym_filename_only'] = '1DFibPrjTS6.csv'
       # TS6Dict['withinBars'] = 300
       # TS6Obj = fib_prj_sell_testscenario(self.Config2tfObj, TS6Dict)
       # self.tsObjList.append(TS6Obj)
       # ####End of Test Scenario6

       # #####Test Scenario7
       # TS7Dict = {}
       # TS7Dict['sym_filename_only'] = 'allAssets.csv'
       # TS7Dict['withinBars'] = 4
       # TS7Obj = UO_Buy_testScenario(self.Config2tfObj, TS7Dict)
       # self.tsObjList.append(TS7Obj)
       # ####End of Test Scenario7

       # #####Test Scenario8
       # TS8Dict = {}
       # TS8Dict['sym_filename_only'] = 'allAssets.csv'
       # TS8Dict['withinBars'] = 4
       # TS8Obj = STOCHRSI_testScenario(self.Config2tfObj, TS8Dict)
       # self.tsObjList.append(TS8Obj)
       # ####End of Test Scenario8

       #####Test Scenario9
       TS9Dict = {}
       TS9Dict['sym_filename_only'] = 'allAssets.csv'
       TS9Dict['withinBars'] = 4
       TS9Obj = barLB_testScenario(self.Config2tfObj, TS9Dict)
       self.tsObjList.append(TS9Obj)
       ####End of Test Scenario9

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

