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

from Strategies.s18_MFI import s18_MFI
#from Strategies.s18_MFI_talib import s18_MFI_talib
from .testScenario import testScenario

class MFI_Buy_testScenario(testScenario):
    def __init__(self, Config2tf, params):
       """Constructor for $class$"""
       super().__init__(Config2tf, params)
       self.name = 'MFI_Buy_testScenario'
       self.set_scenarios()

    def set_scenarios(self):
        s18_MFIObj = s18_MFI()
        s18_MFIObj.strategy_name = self.name+' MFI5_BUY_SHOW'
        s18_MFIObj.withinBars = self.withinBars
        s18_MFIObj.udShow = 1
        s18_MFIObj.mfiPeriod = 5
        s18_MFIObj.mfiOS = 10
        s18_MFIObj.mfiOB = 90
        self.stObjList.append(s18_MFIObj)

        s18_MFIObj2 = s18_MFI()
        s18_MFIObj2.strategy_name = self.name+' MFI10_BUY_SHOW'
        s18_MFIObj2.withinBars = self.withinBars
        s18_MFIObj2.udShow = 1
        s18_MFIObj2.mfiPeriod = 10
        s18_MFIObj2.mfiOS = 20
        s18_MFIObj2.mfiOB = 80
        self.stObjList.append(s18_MFIObj2)
