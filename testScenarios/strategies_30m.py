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
#from .s3_adx_aroon import s3_ADX5_AROON
from Strategies.s4_adx_ol_macd_4h_1h import s4_ADX_OL_MACD_4h_1h
from Strategies.s5_adx_macd_1d_4h import s5_ADX_MACD_1d_4h

class Strategies_30m(Strategy):

    def __init__(self, Config2tf):
       """Constructor for $class$"""
       super().__init__(Config2tf)
       self.config2tfPtr = Config2tf

    def run_strategies(self):
       s1_ADX_OverlapObj=s1_ADX_Overlap(self.config2tfPtr)
       s1_ADX_OverlapObj.run()

       #s2_ADX_OL_MACDObj = s2_ADX_OL_MACD(self.config2tfPtr)
       #s2_ADX_OL_MACDObj.run()

       #self.s3_ADX5_AROONObj=s3_ADX5_AROON(Config2tf)

       self.config2tfPtr.second_timeframe = '4h'
       s4_ADX_OL_MACD_4h_1h_Obj=s4_ADX_OL_MACD_4h_1h(self.config2tfPtr)
       s4_ADX_OL_MACD_4h_1h_Obj.run()

       #self.config2tfPtr.second_timeframe = '1d'
       #s5_ADX_MACD_1d_4h_Obj=s5_ADX_MACD_1d_4h(self.config2tfPtr)
       #s5_ADX_MACD_1d_4h_Obj.run()
