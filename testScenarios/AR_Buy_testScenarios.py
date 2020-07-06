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

from Strategies.s11_arcci_flip import s11_ArCCI_FLIP
from Strategies.s8_amfi import s8_AMFI
from .testScenario import testScenario

class AR_Buy_testScenarios(testScenario):
    def __init__(self, Config2tf, params):
       """Constructor for $class$"""
       super().__init__(Config2tf, params)
       self.name = 'AR_Buy_testScenarios'
       #print('Inside ARCCI BUY Test: withinBars = {}'.format(self.withinBars))
       self.set_scenarios()

    def set_scenarios(self):
        s11_ArCCI_FLIPObj = s11_ArCCI_FLIP()
        s11_ArCCI_FLIPObj.strategy_name = self.name+' ArCCI_FLIP_BUY_SHOW'
        s11_ArCCI_FLIPObj.withinBars = self.withinBars
        s11_ArCCI_FLIPObj.udShow = 1
        self.stObjList.append(s11_ArCCI_FLIPObj)

        s8_AMFIObj = s8_AMFI()
        s8_AMFIObj.strategy_name = self.name+' AMFI_FLIP_BUY_SHOW'
        s8_AMFIObj.withinBars = self.withinBars
        s8_AMFIObj.udShow = 1
        self.stObjList.append(s8_AMFIObj)
