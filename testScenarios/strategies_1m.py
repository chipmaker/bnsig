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
#from .s3_adx_aroon import s3_ADX5_AROON
from Strategies.s4_adx_ol_macd_4h_1h import s4_ADX_OL_MACD_4h_1h
from Strategies.s5_adx_macd_1d_4h import s5_ADX_MACD_1d_4h
from Strategies.s7_adx_ol_macd_4h_1h_15m import s7_ADX_OL_MACD_4h_1h_15m
from Strategies.s10_aroon_ol_flip import s10_AROON_OL_FLIP
from Strategies.s12_adx_rsi import s12_ADX5_RSI
from Strategies.s13_bb_rsi import s13_BB_RSI
from Strategies.s15_adx_rsi_cci import s15_ADX_RSI_CCI
from testScenarios.fib_ext_15m_Sell_testScenario import fib_ext_15m_sell_testscenario
from testScenarios.simple_testScenario import simple_testScenario

class Strategies_1m(Strategy):

    def __init__(self, args, cbIF):
       #print("15M timeframe= {}".format(args.timeframe))
       """Constructor for $class$"""
       super().__init__(args, cbIF)
       self.set_strategies()

    def set_strategies(self):
      #####Test Scenario3
      sym_filename_only = '15MinFibsTS4.csv'
      TS4Obj = fib_ext_15m_sell_testscenario(self.Config2tfObj, sym_filename_only)
      self.tsObjList.append(TS4Obj)
      ###End of Test Scenario3

      #####Test Scenario3
      sym_filename_only = '15MinFibsTS4.csv'
      TS1Obj = simple_testScenario(self.Config2tfObj, sym_filename_only)
      TS1Obj.name = '15MinTS1'
      self.tsObjList.append(TS1Obj)

###End of Test Scenario3
          #s13_BB_RSIObj = s13_BB_RSI(self.config2tfPtr)
#s13_BB_RSIObj.withinBars = 50
           #s13_BB_RSIObj.rsiTol = 0
#self.stObjList.append(s13_BB_RSIObj)

           #s10_AROON_OL_FLIPObj = s10_AROON_OL_FLIP(self.config2tfPtr)
           #s10_AROON_OL_FLIPObj.withinBars = 15
           #self.run_list.append(s10_AROON_OL_FLIPObj)

       #s2_ADX_OL_MACDObj = s2_ADX_OL_MACD(self.config2tfPtr)
       #s2_ADX_OL_MACDObj.run()

       #self.s3_ADX5_AROONObj=s3_ADX5_AROON(Config2tf)

       #self.config2tfPtr.second_timeframe = '4h'
       #s4_ADX_OL_MACD_4h_1h_Obj=s4_ADX_OL_MACD_4h_1h(self.config2tfPtr)
       #s4_ADX_OL_MACD_4h_1h_Obj.run()

       #self.config2tfPtr.second_timeframe = '1d'
       #s5_ADX_MACD_1d_4h_Obj=s5_ADX_MACD_1d_4h(self.config2tfPtr)
       #s5_ADX_MACD_1d_4h_Obj.run()

       #self.config2tfPtr.second_timeframe = '1h'
       #self.config2tfPtr.third_timeframe = '4h'
       #s7_ADX_OL_MACD_4h_1h_15m_Obj=s7_ADX_OL_MACD_4h_1h_15m(self.config2tfPtr)
       #s7_ADX_OL_MACD_4h_1h_15m_Obj.run()

       #s10_AROON_OL_FLIPObj=s10_AROON_OL_FLIP(self.config2tfPtr)
       #s10_AROON_OL_FLIPObj.withinBars = 100
       #s10_AROON_OL_FLIPObj.run()

       #s12_ADX5_RSIObj=s12_ADX5_RSI(self.config2tfPtr)
       #s12_ADX5_RSIObj.withinBars = 15
       #s12_ADX5_RSIObj.run()
