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

from Strategies.s300_STOCHRSI import s300_STOCHRSI
from .testScenario import testScenario

class STOCHRSI_testScenario(testScenario):
    def __init__(self, Config2tf, params):
       """Constructor for $class$"""
       super().__init__(Config2tf, params)
       self.name = 'STOCHRSI_testScenario'
       self.set_scenarios()

    def set_scenarios(self):
        s300_STOCHRSIObj = s300_STOCHRSI()
        s300_STOCHRSIObj.strategy_name = self.name+' STOCHRSI_SHOW'
        s300_STOCHRSIObj.withinBars = self.withinBars
        s300_STOCHRSIObj.uoOS = 20
        s300_STOCHRSIObj.uoOB = 80
        self.stObjList.append(s300_STOCHRSIObj)

