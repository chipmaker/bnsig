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

class Strategies_1D(Strategy):

    def __init__(self, args, cbIF):
        """Constructor for $class$"""
        super().__init__(args, cbIF)
        self.name = 'Strategies_1D'
        self.set_strategies()

    def set_strategies(self):
        #####Test Scenario8
        TS8Dict = {}
        TS8Dict['sym_filename_only'] = 'allAssets.csv'
        TS8Dict['withinBars'] = 4
        TS8Obj = STOCHRSI_testScenario(self.Config2tfObj, TS8Dict)
        self.tsObjList.append(TS8Obj)
        ####End of Test Scenario8

